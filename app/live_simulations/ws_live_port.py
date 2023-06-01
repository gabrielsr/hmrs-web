import json
from flask_socketio import SocketIO

from flask_socketio import Namespace, emit

from app.live_simulations.async_protocol import catch_log_and_ignore



class WebSocketChannelAdapter(Namespace):
    """
    Implementation of @IChannel for WebSocket
    """

    def __init__(self, namespace):
        super().__init__(namespace=namespace)
        self.buffer = []
    
    def on_connect(self):
        print("connected")
        print(self.namespace)

    def on_command(self, command):
        self.buffer.append(command)
        print("received command: ")
        print(command)
        print(self.namespace)

    def send(self, message):
        emit('update', message)
        print(self.namespace)
    
    def on_disconnect(self):
        print("disconnected")
        print(self.namespace)
    
    @catch_log_and_ignore
    def send_updates(self, updates):
        msg = json.dumps(updates)
        self.emit('update', msg)

    @catch_log_and_ignore
    def receive_commands(self):
        commands = list(self.buffer)
        self.buffer.clear()
        return commands


class WebSocketChannelFactory:
    def __init__(self, socketio : SocketIO):
        self.socketio = socketio
        self.socketio.on('connect', self.on_connect)
    
    def on_connect(self):
        print("connected")

    def build(self, simulation_id) -> WebSocketChannelAdapter:
        ns =  f'/ws/live_simulations/{simulation_id}'
        channel = WebSocketChannelAdapter(ns)
        self.socketio.on_namespace(channel)
        return channel
