import re
import typing
from typing import Dict, List

from atscale.connection.connection import Connection
from atscale.base import endpoints
from atscale.errors import atscale_errors
from atscale.base import enums
from atscale.base.enums import Measure, Level, Hierarchy, DMVColumnBaseClass, RequestType

T = typing.TypeVar('T', enums.Level, enums.Hierarchy, enums.Measure)

def get_dmv_data(model,
                 fields: List[T] = None,
                 filter_by: Dict[T, List[str]] = None,
                 id_field: T = None):
    """ Returns DMV data for a given query type, on the given project-model in the Connection as a dict with
    items for each member of that type (ex. date_hierarchy: {}, item_hierarchy: {}).
        Args:
            model (DataModel): The connected DataModel to be queried against
            fields (list of T): A list of keys to query and return. id_field does not need to be
            included.
            filter_by (dict[T, str]): A dict with keys of fields and values of a list of that field's value
             to exclusively include in the return
            id_field (T): The field to split items in the return dict by, the value of this field will be the key in the
            dict. Defaults to None to use the name field of T
        Raises:
            UserError: If any given key is not a enums.DMVColumnBaseClass enum or the _type parameter is not a enums enum.
            Exception: If there is some other problem communicating with the atscale instance an exception may be raised

        Returns:
            dict: A dict with each member's name as the key, with the corresponding value being a dict with key-value
            pairs for each piece of metadata queried.
     """
    if model.project.published_project_name is None:
        if len(model.project.get_published_projects()) > 0:
            raise atscale_errors.UserError('The project of the provided data_model must have an associated '
                                           'published project before submitting a DMV query. '
                                           'Try calling project.select_published_project()')
        else:
            raise atscale_errors.UserError('A published project is required to query against, but there is no '
                                           'published version of the project of the provided data_model. '
                                           'A project can be published programmatically by calling Project.publish()')
    if filter_by is None:
        filter_by = {}
    if not fields:
        fields = []
        if not id_field:
            raise ValueError('One of either fields or id_field need to have a value')

    filter_after_querying = {}
    filter_in_query = {}
    for key, value in filter_by.items():  # this is almost always worth it
        if key.requires_translation():
            filter_after_querying[key] = value
        else:
            filter_in_query[key] = value
    query = generate_dmv_query_statement(fields=fields,
                                         filter_by=filter_in_query,
                                         id_field=id_field)
    rows = submit_dmv_query(atconn=model.project.atconn, query=query, project_name=model.project.published_project_name,
                            model_name=model.name)
    dict = _parse_dmv_helper(rows=rows,
                             fields=fields,
                             id_field=id_field,
                             filter_by=filter_after_querying)
    return dict

def submit_dmv_query(atconn: Connection, project_name: str, model_name: str, query: str):
    """ Submits a DMV Query to this atscale connection and returns a list of rows expressed as xml strings.
     DMV queries hit the published project, meaning any changes that are only in the draft of the project will not
     be queryable through a DMV query
    """
    query_body = dmv_query_body(statement=query, project_name=project_name, model_name=model_name)
    url = endpoints._endpoint_dmv_query(atconn)
    response = atconn._submit_request(request_type=RequestType.POST, url=url, data=query_body, content_type='xml')

    xml_text = str(response.content)

    rows = re.findall('<row>(.*?)</row>', xml_text)

    return rows

def generate_dmv_query_statement(fields: List[T] = None,
                                 filter_by: Dict[DMVColumnBaseClass, List[str]] = None,
                                 id_field: T = None):
    """ Generates a query statement to feed into submit_dmv_query, will query the given keys in the schema of the given
     type. If filter_by_names is passed, then the query will only query for the given names, otherwise it will query
     all. For example, querying Measure type without passing filter_by_names might query keys for date, price, and
     quantity, while passing filter_by_names=['date', 'item'] will only query the keys for date and item """
    # todo: assert each key is of type
    if fields is None:
        fields = []
    if id_field is None:
        id_field = fields[0].__class__.name
        id_name = f'[{id_field.__class__.name.value}]'
    else:
        id_name = f'[{id_field.value}]'
    fields = ', '.join([f'{id_name}'] + [f'[{k.value}]' for k in fields if k != id_field])
    schema = id_field.schema
    where_clause = id_field.where
    if filter_by:
        if not where_clause:
            where_clause = ' WHERE '
        else:
            where_clause += ' AND '
        filter_clauses = ['(' + ' OR '.join(f'[{k.value}] = \'{name}\'' for name in filter_by[k]) + ')' for k in
                          filter_by.keys()]
        where_clause += ' AND '.join(filter_clauses)
    return f'SELECT {fields} FROM {schema}{where_clause}'

