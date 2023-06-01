from .async_protocol import AsyncJob, AsyncJobAbs, Outcome


class SimulationSpec:

    def __init__(self, map):
        self.map = map


class SimulationDescriptor:

    def __init__(self, id: int, job: AsyncJob, **kwargs):
        self.id = id
        self.job = job
        self.info = kwargs

    @property
    def status(self):
        return self.job.status


class IChannel:
    def __init__(self, id):
        self.id = id

    def send_updates(self, message):
        """ 
        Send simulation updates to the client
        """
        print(message)
        pass

    def receive_commands(self):
        """
        Receive commands from the channel
        Commands are external inputs to the simulation.
        """
        return []


class IChannelFactory:
    def __init__(self):
        pass

    def build(self, simulation_id) -> IChannel:
        return IChannel(simulation_id)


class LiveSimulation:
    def __init__(self, **kwargs):
        self.my_state = __class__.state()

    def step(self, time, commands):
        if self.my_state:
            i = next(self.my_state)
            if i is not None:
                return f'beat {i}, time: {time}', Outcome.running
            else:
                self.my_state = None

        return {}, Outcome.success

    def state():
        for i in range(3):
            yield i
        yield None
        return


class InteractiveWatchableJob(AsyncJobAbs):
    """" 
        LiveSimulation AsyncJob Adapter
        A long running process that receives commands and generate
        updates until it concludes.

        @protocol AsyncJob
    """

    def __init__(self, simulation: LiveSimulation,
                 channel: IChannel):
        self.simulation = simulation
        self.channel = channel
        self.status = 'pending'

    def start(self):
        self.channel.send_updates({'status': 'started'})
        self.status = 'started'

    def finish(self, status):
        self.channel.send_updates({'end-status': status})
        self.status = 'finished'

    def step(self, time):
        commands = self.channel.receive_commands()
        updates, status = self.simulation.step(time, commands)
        self.channel.send_updates({'status': status, 'updates': updates})
        return status


class SimulationFactory:

    def __init__(self, channel_factory: IChannelFactory):
        self.channel_factory = channel_factory
        self.next_id = 1

    def build(self, simulation_spec) -> LiveSimulation:
        id = self.get_next_id()
        channel = self.channel_factory.build(id)
        sim_desc = SimulationDescriptor(
            id=id,
            job=InteractiveWatchableJob(
                LiveSimulation(),
                channel)
        )
        return sim_desc

    def get_next_id(self):
        id = self.next_id
        self.next_id += 1
        return id


class SimulationRepository:

    def __init__(self, factory, runner_queue):
        self.factory: SimulationFactory = factory
        self.simulations: dict[int, SimulationDescriptor] = {}
        self.runner_queue = runner_queue

    def create(self, simulation_spec, owner=None):
        sim_desc = self.factory.build(simulation_spec)
        self.simulations[sim_desc.id] = sim_desc
        self.runner_queue.put(sim_desc.job)
        return sim_desc

    def get(self, id) -> InteractiveWatchableJob:
        return self.simulations[id]

    def get_active(self) -> list[InteractiveWatchableJob]:
        return self.simulations.values()

    def get_pending(self) -> list[InteractiveWatchableJob]:
        all = []
        while self.pending.qsize() > 0:
            all.append(self.pending.get())
        return all

    def clean_idle_simulations(self):
        pass
