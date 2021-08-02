import logging
import sqlalchemy

from flask import request, jsonify
from http import HTTPStatus
from app.api import api
from app.api.models import db, Issue
from app.api.routes.users import login_required


logger = logging.getLogger(__name__)


@api.route('/issues', methods=['GET'])
@login_required
def get_all_issues(current_user):
    issues = Issue.query.filter_by(user_id=current_user.id).all()

    output = []

    for issue in issues:
        output.append(issue.as_dict())

    return jsonify({'issues': output}), HTTPStatus.OK


@api.route('/issues/<issue_id>', methods=['GET'])
@login_required
def get_issue(current_user, issue_id):
    issue = Issue.get(current_user, issue_id)

    if not issue:
        return jsonify({'message': 'No issue found'}), HTTPStatus.NOT_FOUND

    return jsonify({'issue': issue.as_dict()}), HTTPStatus.OK


@api.route('/issues', methods=['POST'])
@login_required
def create_issue(current_user):
    data = request.get_json()

    issue = Issue(
        issue_id=data['issue_id'],
        subject=data['subject'],
        is_active=data['is_active'],
        user_id=current_user.id,
    )
    try:
        db.session.add(issue)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        logger.exception(e)
        return jsonify({'message': 'Issue with that ID already exists'}), HTTPStatus.CONFLICT

    return jsonify({
        'message': 'Issue created',
        'issue': issue.as_dict(),
    }), HTTPStatus.CREATED


@api.route('/issues/<issue_id>', methods=['PUT'])
@login_required
def update_issue(current_user, issue_id):
    issue = Issue.get(current_user, issue_id)

    if not issue:
        return jsonify({'message': 'No issue found'}), HTTPStatus.NOT_FOUND

    data = request.get_json()

    issue.subject = data['subject']
    issue.is_active = data.get('is_active')
    db.session.commit()

    return jsonify({'message': 'The issue has been updated', 'issue': issue.as_dict()}), HTTPStatus.OK


@api.route('/issues/<issue_id>', methods=['DELETE'])
@login_required
def delete_issue(current_user, issue_id):
    issue = Issue.get(current_user, issue_id)

    if not issue:
        return jsonify({'message': 'No issue found'}), HTTPStatus.NOT_FOUND

    db.session.delete(issue)
    db.session.commit()

    return jsonify({'message': 'The issue has been deleted'}), HTTPStatus.OK
