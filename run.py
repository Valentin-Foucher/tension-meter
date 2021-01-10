import asyncio
import signal

from functools import partial
from tension_meter import script, utils, stats, runner


async def main():
    codes = {}

    # 0. Setting up graceful shutdown
    signal.signal(signal.SIGTERM, partial(stats.show_results, codes=codes))

    # 1. Initialisation
    try:
        method_parser, details_parser, testing_parser = script.get_main_parser()
        method = script.get_method(method_parser)
        url, headers, data, params = script.get_target_details(details_parser)
        count, time, template, mode, verbose = script.get_testing_details(testing_parser)
    except utils.ScriptException as e:
        print(e)
        return

    args = (url, method, codes, time if time else count, headers, data, params, verbose)

    # 2. Mode selection
    if template:
        # TODO -> setup templates
        runner_class = runner.ConcurrentRunner
    elif mode == 'async':
        runner_class = runner.AsyncRunner
    elif mode == 'concurrent':
        runner_class = runner.ConcurrentRunner
    else:
        runner_class = runner.SyncRunner

    # 3. Running
    await runner_class(*args).run()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
