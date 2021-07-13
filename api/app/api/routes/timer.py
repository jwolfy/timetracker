from flask import request, jsonify
from http import HTTPStatus
from app.api import api
from app.api.models import db, Timer, Task
from app.api.routes.users import login_required
from app.api.routes.tasks import task_not_found


@api.route('/timer', methods=['GET', 'POST', 'PUT', 'DELETE'])
@login_required
def timer(current_user):
    timer = _get_timer(current_user)

    if request.method in ('POST', 'PUT'):
        _increment_previous_task_duration(current_user, timer)

        new_task_id = request.get_json()['task_id']
        new_task = Task.get(current_user, new_task_id)
        if new_task:
            timer.start(new_task_id)
            db.session.commit()
        else:
            return task_not_found()

    elif request.method == 'DELETE':
        _increment_previous_task_duration(current_user, timer)
        timer.stop()
        db.session.commit()

    return jsonify({'timer': timer.as_dict()}), HTTPStatus.OK


def _get_timer(current_user) -> dict:
    timer = Timer.query.filter_by(user_id=current_user.id).first()

    if not timer:
        timer = Timer(user_id=current_user.id)
        db.session.add(timer)
        db.session.commit()

    return timer


def _increment_previous_task_duration(current_user, timer: Timer):
    if timer.task_id:
        previous_task = Task.get(current_user, timer.task_id)
        previous_task.duration += timer.as_dict()['elapsed']
        db.session.commit()


def _start_timer(timer: Timer):
    new_task_id = request.get_json()['task_id']
    timer.start(new_task_id)
    db.session.commit()
