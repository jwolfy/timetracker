import base64

from werkzeug.security import check_password_hash
from http import HTTPStatus
from flask import current_app


USERS_ENDPOINT = 'api/users'
LOGIN_ENDPOINT = 'api/login'

USER_1 = {'username': 'admin', 'password': 'verySecurePassword3'}
USER_2 = {'username': 'boss', 'password': 'verySecurePassword4'}


def test_nonexistent_url_returns_not_found_error(client):
    response = client.get('/non-existent-url')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert b'404 Not Found' in response.data


def _create_user(client, user=USER_1):
    response = client.post(USERS_ENDPOINT, json=user)
    return response


def test_user_is_created(client):
    response = _create_user(client)

    json_data = response.get_json()

    assert response.status_code == HTTPStatus.CREATED
    assert json_data['message'] == 'New user created'
    assert json_data['user']['name'] == USER_1['username']
    assert json_data['user']['is_admin'] is False
    assert check_password_hash(json_data['user']['password'], USER_1['password']) is True


def test_created_user_is_found_by_public_id(client):
    create_user_response = _create_user(client)
    create_user_json_data = create_user_response.get_json()

    user_id = create_user_json_data['user']['public_id']

    get_user_response = client.get(f'{USERS_ENDPOINT}/{user_id}')
    get_user_json_data = get_user_response.get_json()

    assert get_user_response.status_code == HTTPStatus.OK
    assert get_user_json_data['user']['name'] == USER_1['username']
    assert get_user_json_data['user']['public_id'] == user_id
    assert get_user_json_data['user']['is_admin'] is False
    assert check_password_hash(get_user_json_data['user']['password'], USER_1['password']) is True


def test_all_created_users_are_returned(client):
    _create_user(client)
    _create_user(client, USER_2)

    get_users_response = client.get(USERS_ENDPOINT)

    assert get_users_response.status_code == HTTPStatus.OK
    assert len(get_users_response.get_json()['users']) == 2


def test_all_users_list_is_initially_empty(client):
    get_users_response = client.get(USERS_ENDPOINT)
    users = get_users_response.get_json()['users']

    assert get_users_response.status_code == HTTPStatus.OK
    assert isinstance(users, list)
    assert not users


def test_requesting_nonexistent_user_returns_not_found_error(client):
    response = client.get(f'{USERS_ENDPOINT}/1234')
    json_data = response.get_json()

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert json_data['message'] == 'No user found'
    assert json_data.get('user') is None


def test_users_should_have_unique_name(client):
    create_user_1_response = _create_user(client)
    create_user_2_response = _create_user(client)

    assert create_user_1_response.status_code == HTTPStatus.CREATED
    assert create_user_2_response.status_code == HTTPStatus.CONFLICT
    assert create_user_2_response.get_json()['message'] == 'Could not create user. Try a different username'


def test_user_is_promoted(client):
    create_user_response = _create_user(client)
    user_id = create_user_response.get_json()['user']['public_id']

    promote_user_response = client.put(f'{USERS_ENDPOINT}/{user_id}')
    json_data = promote_user_response.get_json()

    assert promote_user_response.status_code == HTTPStatus.OK
    assert json_data['message'] == 'The user has been promoted'
    assert json_data.get('user') is None


def test_promoting_nonexistent_user_returns_not_found_error(client):
    promote_user_response = client.put(f'{USERS_ENDPOINT}/1234')

    assert promote_user_response.status_code == HTTPStatus.NOT_FOUND
    assert promote_user_response.get_json()['message'] == 'No user found'


def test_user_is_deleted(client):
    create_user_response = _create_user(client)
    user_id = create_user_response.get_json()['user']['public_id']

    delete_user_response = client.delete(f'{USERS_ENDPOINT}/{user_id}')
    delete_user_json_data = delete_user_response.get_json()

    get_user_response = client.get(f'{USERS_ENDPOINT}/{user_id}')
    get_user_json_data = get_user_response.get_json()

    assert delete_user_response.status_code == HTTPStatus.OK
    assert delete_user_json_data['message'] == 'The user has been deleted'
    assert get_user_response.status_code == HTTPStatus.NOT_FOUND
    assert get_user_json_data['message'] == 'No user found'


