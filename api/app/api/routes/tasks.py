import logging
from datetime import datetime

from flask import request, jsonify
from http import HTTPStatus
from app.api import api
from app.api.models import db, Task
from app.api.routes.users import login_required


logger = logging.getLogger(__name__)


def _str_to_date(date_str: str) -> datetime.date:
    if date_str:
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    return None


def _date_to_str(date: datetime.date) -> str:
    if date:
        return date.strftime('%Y-%m-%d')
    return None


def _task_to_dict(task: Task) -> dict:
    return {
        'id': task.id,
        'issue_id': task.issue_id,
        'comment': task.comment,
        'spent_on': _date_to_str(task.spent_on),
        'duration': task.duration,
    }


def task_not_found():
    return jsonify({'message': 'No task found'}), HTTPStatus.NOT_FOUND


@api.route('/tasks', methods=['GET'])
@login_required
def get_tasks(current_user):
    issue_id = request.args.get('issue_id')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    filters = (Task.user_id == current_user.id,)

    if issue_id:
        filters = (*filters, Task.issue_id == issue_id)
    if start_date:
        filters = (*filters, Task.spent_on >= _str_to_date(start_date))
    if end_date:
        filters = (*filters, Task.spent_on <= _str_to_date(end_date))

    tasks = db.session.query(Task).filter(*filters).all()

    output = []

    for task in tasks:
        output.append(_task_to_dict(task))

    return jsonify({'tasks': output}), HTTPStatus.OK


@api.route('/tasks/<task_id>', methods=['GET'])
@login_required
def get_task(current_user, task_id):
    task = Task.get(current_user, task_id)

    if not task:
        return task_not_found()

    return jsonify({'task': _task_to_dict(task)}), HTTPStatus.OK


@api.route('/tasks', methods=['POST'])
@login_required
def create_task(current_user):
    data = request.get_json()

    task = Task(
        issue_id=data.get('issue_id'),
        user_id=current_user.id,
        comment=data['comment'],
        spent_on=_str_to_date(data['spent_on']),
        duration=data.get('duration'),
    )
    db.session.add(task)
    db.session.commit()

    return jsonify({
        'message': 'Task created',
        'task': _task_to_dict(task),
    }), HTTPStatus.CREATED


@api.route('/tasks/<task_id>', methods=['PUT'])
@login_required
def update_task(current_user, task_id):
    task = Task.get(current_user, task_id)

    if not task:
        return task_not_found()

    data = request.get_json()

    task.issue_id = data.get('issue_id')
    task.comment = data['comment']
    task.spent_on = _str_to_date(data['spent_on'])
    task.duration = data.get('duration')
    db.session.commit()

    return jsonify({'message': 'The task has been updated'}), HTTPStatus.OK


@api.route('/tasks/<task_id>', methods=['DELETE'])
@login_required
def delete_task(current_user, task_id):
    task = Task.get(current_user, task_id)

    if not task:
        return task_not_found()

    db.session.delete(task)
    db.session.commit()

    return jsonify({'message': 'The task has been deleted'}), HTTPStatus.OK
