import logging

from flask import request, jsonify
from http import HTTPStatus
from app.api import api
from app.api.models import db, Settings, settings_data_from_dict_as_str
from app.api.routes.users import login_required


logger = logging.getLogger(__name__)


@api.route('/settings', methods=['GET'])
@login_required
def get_settings(current_user):
    settings = Settings.get(current_user.id)
    return jsonify({'settings': settings.as_dict()}), HTTPStatus.OK


@api.route('/settings', methods=['POST', 'PUT'])
@login_required
def save_settings(current_user):
    settings = Settings.get(current_user.id)

    data = settings.as_dict()
    new_data = request.get_json()
    settings.data = settings_data_from_dict_as_str({**data, **new_data})
    db.session.commit()

    return jsonify({'message': 'Settings have been saved', 'settings': settings.as_dict()}), HTTPStatus.OK
