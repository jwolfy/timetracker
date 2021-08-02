import pytest
from testing_config import Config as TestingConfig
from flask import current_app
from routes.test_users import _authorize_user
from routes.test_issues import _create_issue, ISSUE_1

from app import create_app, db


@pytest.fixture
def app():
    app = create_app(TestingConfig)

    with app.app_context():
        db.create_all()

        yield app

        db.session.remove()
        db.drop_all()


@pytest.fixture
def client():
    app = create_app(TestingConfig)

    with app.test_client() as client:
        with app.app_context():
            db.create_all()

            yield client

            db.session.remove()
            db.drop_all()


@pytest.fixture
def token(client):
    current_app.config['LOGIN_REQUIRED_DISABLED'] = False
    token = _authorize_user(client)
    return token


@pytest.fixture
def issue_token(client, token):
    _create_issue(client, token, ISSUE_1)
    return token
