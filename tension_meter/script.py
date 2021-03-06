import argparse
import json
import re
import datetime
import sys
import requests

from tension_meter import utils


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
        try:
            setattr(namespace, self.dest, json.loads(values))
        except json.JSONDecodeError:
            raise utils.ArgumentException(f'An error occurred while parsing {self.dest} as JSON: {values}')


def get_method_parser():
    parser = argparse.ArgumentParser(description='', add_help=False)
    parser.add_argument(
        '-P', '--POST', '--post',
        action='store_true'
    )
    parser.add_argument(
        '-G', '--GET', '--get',
        action='store_true',
    )
    parser.add_argument(
        '-Q', '--PUT', '--put',
        action='store_true',
    )
    parser.add_argument(
        '-D', '--DELETE', '--delete',
        action='store_true',
    )
    parser.add_argument(
        '-I', '--HEAD', '--head',
        action='store_true',
    )
    parser.add_argument(
        '-R', '--PATCH', '--patch',
        action='store_true',
    )
    parser.add_argument(
        '-O', '--OPTIONS', '--options',
        action='store_true',
    )

    return parser


def get_details_parser():
    parser = argparse.ArgumentParser(description='', add_help=False)
    parser.add_argument(
        'url',
        type=str,
        help='Target url'
    )
    parser.add_argument(
        '-d', '--data',
        type=str,
        action=JsonObject,
        help='Payload in JSON format'
    )
    parser.add_argument(
        '-p', '--params',
        type=str,
        action=JsonObject,
        help='Query parameters in JSON format'
    )
    parser.add_argument(
        '-H', '--headers',
        type=str,
        action=HeadersObject,
        nargs='*',
        help='Headers in JSON format'
    )
    return parser


def get_testing_parser():
    parser = argparse.ArgumentParser(description='', add_help=False)
    parser.add_argument(
        '-n', '--count',
        type=int,
        default=-1,
        help=f'The maximum amount of requests you want to perform '
             f'(by default, infinity in sync mode, {utils.MAX_ASYNC_REQUESTS} in async mode)'
    )
    parser.add_argument(
        '-t', '--time',
        type=int,
        help='The maximum time in seconds you want to be requesting (only in sync mode if no count was specified)'
    )
    parser.add_argument(
        '-b', '--template',
        type=str,
        help='TODO'
    )
    parser.add_argument(
        '-a', '--async',
        action='store_true',
        help='Shall the requests be performed asynchronously'
    )
    parser.add_argument(
        '-c', '--concurrent',
        action='store_true',
        help='Shall the requests be performed concurrently'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Shall you see the responses content'
    )
    return parser


def get_main_parser():
    method_parser = get_method_parser()
    details_parser = get_details_parser()
    testing_parser = get_testing_parser()
    parser = argparse.ArgumentParser(
        description='',
        parents=[method_parser, details_parser, testing_parser])
    parser.parse_args()
    return method_parser, details_parser, testing_parser


def get_method(parser):
    methods = []
    for method, selected in vars(parser.parse_known_args()[0]).items():
        if selected:
            methods.append(method)

    if len(methods) > 1:
        raise utils.ArgumentException(f'Only one method accepted, got {methods}')

    return methods[0].lower()


def get_target_details(parser):
    details = vars(parser.parse_known_args()[0])
    url = details['url'] if re.search(URL_REGEX, details['url']) else f'http://{details["url"]}'
    return url, details['headers'], details['data'], details['params']


def get_testing_details(parser):
    details = vars(parser.parse_known_args()[0])
    if details['count'] > 0:
        count = details['count']
        time = None
    elif details['concurrent'] or details['async']:
        count = utils.MAX_ASYNC_REQUESTS
        time = None
    else:
        count = sys.maxsize
        time = datetime.datetime.now() + datetime.timedelta(seconds=details['time']) if details['time'] else None

    if details['concurrent'] and details['async']:
        raise utils.ArgumentException('Select one mode between concurrent and asynchronous at most')

    mode = 'concurrent' if details['concurrent'] \
        else 'async' if details['async'] \
        else None

    return count, time, details['template'], mode, details['verbose']
