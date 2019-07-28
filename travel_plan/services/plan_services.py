from datetime import datetime
from typing import Optional

from travel_plan.nosql_models.patrol import Patrol


def get_plans():
    return [
        {'name': 'flask', 'version': '1.2.3'},
        {'name': 'sqlalchemy', 'version': '2.2.0'},
        {'name': 'passlib', 'version': '3.0.0'},
    ]


def create_plan(start_date: str, entry_point: str, end_date: str, exit_point: str, tracked: str, plb: str,
                name0: str, call_sign0: str, pack_color0: str,
                name1: str, call_sign1: str, pack_color1: str,
                name2: str, call_sign2: str, pack_color2: str,
                name3: str, call_sign3: str, pack_color3: str,
                date0: str, start0: str, end0: str, route0: str, mode0: str,
                date1: str, start1: str, end1: str, route1: str, mode1: str,
                date2: str, start2: str, end2: str, route2: str, mode2: str,
                contact0: str, contact1: str,
                ) -> Optional[Patrol]:

    patrol = Patrol()
    patrol.start_date = datetime.strptime(start_date, '%Y-%m-%d')
    patrol.entry_point = entry_point
    patrol.end_date = datetime.strptime(end_date, '%Y-%m-%d')
    patrol.exit_point = exit_point

    patrol.tracked = True if tracked == 'yes' else False
    patrol.plb = plb

    patrol.name0 = name0
    patrol.call_sign0 = call_sign0
    patrol.pack_color0 = pack_color0
    patrol.name1 = name1
    patrol.call_sign1 = call_sign1
    patrol.pack_color1 = pack_color1
    patrol.name2 = name2
    patrol.call_sign2 = call_sign2
    patrol.pack_color2 = pack_color2
    patrol.name3 = name3
    patrol.call_sign3 = call_sign3
    patrol.pack_color3 = pack_color3

    patrol.date0 = None if date0 == '' else datetime.strptime(date0, '%Y-%m-%d')
    patrol.start0 = start0
    patrol.end0 = end0
    patrol.route0 = route0
    patrol.mode0 = mode0
    patrol.date1 = None if date1 == '' else datetime.strptime(date1, '%Y-%m-%d')
    patrol.start1 = start1
    patrol.end1 = end1
    patrol.route1 = route1
    patrol.mode1 = mode1
    patrol.date2 = None if date1 == '' else datetime.strptime(date2, '%Y-%m-%d')
    patrol.start2 = start2
    patrol.end2 = end2
    patrol.route2 = route2
    patrol.mode2 = mode2

    patrol.contact0 = contact0
    patrol.contact1 = contact1

    patrol.save()

    return patrol
