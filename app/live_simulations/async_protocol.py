from enum import Enum
from typing import Protocol


class Outcome(Enum):
    running = 'running'
    success = 'success'
    failure = 'failure'

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

    @property
    def status(self):
        pass

class AsyncJobAbs(AsyncJob):

    def start(self):
        pass

    def step(self, time:float ) -> Outcome:
        pass

    def before_finish(self):
        pass

    def finish(self, end_status):
        pass
