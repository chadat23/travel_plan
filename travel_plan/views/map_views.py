import flask

from travel_plan.infrastructure.view_modifiers import response
from travel_plan.services import patrol_services


blueprint = flask.Blueprint('map', __name__, template_folder='templates')


@blueprint.route('/map/heat-map/<location>')
# @response(template_file='map/heat_map.html')
def heat_map(location: str):
    return f"Here's a heat-map of the season's travel: {location}"


@blueprint.route('/map/time-map/<location>')
# @response(template_file='map/heat_map.html')
def time_map(location: str):
    return f"Here's a time-map of the season's travel: {location}"
