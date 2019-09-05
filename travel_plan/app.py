import os
import sys

import flask
folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, folder)
from travel_plan.models import db_session
try:
    import travel_plan.config as config
except:
    print('*'*10 + ' Did you create a config.py file from the config_example.py file? ' + '*'*10)

# from travel_plan.nosql_models import mongo_setup

app = flask.Flask(__name__)


def main():
    configure()
    # app.run()
    app.run(debug=True)


def configure():
    print("Configuring Flask app:")

    register_blueprints()
    print("Registered blueprints")

    setup_db()
    print("DB setup completed.")
    print("", flush=True)


def setup_db():
    db_path = config.DB_FOLDER_PATH
    os.makedirs(db_path, exist_ok=True)

    # db_existing = os.path.join(
    #     os.path.dirname(__file__),
    #     'db',
    #     'existing.sqlite'
    # )
    # db_patrol = os.path.join(
    #     os.path.dirname(__file__),
    #     'db',
    #     'patrol.sqlite'
    # )

    db_patrol = os.path.join(db_path, config.DB_NAME)

    # db_session.global_init(db_existing, db_patrol)
    # db_session.global_init("", db_patrol)
    db_session.global_init(db_patrol)


def register_blueprints():
    from travel_plan.views import index_views
    from travel_plan.views import location_views
    from travel_plan.views import map_views
    from travel_plan.views import travel_views

    app.register_blueprint(index_views.blueprint)
    app.register_blueprint(location_views.blueprint)
    app.register_blueprint(map_views.blueprint)
    app.register_blueprint(travel_views.blueprint)


if __name__ == '__main__':
    main()
