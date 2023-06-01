import asyncio
import queue
import time
from app.live_simulations.async_protocol import Outcome

from app.live_simulations.domain_model import AsyncJob, IChannel, IChannelFactory





class Clock:
    def __init__(self, target_fps=60, initial_time=0):
        self.target_latency = 1/target_fps
        self.reset(initial_time)

    def reset(self, initial_time=0):
        self.last_wall_clock = -1 # to force no initial sleep
        self.next_time = initial_time

    def new():
        return Clock()
    
    async def await_singnal(self):
        # calculate the required sleep time to keep pace
        now = time.time()
        pending_sleep = ( self.last_wall_clock + self.target_latency ) - now 
        if pending_sleep > 0:
            await asyncio.sleep(pending_sleep)
        
        # update the last measure
        self.last_wall_clock = time.time()

        curr_time = self.next_time
        self.next_time += self.target_latency
        return curr_time




async def carry_time_regular_job(job: AsyncJob, target_fps=60):
    status = None
    

async def clock_worker(name, queue):
    clock = Clock(target_fps=60)
    while True:
        status = None
        job: AsyncJob = await queue.get()
        clock.reset()
        try:
            status = Outcome.running
            job.start()
            while status not in [Outcome.success, Outcome.failure]:
                time = await clock.await_singnal()
                status = job.step(time)
            job.before_finish()
        except Exception as e:
            print(e)
            status = 'error'
        finally:
            queue.task_done()
            job.finish(status=status)
        print(f'{name} done a task')

class ChannelFactory(IChannelFactory):
    def __init__(self):
        pass

    def build(self, id):
        return IChannel()

class AsyncJobRunner:
    def __init__(self):
        self.inbox = queue.Queue()
        self.queue = None

    async def run(self, num_workers=3):
        self.queue = asyncio.Queue()
        t = asyncio.create_task(handle_inbox(self))
        tasks = [t]
        for i in range(num_workers):
            task = asyncio.create_task(clock_worker(f'worker-{i}', self.queue))
            tasks.append(task)
            
        results = await asyncio.gather(*tasks)
        return results

    def put(self, job: AsyncJob):
        self.inbox.put_nowait(job)
        if self.queue is None:
            self.start_run()

    def start_run(self):
        from app.webapp import task_runner
        task_runner.execute() # start execution
    
    def cancel(self):
        for task in asyncio.all_tasks():
            task.cancel()
        self.queue = None

async def beat():
    while True:
        await asyncio.sleep(1)

async def handle_inbox(async_job_runner: AsyncJobRunner):
    """
    This function is responsible for moving jobs from the inbox to the queue.
    """
    while True:
        try:
            job = async_job_runner.inbox.get_nowait()
            async_job_runner.queue.put_nowait(job)
        except queue.Empty:
            await asyncio.sleep(1)
