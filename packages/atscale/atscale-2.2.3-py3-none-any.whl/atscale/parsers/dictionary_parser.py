from typing import List

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
