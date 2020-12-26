import argparse
import json

import requests
import re


HTTP_METHODS = {
    'POST': requests.post,
    'GET': requests.get,
    'PUT': requests.put,
    'DELETE': requests.delete,
    'HEAD': requests.head,
    'PATCH': requests.patch,
    'OPTIONS': requests.options
}

URL_REGEX = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'


class HeadersObject(argparse.Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        self._nargs = nargs
        super().__init__(option_strings, dest, nargs=nargs, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        d = {}
        for header in values:
            d = {**d, **json.loads(header)}
        setattr(namespace, self.dest, d)


class JsonObject(argparse.Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        self._nargs = nargs
        super().__init__(option_strings, dest, nargs=nargs, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, json.loads(values))


class ScriptException(Exception):
    pass


class ArgumentException(ScriptException):
    pass


class RequestException(ScriptException):
    pass


def make_request(url, method, headers=None, data=None, params=None):
    kwargs = dict(
        headers=headers,
        data=data,
        params=params
    )
    print(method)
    try:
        response = method(url, **kwargs)
    except requests.exceptions.RequestException as ex:
        raise RequestException(str(ex))

    print(response.status_code)
    print(response.text)


def main():
    # 1. initialisation
    method_parser = get_method_parser()
    details_parser = get_details_parser(method_parser)
    method = get_method(method_parser)
    url, headers, data, params = get_target_details(details_parser)

    # 2. requesting phase
    make_request(url, method, headers=headers, data=data, params=params)

    # 3. graceful shutdown


def get_method_parser():
    parser = argparse.ArgumentParser(description='', add_help=False)
    parser.add_argument(
        '-P', '--POST', '--post',
        action='store_true',
        help=''
    )
    parser.add_argument(
        '-G', '--GET', '--get',
        action='store_true',
        help=''
    )
    parser.add_argument(
        '-Q', '--PUT', '--put',
        action='store_true',
        help=''
    )
    parser.add_argument(
        '-D', '--DELETE', '--delete',
        action='store_true',
        help=''
    )
    parser.add_argument(
        '-I', '--HEAD', '--head',
        action='store_true',
        help=''
    )
    parser.add_argument(
        '-R', '--PATCH', '--patch',
        action='store_true',
        help=''
    )
    parser.add_argument(
        '-O', '--OPTIONS', '--options',
        action='store_true',
        help=''
    )

    return parser


def get_details_parser(method_parser):
    parser = argparse.ArgumentParser(description='', parents=[method_parser])
    parser.add_argument(
        'url',
        type=str,
        help=''
    )
    parser.add_argument(
        '-d', '--data',
        type=str,
        action=JsonObject,
        help=''
    )
    parser.add_argument(
        '-p', '--params',
        type=str,
        action=JsonObject,
        help=''
    )
    parser.add_argument(
        '-H', '--headers',
        type=str,
        action=HeadersObject,
        nargs='*',
        help=''
    )
    return parser


def get_method(parser):
    methods = []
    for method, selected in vars(parser.parse_known_args()[0]).items():
        if selected:
            methods.append(method)

    if len(methods) > 1:
        raise ArgumentException(f'Only one method accepted, got {methods}')

    return HTTP_METHODS.get(methods[0])


def get_target_details(parser):
    try:
        details = vars(parser.parse_args())
    except json.JSONDecodeError as ex:
        raise ArgumentException(ex)

    url = details['url']
    url = url if re.search(URL_REGEX, url) else f'http://{url}'
    return url, *[details[key] for key in ('headers', 'data', 'params')]


if __name__ == '__main__':
    try:
        main()
    except ScriptException as e:
        print(e)
        exit()
