from flask import Blueprint
from flask_restx import Api
import flask_praetorian

# import namespaces
# from .owners import api_owner
# from .pets import api_pet
from .users import api_user
from .teams import api_team
from .players import api_player
from .countries import api_country
from .regions import api_region
from .localities import api_locality
from .ranking import api_ranking

# one blueprint (Flask) for all the resources
blueprint = Blueprint('PetZilla', __name__)
api = Api(blueprint, title="Clicker competition", version="1.0", description="Caring for big clicks", doc="/docs")
flask_praetorian.PraetorianError.register_error_handler_with_flask_restx(api_player)

# every resource in a namespace (RestX)
api.add_namespace(api_user, path='/user')
api.add_namespace(api_team, path='/team')
api.add_namespace(api_player, path='/player')
api.add_namespace(api_country, path='/country')
api.add_namespace(api_region, path='/region')
api.add_namespace(api_locality, path='/locality')
api.add_namespace(api_ranking, path='/ranking')
