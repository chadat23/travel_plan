from collections import namedtuple
import os

from bs4 import BeautifulSoup as bs
import folium


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
