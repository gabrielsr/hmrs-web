from enum import Enum
from typing import Protocol


class Outcome(str, Enum):
    running = 'running'
    success = 'success'
    failure = 'failure'


def catch_and_stop_async(fnc):
    async def wrapper(*args, **kwargs):
        try:
            return await fnc(*args, **kwargs)
        except Exception as e:
            print(e)
            return Outcome.failure
    return wrapper

def catch_log_and_ignore(fnc):
    def wrapper(*args, **kwargs):
        try:
            return fnc(*args, **kwargs)
        except Exception as e:
            print(e)
    return wrapper

class AsyncJob(Protocol):

    def start(self):
        pass

    def step(self, time:float ) -> Outcome:
        """
        return 'running' for more steps
        return 'success' for success
        return 'failure' for failure
        """
        pass

    def before_finish(self):
        pass

    def finish(self, end_status):
        pass

    # @property
    # def status(self):
    #     pass

class AsyncJobAbs(AsyncJob):

    def start(self):
        pass

    def step(self, time:float ) -> Outcome:
        pass

    def before_finish(self):
        pass

    def finish(self, end_status):
        pass
