import json

import requests

from atscale.atscale_errors import UserError


def generate_headers(content_type: str = 'json', token: str = None) -> dict:
    """generate the headers needed to query the api
    Args:
        content_type (str, optional): the shorthand of the content type for headers acceptable options are ['json', 'xml', 'x-www-form-urlencoded']
        token (str, optional): the Bearer token if applicable
    Raises:
        Exception: Raises exception if non-valid content is input
    Returns:
        dict: the header dictionary
    """
    response_dict = {}

    if content_type == 'json':
        response_dict['Content-type'] = 'application/json'
    elif content_type == 'x-www-form-urlencoded':
        response_dict['Content-type'] = 'application/x-www-form-urlencoded'
    elif content_type == 'xml':
        response_dict['Content-type'] = 'application/xml'
    else:
        raise Exception(f'Invalid content_type: `{content_type}`')

    if token:
        response_dict['Authorization'] = 'Bearer ' + token

    return response_dict


def check_response(response):
    if response.ok:
        return response
    elif response.status_code == 401:  # for invalid credentials
        raise UserError(response.text)
    else:
        resp = json.loads(response.text)
        raise Exception(resp)


def get_request(url, data='', headers=None, raises=True):
    """ Sends a get request to the given url with the given parameters and returns the response.
    Raises error if response status code is not 200 unless raises is set to False in which case the errored response
    will be returned
    """
    response = requests.get(url, data=data, headers=headers)
    if raises:
        check_response(response)
    return response


def post_request(url, data='', headers=None, raises=True):
    """ Sends a post request to the given url with the given parameters and returns the response.
    Raises error if response status code is not 200 unless raises is set to False in which case the errored response
    will be returned
    """
    response = requests.post(url=url, data=data, headers=headers)
    if raises:
        check_response(response)
    return response


def put_request(url, data='', headers=None, raises=True):
    """ Sends a put request to the given url with the given parameters and returns the response.
    Raises error if response status code is not 200 unless raises is set to False in which case the errored response
    will be returned
    """
    response = requests.put(url=url,
                            data=data,
                            headers=headers)
    if raises:
        check_response(response)
    return response


def delete_request(url, data='', headers=None, raises=True):
    """ Sends a delete request to the given url with the given parameters and returns the response.
    Raises error if response status code is not 200 unless raises is set to False in which case the errored response
    will be returned
    """
    response = requests.delete(url=url,
                               data=data,
                               headers=headers)
    if raises:
        check_response(response)
    return response


def generate_query_for_post(query: str, project_name: str, organization: str, useAggs=True, genAggs=False,
                            fakeResults=False, dryRun=False,
                            useLocalCache=True, useAggregateCache=True, timeout=2) -> dict:
    return {
        'language': 'SQL',
        'query': query,
        'context': {
            'organization': {
                'id': organization
                },
            'environment': {
                'id': organization
                },
            'project': {
                'name': project_name
                }
            },
        'aggregation': {
            'useAggregates': useAggs,
            'genAggregates': genAggs
            },
        'fakeResults': fakeResults,
        'dryRun': dryRun,
        'useLocalCache': useLocalCache,
        'useAggregateCache': useAggregateCache,
        'timeout': f'{timeout}.minutes'
        }
