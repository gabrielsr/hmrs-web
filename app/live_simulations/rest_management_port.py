from flask_restx import Resource, fields
from flask import Blueprint
from flask_restx import Api

blueprint = Blueprint('api', __name__)
api = Api(blueprint, doc='/doc/')

from ..models import simulation_repo

simulation_spec = api.model('simulation_spec', {
    'map_name': fields.String(required=True, description='The name of the map')
})

simulation_desc = api.model('simulation_desc', {
    'id': fields.Integer(required=True, description=''),
    'status': fields.Integer(required=True, description='')
})


@api.route('/simulations')
@api.doc(params={'map_name': 'Name of the map'})
class Reviews(Resource):
    
    @api.marshal_with(simulation_desc, as_list=True)
    def post(self, map_name):
        return simulation_repo.create(map_name)


    