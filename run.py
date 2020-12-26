from tension_meter import script, utils, core


def main():
    # 1. initialisation
    method_parser = script.get_method_parser()
    details_parser = script.get_details_parser(method_parser)
    method = script.get_method(method_parser)
    url, headers, data, params = script.get_target_details(details_parser)

    # 2. requesting phase
    core.make_request(url, method, headers=headers, data=data, params=params)

    # 3. graceful shutdown


if __name__ == '__main__':
    try:
        main()
    except utils.ScriptException as e:
        print(e)
        exit()
