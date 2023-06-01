
class AsyncJob:
    def __init__(self, job):
        self.job = job
        self.status = 'created'

    def start(self):
        self.job.on_start()
        self.status = 'running'

    def step(self, time):
        yield from self.job.step(time)
        return 'finished'


class SimulationSpec:

    def __init__(self, map):
        self.map = map

class SimulationDescriptor:
    
    def __init__(self, id:int, status, job, **kwargs):
        self.id = id
        self.status = status
        self.job = job
        self.info = kwargs

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
                return f'beat {i}, time: {time}', 'running'
            else:
                self.my_state = None
        
        return {}, 'finished'

    def state():
        for i in range(3):
            yield i
        yield None
        return



class InteractiveWatchableJob(AsyncJob):
    """" 
        A long running process that receives commands and generate
        updates until it concludes.
    """
    
    def __init__(self, simulation: LiveSimulation, 
                 channel: IChannel ):
        self.simulation = simulation
        self.channel = channel

    def on_start(self):
        self.channel.send_updates({'status': 'started'})

    def on_finish(self, status):
        self.channel.send_updates({'end-status': status})

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
        id= self.get_next_id()
        sim = LiveSimulation()
        channel = self.channel_factory.build(id)
        sim_desc = SimulationDescriptor(
            id=id,
            status="created",
            # title=simulation_spec.title,
            job = InteractiveWatchableJob(
            LiveSimulation(), channel)
        )

        return sim_desc
    
    def get_next_id(self):
        id = self.next_id
        self.next_id += 1
        return id


class SimulationRepository:

    def __init__(self, factory, runner_queue):
        self.factory = factory
        self.simulations: dict[int, SimulationDescriptor] = {}
        self.runner_queue = runner_queue
        

    def create(self, simulation_spec, owner=None):
        sim_desc = self.factory.build(simulation_spec)
        sim_desc.status = 'pending'
        self.simulations[id] = sim_desc
        self.runner_queue.put(sim_desc.job)
        return sim_desc
    
    def get(self, id):
        return self.simulations[id]

    def get_active(self) -> list[InteractiveWatchableJob]:
        return self.simulations.values()
    
    def get_pending(self) -> list[InteractiveWatchableJob]:
        all = []
        while self.pending.qsize() > 0:
            all.append(self.pending.get())
        return all
    
    def kill_idle_simulations(self):
        pass


