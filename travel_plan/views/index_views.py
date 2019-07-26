import flask

from travel_plan.infrastructure.view_modifiers import response

blueprint = flask.Blueprint('index', __name__, template_folder='templates')


@blueprint.route('/')
# @response(template_file='plan/entry.html')
def index():
    return flask.redirect('/plans/entry')
