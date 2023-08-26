from typing import List

from atscale import atscale_errors


def append_to_branch(json_reference: dict, key, value):
    """If the given key exists in the json_reference as a list, appends the value or values to that branch.
    If the key is not in json_reference, it is created as a list of the given values.
    :raises: UserError if the given key exists in json_reference but is not a list"""
    if key not in json_reference:
        json_reference[key] = []
    elif not isinstance(json_reference[key], list):
        raise atscale_errors.UserError(
            'The given key corresponds to an existing branch in the dictionary holding a non-list item')
    if isinstance(value, list):
        json_reference[key] += value
    else:
        json_reference[key].append(value)


def create_empty_branches(json_reference: dict):
    pass


def path_exists(dict_item_this, dict_item_other, path: List[str]):
    for key in path:
        if key in dict_item_this and key in dict_item_other:
            dict_item_this = dict_item_this[key]
            dict_item_other = dict_item_other[key]
        else:
            return False
    return True


def parse_dict_list(dict_list: list, key, value) -> dict:
    """Return the first dict in dict_list where dict.get(key)==value.
    This method does not search beyond the top level of the dict (since
    some values like 'id' recur multiple times)

    Args:
        dict_list (list): a list of python dictionaries
        key (_type_): the key to search for at the top level of the dict (i.e. this does not recurse)
        value (_type_): if key is found, the value it should have to return that dict

    Returns:
        dict: the dict in the dict_list where dict.get(key)==value
    """
    if dict_list is None:
        return None
    for d in dict_list:
        if d.get(key) == value:
            return d
    return None
