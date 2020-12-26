import signal
from datetime import datetime
from functools import partial

from tension_meter import script, utils, core, stats


def main():
    codes = {}

    # 0. Setting up graceful shutdown
    signal.signal(signal.SIGTERM, partial(stats.show_results, codes=codes))

    # 1. initialisation
    try:
        method_parser = script.get_method_parser()
        details_parser = script.get_details_parser(method_parser)
        testing_parser = script.get_testing_parser(details_parser)
        method = script.get_method(method_parser)
        url, headers, data, params = script.get_target_details(details_parser)
        count, time, template = script.get_testing_details(testing_parser)
    except utils.ScriptException as e:
        print(e)
        return

    # 2. requesting phase
    if template:
        # TODO -> setup templates
        pass
    else:
        if time:
            def is_not_over():
                return datetime.now() < time
        else:
            cpt = 0

            def is_not_over():
                nonlocal cpt
                cpt += 1
                return count > cpt
        try:
            while is_not_over():
                response = core.make_request(url, method, headers=headers, data=data, params=params)
                if response.status_code not in codes:
                    codes[response.status_code] = 0

                codes[response.status_code] += 1
                print(core.format_response(response, method, url))
        except KeyboardInterrupt:
            stats.show_results(codes)


if __name__ == '__main__':
    main()