def test_deleting_nonexistent_user_returns_not_found_error(client):
    delete_user_response = client.put(f'{USERS_ENDPOINT}/1234')

    assert delete_user_response.status_code == HTTPStatus.NOT_FOUND
    assert delete_user_response.get_json()['message'] == 'No user found'


def _encode_auth_creds(username: str, password: str) -> str:
    return base64.b64encode(f'{username}:{password}'.encode()).decode('utf-8')


def _login_headers(username: str, password: str) -> dict:
    return {'Authorization': f'Basic {_encode_auth_creds(username, password)}'}


def _login(client, headers={}):
    return client.get(LOGIN_ENDPOINT, headers=headers)


def _authorize_user(client, user=USER_1):
    _create_user(client, user)
    response = _login(client, headers=_login_headers(**user))
    token = response.get_json()['token']
    return token


def _auth_headers(token: str) -> dict:
    return {'X-Access-Token': token}


def test_bad_auth_params_or_nonexistent_user_returns_unauthorized_error(client):
    _create_user(client)

    login_responses = [
        _login(client),
        _login(client, headers={'Authorization': ''}),
        _login(client, headers={'Authorization': 'Basic user:pass'}),
        _login(client, headers=_login_headers('user', '')),
        _login(client, headers=_login_headers('', 'pass')),
        _login(client, headers=_login_headers('user', 'pass')),
        _login(client, headers={'Authorization': f"Basic {_encode_auth_creds('user', 'pass')}"}),
        _login(client, headers=_login_headers(USER_1['username'], 'pass')),
    ]

    for response in login_responses:
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.headers.get('WWW-Authenticate') == 'Basic realm="Timetracker API"'


def test_user_receives_auth_token(client):
    _create_user(client)
    response = _login(client, headers=_login_headers(**USER_1))

    assert response.status_code == HTTPStatus.OK
    assert response.get_json()['token'] != ''


def test_missing_token_returns_unauthorized_error(client):
    current_app.config['LOGIN_REQUIRED_DISABLED'] = False

    response = client.get(USERS_ENDPOINT)

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.get_json() == {'message': 'Token is missing'}


def test_invalid_token_returns_unauthorized_error(client):
    current_app.config['LOGIN_REQUIRED_DISABLED'] = False
    _authorize_user(client)
    token = 'invalid_token'

    response = client.get(USERS_ENDPOINT, headers=_auth_headers(token))

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.get_json() == {'message': 'Token is invalid'}


def test_successful_token_authentication(client):
    current_app.config['LOGIN_REQUIRED_DISABLED'] = False
    token = _authorize_user(client)

    response = client.get(USERS_ENDPOINT, headers=_auth_headers(token))

    assert response.status_code == HTTPStatus.OK
    assert response.get_json()['users']


def test_non_admin_cannot_manage_users(client):
    current_app.config['LOGIN_REQUIRED_DISABLED'] = False
    current_app.config['ADMIN_LOGIN_REQUIRED_DISABLED'] = False
    token = _authorize_user(client)

    response = client.get(USERS_ENDPOINT, headers=_auth_headers(token))
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_admin_can_manage_users(client):
    current_app.config['LOGIN_REQUIRED_DISABLED'] = False

    create_response = _create_user(client)
    user_id = create_response.get_json()['user']['public_id']

    login_response = _login(client, headers=_login_headers(**USER_1))
    token = login_response.get_json()['token']

    client.put(f'{USERS_ENDPOINT}/{user_id}', headers=_auth_headers(token))

    current_app.config['ADMIN_LOGIN_REQUIRED_DISABLED'] = False

    response = client.get(USERS_ENDPOINT, headers=_auth_headers(token))
    assert response.status_code == HTTPStatus.OK
    assert response.get_json()['users']

