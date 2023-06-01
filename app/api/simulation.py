from flask_login import current_user
from flask_restx import Resource, fields
from flask import Blueprint
from flask_restx import Api
from flask_socketio import emit

from app.live_simulations.domain_model import SimulationSpec

from ..webapp import socketio

blueprint = Blueprint('api', __name__)
api = Api(blueprint, doc='/doc/')

ns = api.namespace('simulations', description='Simulations')

sim_spec = api.model('Simulation Spec', {
    'title': fields.Integer(required=True, description='Title'),
})

sim_desc= api.model('Simulation Desc', {
    'id': fields.Integer(required=True, description='id'),
    'title': fields.Integer(required=True, description='Title'),
    'status': fields.String(description='Status'),
    'ws_url': fields.String(description='Websocket URL when running'),
})

from ..webapp import task_runner
repo = task_runner.repository

@ns.route('/')
class SimulationList(Resource):
    @ns.doc('list_simulations')
    @ns.marshal_list_with(sim_desc)
    def get(self):
        '''List all '''
        return repo.get_active()

    @ns.doc('create_simulation')
    @ns.expect(sim_spec)
    @ns.marshal_with(sim_desc, code=201)
    def post(self):
        '''Create a new simulation'''
        sim_spec_inst = SimulationSpec(api.payload)
        sim =  repo.create(sim_spec_inst)
        return sim

@ns.route('/<int:id>')
@ns.param('id', 'The simulation identifier')
class Simulation(Resource):
    
    @ns.marshal_with(sim_desc)
    @ns.doc(params={'id': 'ID of a simulation'})
    def get(self, id):
        return repo.get(id)



@socketio.on('message')
def handle_message(data):
    if current_user.is_authenticated:
        emit('my response',
             {'message': '{0} has joined'.format(current_user.username)},
             broadcast=True)
        
    print('received message: ' + data)


@socketio.on('my event') 
def handle_message(data):
    if current_user.is_authenticated:
        emit('my response',
                {'message': '{0} has joined'.format(current_user.username)},
                broadcast=True)
    print('received message: ' + data['data'])

    