def dmv_query_body(statement: str, project_name: str, model_name: str):
    return f"""<?xml version="1.0" encoding="UTF-8"?>
                <Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/">
                    <Body>
                        <Execute xmlns="urn:schemas-microsoft-com:xml-analysis">
                            <Command>
                            <Statement>{statement}</Statement>
                            </Command>
                            <Properties>
                            <PropertyList>
                                <Catalog>{project_name}</Catalog>
                            </PropertyList>
                            </Properties>
                            <Parameters xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
                            <Parameter>
                                <Name>CubeName</Name>
                                <Value xsi:type="xsd:string">{model_name}</Value>
                            </Parameter>
                            </Parameters>
                        </Execute>
                    </Body>
                </Envelope>"""

def _parse_dmv_helper(rows,
                      fields: List[DMVColumnBaseClass],
                      id_field: DMVColumnBaseClass,
                      filter_by: Dict[DMVColumnBaseClass, List[str]] = {}) -> Dict[str, dict]:
    """ Parses the given rows of xml text into a dict with keys determined by the name_search field and with each key
    having a dict of values for each search_term
        Args:
            rows (list of str): rows of xml text from a DMV Query
            fields (list of DMVColumnBaseClass): a list of keys corresponding to the columns in the rows to turn
            into key-value pairs in the value of the returned dict corresponding to each row's key parsed by name_key
            id_field (DMVColumnBaseClass): the key to search that is the name of the row (top level key in return dict)
            """
    # convert filter_by values to dict to save iterating fully for every filtered out value
    filter_by = {k: {v: True for v in l} for k, l in filter_by.items()}
    result = {}
    if id_field is None:
        id_field = fields[0].__class__.name
    for level in rows:
        id_untranslated = re.search(id_field.to_regex(), level)[1]
        name = id_field.translate(val=id_untranslated)
        if id_field in filter_by and name not in filter_by[id_field]:  # names will be parsed out in query unless change
            continue
        sub_dict = {}
        for term in fields:
            value = re.search(term.to_regex(), level)
            if value:
                value = value[1]
                if term in filter_by and term.translate(value) not in filter_by[term]:
                    break
                sub_dict[term.name] = term.translate(value)
            else:
                sub_dict[term.name] = ''
        else:
            if not id_field.name == 'name':
                if result.get(name):
                    result[name].append(sub_dict)
                else:
                    result[name] = [sub_dict]
            else:
                result[name] = sub_dict  # need to account for same level in two different hierarchies
    return result

def dimensions_from_dmv(rows) -> Dict[str, dict]:
    """ Parses rows of a dimension dmv query into a dimension_dict containing keys for each published categorical
    feature. Each categorical feature (dimension) maps to a dict containing the following keys: description, caption,
    visible, level_number, level_type, hierarchy, and dimension.
    :param: rows - a list of xml strings, each pertaining to a dimension
    :rtype: dict
    """
    keys = [m for m in Level if m.name != 'name']
    dimension_dict = _parse_dmv_helper(rows=rows,
                                       fields=keys,
                                       id_field=Level.name)
    return dimension_dict

def measures_from_dmv(rows) -> Dict[str, dict]:
    """ Parses the rows of a measures DMV query into a dict with keys for each measure, each of which map to a dict
    containing the keys: description, caption, folder, expression, visible, and type(of aggregation).
    :param: rows - a list of xml strings, each pertaining to a measure
    :rtype: dict
    """
    keys = [m for m in Measure if m.name != 'name']
    measure_dict = _parse_dmv_helper(rows=rows, fields=keys, id_field=Measure.name)
    return measure_dict

def hierarchies_from_dmv(rows) -> Dict[str, dict]:
    """ Parses rows of a hierarchy dmv query into a hierachy dict containing keys for each published hierarchy's query
    name. Each hierarchy maps to a dict containing the following keys: secondary_attribute(bool), dimension, caption,
    folder, visible and type.
    :param: rows - a list of xml strings, each pertaining to a hierarchy
    :rtype: dict
    """
    keys = [m for m in Hierarchy if m.name != 'name']
    hierarchy_dict = _parse_dmv_helper(rows=rows,
                                       fields=keys,
                                       id_field=Hierarchy.name)

    # levels = []
    # for level in self.get_all_categorical_features():
    #     if dimension_dict[level]['hierarchy'] in dimension_dict:
    #         levels.append(
    #             (dimension_dict[level]['level_number'], level, dimension_dict[level]['level_type']))
    #         # push the folder to each level
    #         dimension_dict[level]['folder'] = hierarchy_folder
    # hierarchy_dict['levels'] = levels
    # TODO implement ^this^ somewhere
    return hierarchy_dict
