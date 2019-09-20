import os
import sys
folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, folder)

from travel_plan import app, db

def main():
    configure()
    app.run(debug=True)


def configure():
    print("Configuring Flask app:")

    # register_blueprints()
    # print("Registered blueprints")

    setup_db()
    os.makedirs(config.PDF_FOLDER_PATH, exist_ok=True)
    print("DB setup completed.")
    print("", flush=True)


def setup_db():
    import travel_plan.models.__all_models

    models.db.create_all()


# def register_blueprints():
#     from travel_plan.views import index_views
#     from travel_plan.views import location_views
#     from travel_plan.views import map_views
#     from travel_plan.views import travel_views

#     app.register_blueprint(index_views.blueprint)
#     app.register_blueprint(location_views.blueprint)
#     app.register_blueprint(map_views.blueprint)
#     app.register_blueprint(travel_views.blueprint)


if __name__ == '__main__':
    main()
