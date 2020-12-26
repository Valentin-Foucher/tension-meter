import requests

from tension_meter import utils


def make_request(url, method, headers=None, data=None, params=None):
    kwargs = dict(
        headers=headers,
        data=data,
        params=params
    )
    try:
        response = method(url, **kwargs)
    except requests.exceptions.RequestException as ex:
        raise utils.RequestException(str(ex))

    return response


def format_response(response, method, url):
    return f'{response.status_code} {response.elapsed.total_seconds()} secs: {len(response.content)} bytes => ' \
           f'{method.__name__.upper()} {url}'

