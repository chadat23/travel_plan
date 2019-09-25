from flask import Blueprint, redirect, url_for

blueprint = Blueprint('index', __name__, template_folder='templates')


@blueprint.route('/')
def index():
    return redirect(url_for('travel.entry_get'))
