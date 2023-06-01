
import asyncio
from app.live_simulations.domain_model import IChannelFactory, SimulationFactory, SimulationRepository
from app.live_simulations.infra_async_jobs import AsyncJobRunner



class TaskRunner:
    def __init__(self):
        channel_factory = IChannelFactory()
        sim_factory = SimulationFactory(channel_factory)
        self.sim_runner = AsyncJobRunner()
        self.repository = SimulationRepository(
            factory = sim_factory, 
            runner_queue = self.sim_runner)
    
        self.executor = None

    def run(self):
        """ run the event loop """
        print("running async.io event loop")
        try:
            asyncio.run(self.sim_runner.run(num_workers=3))
        except Exception as e:
            print("error on async.io event loop")
            print(e)
        finally:
            self.sim_runner.cancel()
            print("done with async.io event loop")

    def init_app(self, app):
        with app.app_context():
            from app.webapp import executor
            # from app.webapp import app
            self.executor = executor

    def execute(self):
        """ submit a task to the executor 
            execute should create a thread or process and run the event loop
        """
        self.executor.submit(self.run)

        

