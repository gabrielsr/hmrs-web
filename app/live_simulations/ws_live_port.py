class WebSocketChannel:
    """
    Implementation of @IChannel for WebSocket
    """
    def __init__(self, simulation_id):
        self.simulation_id = simulation_id

    def send(self, message):
        pass

    def receive(self):
        pass

    def close(self):
        pass


class WebSocketChannelFactory:
    def __init__(self):
        pass

    def build(self, simulation_id) -> WebSocketChannel:
        return WebSocketChannel(simulation_id)
