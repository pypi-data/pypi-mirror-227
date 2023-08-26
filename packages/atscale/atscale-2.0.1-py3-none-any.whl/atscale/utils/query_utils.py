import datetime
import json
import re
from typing import Dict, List, Tuple

from atscale.errors import atscale_errors
from atscale.base import config
from atscale.data_model.data_model import DataModel
from atscale.utils import feature_utils
from atscale.base.enums import RequestType


def generate_atscale_query(data_model: DataModel, feature_list: List[str], filter_equals: Dict[str,str] = None, 
                            filter_greater: Dict[str,str] = None, filter_less: Dict[str,str] = None,
                           filter_greater_or_equal: Dict[str,str] = None, filter_less_or_equal: Dict[str,str] = None, 
                           filter_not_equal: Dict[str,str] = None, filter_in: Dict[str,str] = None, 
                           filter_between: Dict[str,Tuple[str,str]] = None, filter_like: Dict[str,str] = None, 
                           filter_rlike: Dict[str,str] = None, filter_null: Dict[str,str] = None, 
                           filter_not_null: Dict[str,str] = None, limit: int = None, comment:str = None,
                           use_aggs=True, gen_aggs=True) -> str:
    """Generates an AtScale query to get the given features.

    Args:
        data_model (DataModel): The AtScale DataModel that the generated query interacts with.
        feature_list (List[str]): The list of features to query.
        filter_equals (Dict[str:str], optional): Filters results based on the feature equaling the value. Defaults
             to None
        filter_greater (Dict[str:str], optional): Filters results based on the feature being greater than the value.
             Defaults to None
        filter_less (Dict[str:str], optional): Filters results based on the feature being less than the value. 
            Defaults to None
        filter_greater_or_equal (Dict[str:str], optional): Filters results based on the feature being greater or 
            equaling the value. Defaults to None
        filter_less_or_equal (Dict[str:str], optional): Filters results based on the feature being less or equaling 
            the value. Defaults to None
        filter_not_equal (Dict[str:str], optional): Filters results based on the feature not equaling the value. 
            Defaults to None
        filter_in (Dict[str:List(str)], optional): Filters results based on the feature being contained in the values. 
            Takes in a list of str as the dictionary values. Defaults to None
        filter_between (Dict[str:(str,str)], optional): Filters results based on the feature being between the values.
             Defaults to None
        filter_like (Dict[str:str], optional): Filters results based on the feature being like the clause. Defaults 
            to None
        filter_rlike (Dict[str:str], optional): Filters results based on the feature being matched by the regular
            expression. Defaults to None
        filter_null (Dict[str:str], optional): Filters results to show null values of the specified features. 
            Defaults to None
        filter_not_null (Dict[str:str], optional): Filters results to exclude null values of the specified
            features. Defaults to None
        limit (int, optional): Limit the number of results. Defaults to None for no limit.
        comment (str, optional): A comment string to build into the query. Defaults to None for no comment.

    Returns:
        str: An AtScale query string
    """

    if filter_equals is None:
        filter_equals = {}
    if filter_greater is None:
        filter_greater = {}
    if filter_less is None:
        filter_less = {}
    if filter_greater_or_equal is None:
        filter_greater_or_equal = {}
    if filter_less_or_equal is None:
        filter_less_or_equal = {}
    if filter_not_equal is None:
        filter_not_equal = {}
    if filter_in is None:
        filter_in = {}
    if filter_between is None:
        filter_between = {}
    if filter_like is None:
        filter_like = {}
    if filter_rlike is None:
        filter_rlike = {}
    if filter_null is None:
        filter_null = []
    if filter_not_null is None:
        filter_not_null = []

    if type(feature_list) != list:
        raise atscale_errors.UserError(f'The features parameter must be a list')
    if type(filter_equals) != dict:
        raise atscale_errors.UserError(f'The filter_equals parameter must be a string/string dict')
    if type(filter_greater) != dict:
        raise atscale_errors.UserError(f'The filter_greater parameter must be a string/string dict')
    if type(filter_less) != dict:
        raise atscale_errors.UserError(f'The filter_less parameter must be a string/string dict')
    if type(filter_greater_or_equal) != dict:
        raise atscale_errors.UserError(f'The filter_greater_or_equal parameter must be a string/string dict')
    if type(filter_less_or_equal) != dict:
        raise atscale_errors.UserError(f'The filter_less_or_equal parameter must be a string/string dict')
    if type(filter_not_equal) != dict:
        raise atscale_errors.UserError(f'The filter_not_equal parameter must be a string/string dict')
    if type(filter_in) != dict:
        raise atscale_errors.UserError(f'The filter_in parameter must be a string/List[string] dict')
    if type(filter_between) != dict:
        raise atscale_errors.UserError(f'The filter_between parameter must be a string/Tuple(string, string) dict')
    if type(filter_like) != dict:
        raise atscale_errors.UserError(f'The filter_like parameter must be a string/string dict')
    if type(filter_rlike) != dict:
        raise atscale_errors.UserError(f'The filter_rlike parameter must be a string/string dict')
    if type(filter_null) != list:
        raise atscale_errors.UserError(f'The filter_null parameter must be a List[string]')
    if type(filter_not_null) != list:
        raise atscale_errors.UserError(f'The filter_not_null parameter must be a List[string]')

    data_df = data_model.get_features()

    list_all = data_df['name'].tolist()

    feature_utils.check_features(feature_list, list_all)

    list_params = [filter_equals, filter_greater, filter_less, filter_greater_or_equal, filter_less_or_equal, \
                   filter_not_equal, filter_in, filter_between, filter_like, filter_rlike, filter_null, \
                   filter_not_null]

    for param in list_params:
        feature_utils.check_features(param, list_all)

    categorical_features = []
    numeric_features = []

    all_categorical_features = [data_df['name'][i] for i in data_df.index if
                                not (data_df['data type'][i] == 'Aggregate' or data_df['data type'][i] == 'Calculated')]
    for feature in feature_list:
        if feature in all_categorical_features:
            categorical_features.append(feature)
        else:
            numeric_features.append(feature)

    if categorical_features:
        categorical_columns_string = ' ' + \
                                     ', '.join(f'`{x}`' for x in categorical_features)
        order_string = f' ORDER BY{categorical_columns_string}'
    else:
        order_string = ''
    
    all_columns_string = ' ' + \
                         ', '.join(f'`{x}`' for x in feature_list)

    if any(list_params):
        filter_string = ' WHERE ('
        for key, value in filter_equals.items():
            if filter_string != ' WHERE (':
                filter_string += ' and '
            if not isinstance(value, (int, float, bool)):
                filter_string += f'(`{key}` = \'{value}\')'
            else:
                filter_string += f'(`{key}` = {value})'
        for key, value in filter_greater.items():
            if filter_string != ' WHERE (':
                filter_string += ' and '
            if not isinstance(value, (int, float, bool)):
                filter_string += f'(`{key}` > \'{value}\')'
            else:
                filter_string += f'(`{key}` > {value})'
        for key, value in filter_less.items():
            if filter_string != ' WHERE (':
                filter_string += ' and '
            if not isinstance(value, (int, float, bool)):
                filter_string += f'(`{key}` < \'{value}\')'
            else:
                filter_string += f'(`{key}` < {value})'
        for key, value in filter_greater_or_equal.items():
            if filter_string != ' WHERE (':
                filter_string += ' and '
            if not isinstance(value, (int, float, bool)):
                filter_string += f'(`{key}` >= \'{value}\')'
            else:
                filter_string += f'(`{key}` >= {value})'
        for key, value in filter_less_or_equal.items():
            if filter_string != ' WHERE (':
                filter_string += ' and '
            if not isinstance(value, (int, float, bool)):
                filter_string += f'(`{key}` <= \'{value}\')'
            else:
                filter_string += f'(`{key}` <= {value})'
        for key, value in filter_not_equal.items():
            if filter_string != ' WHERE (':
                filter_string += ' and '
            if not isinstance(value, (int, float, bool)):
                filter_string += f'(`{key}` <> \'{value}\')'
            else:
                filter_string += f'(`{key}` <> {value})'
        for key, value in filter_like.items():
            if filter_string != ' WHERE (':
                filter_string += ' and '
            if not isinstance(value, (int, float, bool)):
                filter_string += f'(`{key}` LIKE \'{value}\')'
            else:
                filter_string += f'(`{key}` LIKE {value})'
        for key, value in filter_rlike.items():
            if filter_string != ' WHERE (':
                filter_string += ' and '
            filter_string += f'(`{key}` RLIKE \'{value}\')'
        for key, value in filter_in.items():
            str_values = [str(x) for x in value]
            if filter_string != ' WHERE (':
                filter_string += ' and '
            if not isinstance(value[0], (int, float, bool)):
                filter_string += f'(`{key}` IN (\''
                filter_string += '\', \''.join(str_values)
                filter_string += '\'))'
            else:
                filter_string += f'(`{key}` IN ('
                filter_string += ', '.join(str_values)
                filter_string += '))'
        for key, value in filter_between.items():
            if filter_string != ' WHERE (':
                filter_string += ' and '
            if not isinstance(value[0], (int, float, bool)):
                filter_string += f'(`{key}` BETWEEN \'{value[0]}\' and \'{value[1]}\')'
            else:
                filter_string += f'(`{key}` BETWEEN {value[0]} and {value[1]})'
        for key in filter_null:
            if filter_string != ' WHERE (':
                filter_string += ' and '
            filter_string += f'(`{key}` IS NULL)'
        for key in filter_not_null:
            if filter_string != ' WHERE (':
                filter_string += ' and '
            filter_string += f'(`{key}` IS NOT NULL)'
        filter_string += ')'
    else:
        filter_string = ''

    if limit is None:
        limit_string = ''
    else:
        limit_string = f' LIMIT {limit}'

    if comment is None:
        comment_string = ''
    else:
        comment_string = f' /* {comment} */'

    version_comment = f' /* Python library version: {config.Config().version} */'
    
    if use_aggs:
        use_aggs_comment = ''
    else:
        use_aggs_comment = ' /* use_aggs(false) */'
    if gen_aggs:
        gen_aggs_comment = ''
    else:
        gen_aggs_comment = ' /* generate_aggs(false) */'
        
    query = f'SELECT{use_aggs_comment}{gen_aggs_comment}{all_columns_string}' \
            f' FROM `{data_model.project.project_name}`.`{data_model.name}`' \
            f'{filter_string}{order_string}{limit_string}{comment_string}{version_comment}'
    return query


