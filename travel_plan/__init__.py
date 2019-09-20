import os
import sys

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# sys.path.insert(0, folder)
try:
    from travel_plan.config import DB_FOLDER_PATH, DB_NAME
except:
    print('*'*10 + ' Did you create a config.py file from the config_example.py file? ' + '*'*10)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'nf836fnfk38fhemvid8ehekf'
os.makedirs(DB_FOLDER_PATH, exist_ok=True)
db_full_path = os.path.join(DB_FOLDER_PATH, DB_NAME)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///foo.db' + db_full_path
db = SQLAlchemy(app)

from travel_plan.views import index_views
from travel_plan.views import location_views
from travel_plan.views import map_views
from travel_plan.views import travel_views
print(type(app))
app.register_blueprint(index_views.blueprint)
app.register_blueprint(location_views.blueprint)
app.register_blueprint(map_views.blueprint)
app.register_blueprint(travel_views.blueprint)
print("Registered blueprints")