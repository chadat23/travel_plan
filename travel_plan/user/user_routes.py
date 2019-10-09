from flask import Blueprint, current_app, jsonify, redirect, request, url_for

from travel_plan.user import user_services

blueprint = Blueprint('traveler', __name__, template_folder='templates')


@blueprint.route('/traveler/get-responsible-party-info', methods=['GET'])
def get_responsible_party_info():
    print('starting')
    name = request.args.get('name', None, type=str)
    user = user_services.get_user_from_name(name)
    if user:
        return jsonify(name=user.name, email=user.email, 
                       home_number=user.home_number, work_number=user.work_number, cell_number=user.cell_number)
    else:        
        return jsonify(name='', email='', home_number='', work_number='', cell_number='')
        