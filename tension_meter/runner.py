import abc
import datetime

from tension_meter import core, stats, utils


class Runner(abc.ABC):
    def __init__(self, url, method, codes, limit, headers=None, data=None, params=None):
        self.url = url
        self.method = method
        self.codes = codes
        self.headers = headers
        self.data = data
        self.params = params
        self.limit = limit
        self.cpt = 0

    def has_reached_max_count_limit(self):
        self.cpt += 1
        return self.limit > self.cpt

    def has_reached_max_time_limit(self):
        return datetime.datetime.now() < self.limit

    @abc.abstractmethod
    def run(self):
        raise NotImplementedError()


class SyncRunner(Runner):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_not_over = self.has_reached_max_time_limit if isinstance(self.limit, datetime.datetime) \
            else self.has_reached_max_count_limit

    def run(self):
        try:
            while self.is_not_over():
                response = core.make_request(self.url,
                                             self.method,
                                             headers=self.headers,
                                             data=self.data,
                                             params=self.params)

                if response.status_code not in self.codes:
                    self.codes[response.status_code] = 0

                self.codes[response.status_code] += 1
                print(core.format_response(response, self.method, self.url))
        finally:
            stats.show_results(self.codes)


class AsyncRunner(Runner):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if isinstance(self.limit, datetime.datetime):
            raise utils.ScriptException('Cannot use temporal limit with an async runner')

        self.is_not_over = self.has_reached_max_count_limit

    def run(self):
        pass
