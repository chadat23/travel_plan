import flask
from flask import Markup
import folium
from bs4 import BeautifulSoup as bs

from travel_plan.infrastructure.view_modifiers import response
from travel_plan.services import travel_services


blueprint = flask.Blueprint('map', __name__, template_folder='templates')


@blueprint.route('/map/entry-exit-points')
@response(template_file='map/travel_map.html')
def heat_map():
    points = travel_services.get_lat_long_frequencies()

    m = folium.Map(location=[37.844617, -119.491018], zoom_start=10)

    for point in points:
        folium.CircleMarker(
            location=point[:2],
            radius=point[-1]*5,
            color='#428bca',
            fill=True,
            fill_color='#428bca'
        ).add_to(m)

    m.save('./templates/map/map.html')
    html_doc = m.get_root().render()
    soup = bs(html_doc, 'html.parser')
    head = soup.head
    index1 = str(head).index('<script>')
    head = str(head)[index1: -7]  
    body = soup.body.findChildren()[0]
    # scripts = ''.join(str(soup.script.findChildren()))
    index1 = str(soup).index('</body>')
    scripts = str(soup)[index1+7:]
    # scripts = 'hello'
    print('#'*20)
    print(scripts)
    print('#'*20) 

    # print('#$'*20)
    # print(soup)
    # print('#$'*20)
    # print(soup.head)
    return {'head': head,
            'body': body,
            'scripts': scripts,
            }


@blueprint.route('/map/map')
def map():
    return flask.render_template('./map/map.html')


@blueprint.route('/map/time-map/<location>')
# @response(template_file='map/heat_map.html')
def time_map(location: str):
    return f"Here's a time-map of the season's travel: {location}"
