import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from travel_plan.config import Config
# from travel_plan.infrastructure.view_modifiers import response
# from travel_plan.viewmodels.travel.travel_entry_viewmodel import TravelEntryViewModel

db: SQLAlchemy = SQLAlchemy()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    app.app_context().push()  # Didn't seen this with the other version
    db.init_app(app)

    if app.config.get('PDF_FOLDER_PATH'):
        os.makedirs(app.config['PDF_FOLDER_PATH'], exist_ok=True)
    if app.config.get('DB_FOLDER_PATH'):
        os.makedirs(app.config['DB_FOLDER_PATH'], exist_ok=True)

    # with app.app_context():
    from travel_plan.car.cars import Car
    from travel_plan.color.colors import Color
    from travel_plan.department.departments import Department
    from travel_plan.location.locations import Location
    from travel_plan.travel.travel_days import TravelDay
    from travel_plan.travel.travels import Travel
    from travel_plan.user.users import User
    db.create_all()

    from travel_plan.index import index_routes
    from travel_plan.travel import travel_routes
    app.register_blueprint(index_routes.blueprint)
    app.register_blueprint(travel_routes.blueprint)

    return app
