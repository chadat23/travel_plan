from collections import namedtuple
import os
from typing import List, Callable

from bs4 import BeautifulSoup as bs
import folium

from travel_plan.sql_models.locations import Location

park_center = [37.844617, -119.491018]

Html_Chunks = namedtuple('Html_Chunks', ['head', 'body', 'scripts'])


def parse_map_html(park_map: folium.folium.Map):
    html_doc = park_map.get_root().render()
    soup = bs(html_doc, 'html.parser')
    head = soup.head
    index1 = str(head).index('<script>')
    head = str(head)[index1: -7]
    body = str(soup.body.findChildren()[0])
    index1 = str(soup).index('</body>')
    scripts = str(soup)[index1 + 7:]

    return Html_Chunks(head, body, scripts)


def get_map(center) -> folium.folium.Map:
    # park_map = folium.Map(location=center, zoom_start=10)
    park_map = folium.Map(location=center,
                          zoom_start=10,
                          tiles='https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',
                          attr='Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
                               + 'contributors, <a href="http://viewfinderpanoramas.org">SRTM</a> | Map style: &copy; '
                               + '<a href="https://opentopomap.org">OpenTopoMap</a> '
                               + '(<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)')

    yosemite_overlay = os.path.join('.', 'static', 'geojson', 'yosemite.geo.json')
    style = {'fillColor': '#00000000', 'color': '#244f23FF'}

    folium.GeoJson(yosemite_overlay, name='Yosemite Boundary', style_function=lambda x: style).add_to(park_map)

    return park_map


def add_locations_to_map(park_map: folium.folium.Map,
                         locations: List[Location],
                         popup: Callable[[Location], str],
                         tooltip: Callable[[Location], str],
                         color: str = 'darkblue') -> folium.folium.Map:

    for loc in locations:
        park_map = add_location_to_map(park_map, loc, popup, tooltip, color)

    return park_map


def add_location_to_map(park_map: folium.folium.Map,
                        location: Location,
                        popup: Callable[[Location], str],
                        tooltip: Callable[[Location], str],
                        color: str = 'darkblue') -> folium.folium.Map:

    folium.Marker(
        location=[location.latitude, location.longitude],
        popup=popup(location),
        tooltip=tooltip(location),
        icon=folium.Icon(color=color, icon=''),
    ).add_to(park_map)

    return park_map
