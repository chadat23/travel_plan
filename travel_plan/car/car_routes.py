from flask import Blueprint, current_app, jsonify, redirect, request, url_for

from travel_plan.car import car_services

blueprint = Blueprint('car', __name__, template_folder='templates')


@blueprint.route('/vehicle/get-vehicle-info', methods=['GET'])
def get_responsible_party_info():
    plate = request.args.get('plate', None, type=str)
    plate = plate.split(' ')[0]
    car = car_services.get_car_by_plate(plate)
    if car:
        if car.color:
            color = car.color.name
        else:
            color = ''
        return jsonify(plate=car.plate, make=car.make, model=car.model, color=color)
    else:
        return jsonify(plate=plate, make='', model='', color='')