def generate_db_query(data_model: DataModel, atscale_query: str,
                      use_aggs: bool = True, gen_aggs: bool = True, fake_results: bool = False,
                      use_local_cache: bool = True, use_aggregate_cache: bool = True, timeout: int = 10
                      ) -> str:
    """Submits an AtScale query to the query planner and grabs the outbound query to the database which is returned.

    Args:
        data_model (DataModel): an atscale DataModel object
        atscale_query (str): an SQL query that references the atscale semantic layer (rather than the backing data warehouse)
        use_aggs (bool, optional): Whether to allow the query to use aggs. Defaults to True.
        gen_aggs (bool, optional): Whether to allow the query to generate aggs. Defaults to True.
        fake_results (bool, optional): Whether to use fake results. Defaults to False.
        use_local_cache (bool, optional): Whether to allow the query to use the local cache. Defaults to True.
        use_aggregate_cache (bool, optional): Whether to allow the query to use the aggregate cache. Defaults to True.
        timeout (int, optional): The number of minutes to wait for a response before timing out. Defaults to 10.

    Returns:
        str: the query that atscale would send to the backing data warehouse given the atscale_query sent to atscale
    """

    # if the atscale_query already has a limit in the sql, we replace it with a limit 1
    limit_match = re.search(r"LIMIT [0-9]+", atscale_query)
    if limit_match:
        inbound_query = atscale_query.replace(
            limit_match.group(0), 'LIMIT 1')
    else:
        inbound_query = f'{atscale_query} LIMIT 1'

    # we'll keep track of any comment so it can be added to the outbound query that is returned
    comment_match = re.findall(r"/\*.+?\*/", atscale_query)

    # we use a time stamp around the time we submit the query, to then query atscale to
    # try and get back the query it actually submitted to the backing data warehouse
    now = datetime.datetime.utcnow()  # current date and time
    now = now - datetime.timedelta(minutes=5)

    date_time = now.strftime('%Y-%m-%dT%H:%M:%S.000Z')

    # Post the rest query through atscale. No return value, we have to dig through logs to see what it was later
    atconn = data_model.project.atconn
    published_project_name = data_model.project.published_project_name

    atconn._post_query(query=inbound_query,
                       project_name=published_project_name,
                       use_aggs=use_aggs,
                       gen_aggs=gen_aggs,
                       fake_results=fake_results,
                       use_local_cache=use_local_cache,
                       use_aggregate_cache=use_aggregate_cache,
                       timeout=timeout
                       )

    url = f'{atconn._query_view_endpoint()}' \
          f'&querySource=user&queryStarted=5m&queryDateTimeStart={date_time}'

    response = atconn._submit_request(request_type=RequestType.GET, url=url)
    json_data = json.loads(response.content)['response']
    db_query = ''

    for query_info in json_data['data']:
        if db_query != '':
            break
        if query_info['query_text'] == inbound_query:
            for event in query_info['timeline_events']:
                if event['type'] == 'SubqueriesWall':
                    # check if it was truncated
                    if event['children'][0]['query_text_truncated']:
                        url = f'{atconn.server}:{atconn.design_center_server_port}/org/{atconn.organization}/' \
                              f'fullquerytext/queryId/{query_info["query_id"]}' \
                              f'?subquery={event["children"][0]["query_id"]}'
                        response = atconn._submit_request(request_type=RequestType.GET, url=url)
                        outbound_query = response.text
                    else:
                        outbound_query = event['children'][0]['query_text']
                    if limit_match:  # if there was a limit in the original query, replace our limit 1 with the original limit
                        db_query = outbound_query.replace('LIMIT 1', limit_match.group(0))
                        db_query = db_query.replace('TOP (1)', f'TOP ({limit_match.group(0).split()[1]})')
                    else:  # if there was no limit in the original query, then just remove ours
                        db_query = outbound_query.replace('LIMIT 1', '')
                        db_query = db_query.replace('TOP (1)', '')
                    if comment_match:  # add any comment to the outbound query
                        for comment in comment_match:
                            db_query += ' '
                            db_query += comment

                    break
    return db_query
