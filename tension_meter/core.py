import requests

from tension_meter import utils


def make_request(client, url, method, headers=None, data=None, params=None):
    """
    Function that allows requesting accordingly to user input

    :param client: HTTP client
    :param url: target
    :param method: HTTP code
    :param headers: dict of headers (optional)
    :param data: dict of data (optional)
    :param params: dict of params optional
    :return: the requests.Response object obtained
    """
    kwargs = dict(
        headers=headers,
        data=data,
        params=params
    )
    try:
        response = getattr(client, method)(url, **kwargs)
    except requests.exceptions.RequestException as ex:
        raise utils.RequestException(str(ex))

    return response


def format_response_requests(response, method, url, verbose):
    """

    :param response: the requests.Response object obtained
    :param method: HTTP code
    :param url: target
    :param verbose: whether or not to print to content of the response
    :return: a string containing data to print
    """
    formatted_response = f'{response.status_code} {response.elapsed.total_seconds()} secs: ' \
                         f'{len(response.content)} bytes => {method.upper()} {url}'
    if verbose:
        formatted_response = f'{formatted_response}\n{response.content}'

    return formatted_response


def format_response_aiohttp(response, method, url, verbose):
    """

    :param response: the requests.Response object obtained
    :param method: HTTP code
    :param url: target
    :param verbose: whether or not to print to content of the response
    :return: a string containing data to print
    """
    formatted_response = f'{response.status} - {len(response.payload)} bytes => {method.upper()} {url}'
    if verbose:
        formatted_response = f'{formatted_response}\n{response.payload}'

    return formatted_response
