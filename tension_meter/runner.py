import abc
import asyncio
import datetime
import multiprocessing as mp

import aiohttp
import requests

from tension_meter import core, stats, utils


class Runner(abc.ABC):
    def __init__(self, url, method, codes, limit, headers=None, data=None, params=None, verbose=False):
        self.url = url
        self.method = method
        self.codes = codes
        self.headers = headers
        self.data = data
        self.params = params
        self.limit = limit
        self.verbose = verbose
        self.cpt = 0

    def has_reached_max_count_limit(self):
        self.cpt += 1
        return self.limit >= self.cpt

    def has_reached_max_time_limit(self):
        return datetime.datetime.now() < self.limit

    def add_response_code(self, code):
        if code not in self.codes:
            self.codes[code] = 0

        self.codes[code] += 1

    def make_request(self):
        response = core.make_request(requests,
                                     self.url,
                                     self.method,
                                     headers=self.headers,
                                     data=self.data,
                                     params=self.params)
        self.add_response_code(response.status_code)

        return core.format_response_requests(response, self.method, self.url, self.verbose)

    async def run(self):
        try:
            await self._run()
        except KeyboardInterrupt:
            pass
        except utils.RequestException as e:
            print(str(e))
            exit()
        finally:
            stats.show_results(self.codes)

    @abc.abstractmethod
    async def _run(self):
        raise NotImplementedError()


class SyncRunner(Runner):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_not_over = self.has_reached_max_time_limit if isinstance(self.limit, datetime.datetime) \
            else self.has_reached_max_count_limit

    async def _run(self):
        while self.is_not_over():
            print(self.make_request())


def _concurrent_make_request(runner):
    """
    Job designed to be ran in an asynchronous mode
    :param runner: ConcurrentRunner instance
    :return: result of make_request
    """
    return runner.make_request(), list(runner.codes.keys())[0]


class SiegeRunner(Runner, abc.ABC):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if isinstance(self.limit, datetime.datetime):
            raise utils.ScriptException('Cannot use temporal limit with an async runner')


class ConcurrentRunner(SiegeRunner):
    async def _run(self):
        mp.set_start_method('spawn')
        pool = mp.Pool(4)
        results = pool.map_async(_concurrent_make_request, (self for _ in range(self.limit)))
        pool.close()
        pool.join()
        output = ''
        for result in results.get():
            output = f'{output}\n{result[0]}'
            self.add_response_code(result[1])

        print(output)


class AsyncRunner(SiegeRunner):
    async def make_request(self):
        async with core.make_request(self.session,
                                     self.url,
                                     self.method,
                                     headers=self.headers,
                                     data=self.data,
                                     params=self.params) as response:
            self.add_response_code(response.status)
            response.payload = await response.text()
            print(core.format_response_aiohttp(response, self.method, self.url, self.verbose))

    async def _run(self):
        async with aiohttp.ClientSession() as self.session:
            await asyncio.gather(*(self.make_request() for _ in range(self.limit)))
