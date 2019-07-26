import os

import flask

from travel_plan.sql_models import db_session
from travel_plan.nosql_models import mongo_setup

app = flask.Flask(__name__)


def main():
    configure()
    app.run(debug=True)


def configure():
    print("Configuring Flask app:")

    register_blueprints()
    print("Registered blueprints")

    setup_db()
    print("DB setup completed.")
    print("", flush=True)


def setup_db():
    mongo_setup.global_init()

    db_file = os.path.join(
        os.path.dirname(__file__),
        'db',
        'existing.sqlite'
    )

    db_session.global_init(db_file)


def register_blueprints():
    from travel_plan.views import index_views
    from travel_plan.views import map_views
    from travel_plan.views import plan_views

    app.register_blueprint(index_views.blueprint)
    app.register_blueprint(map_views.blueprint)
    app.register_blueprint(plan_views.blueprint)


if __name__ == '__main__':
    main()
