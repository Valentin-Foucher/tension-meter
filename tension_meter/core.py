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

    print(response.status_code)
    print(response.text)
