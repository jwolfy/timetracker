from http import HTTPStatus
from flask import current_app
from routes.test_users import USER_1, USER_2, _auth_headers, _authorize_user


ISSUES_ENDPOINT = '/issues'

ISSUE_1 = {'issue_id': 1442, 'subject': 'Users should have fun', 'is_active': True}
ISSUE_2 = {'issue_id': 1444, 'subject': 'API for the win', 'is_active': False}


def _create_issue(client, token, issue):
    return client.post(ISSUES_ENDPOINT, headers=_auth_headers(token), json=issue)


def test_issue_is_created(client, token):
    response = _create_issue(client, token, ISSUE_1)
    json_data = response.get_json()

    assert response.status_code == HTTPStatus.CREATED
    assert json_data['issue']['issue_id'] == ISSUE_1['issue_id']
    assert json_data['issue']['subject'] == ISSUE_1['subject']
    assert json_data['issue']['is_active'] == ISSUE_1['is_active']


def test_all_created_issues_are_returned(client, token):
    _create_issue(client, token, ISSUE_1)
    _create_issue(client, token, ISSUE_2)
    get_issues_response = client.get(ISSUES_ENDPOINT, headers=_auth_headers(token))

    assert get_issues_response.status_code == HTTPStatus.OK
    assert len(get_issues_response.get_json()['issues']) == 2


def test_all_issues_list_is_initially_empty(client, token):
    get_issues_response = client.get(ISSUES_ENDPOINT, headers=_auth_headers(token))
    issues = get_issues_response.get_json()['issues']

    assert get_issues_response.status_code == HTTPStatus.OK
    assert isinstance(issues, list)
    assert not issues


def test_issues_should_have_unique_issue_id_per_user(client, token):
    response_1 = _create_issue(client, token, ISSUE_1)
    response_2 = _create_issue(client, token, ISSUE_1)

    assert response_1.status_code == HTTPStatus.CREATED
    assert response_2.status_code == HTTPStatus.CONFLICT
    assert response_2.get_json()['message'] == 'Issue with that ID already exists'


def test_issues_created_by_a_user_should_not_be_visible_by_another(client):
    current_app.config['LOGIN_REQUIRED_DISABLED'] = False
    token_1 = _authorize_user(client, USER_1)
    token_2 = _authorize_user(client, USER_2)

    _create_issue(client, token_1, ISSUE_1)
    _create_issue(client, token_1, ISSUE_2)

    get_issues_response_1 = client.get(ISSUES_ENDPOINT, headers=_auth_headers(token_1))
    get_issues_response_2 = client.get(ISSUES_ENDPOINT, headers=_auth_headers(token_2))

    assert get_issues_response_1.status_code == HTTPStatus.OK
    assert len(get_issues_response_1.get_json()['issues']) == 2

    issues_2 = get_issues_response_2.get_json()['issues']
    assert get_issues_response_2.status_code == HTTPStatus.OK
    assert isinstance(issues_2, list)
    assert not issues_2


def test_created_issue_is_found_by_issue_id(client, token):
    _create_issue(client, token, ISSUE_1)

    get_response = client.get(f"{ISSUES_ENDPOINT}/{ISSUE_1['issue_id']}", headers=_auth_headers(token))
    issue_json_data = get_response.get_json()

    assert get_response.status_code == HTTPStatus.OK
    assert issue_json_data['issue']['issue_id'] == ISSUE_1['issue_id']
    assert issue_json_data['issue']['subject'] == ISSUE_1['subject']
    assert issue_json_data['issue']['is_active'] == ISSUE_1['is_active']


def test_requesting_nonexistent_issue_retuns_not_found_error(client, token):
    response = client.get(f"{ISSUES_ENDPOINT}/{ISSUE_1['issue_id']}", headers=_auth_headers(token))
    json_data = response.get_json()

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert json_data['message'] == 'No issue found'
    assert json_data.get('issue') is None


def test_issue_gets_updated(client, token):
    _create_issue(client, token, ISSUE_1)

    update_response = client.put(
        f"{ISSUES_ENDPOINT}/{ISSUE_1['issue_id']}", headers=_auth_headers(token), json=ISSUE_2)
    updated_issue = update_response.get_json()['issue']

    assert update_response.status_code == HTTPStatus.OK
    assert updated_issue['issue_id'] == ISSUE_1['issue_id']     # issue_id cannot be updated
    assert updated_issue['subject'] == ISSUE_2['subject']
    assert updated_issue['is_active'] == ISSUE_2['is_active']


def test_updating_nonexistent_issue_returns_not_found_error(client, token):
    update_response = client.put(f"{ISSUES_ENDPOINT}/1234", headers=_auth_headers(token), json=ISSUE_2)

    assert update_response.status_code == HTTPStatus.NOT_FOUND
    assert update_response.get_json()['message'] == 'No issue found'


def test_issue_gets_deleted(client, token):
    _create_issue(client, token, ISSUE_1)

    delete_response = client.delete(f"{ISSUES_ENDPOINT}/{ISSUE_1['issue_id']}", headers=_auth_headers(token))
    get_response = client.get(f"{ISSUES_ENDPOINT}/{ISSUE_1['issue_id']}", headers=_auth_headers(token))

    assert delete_response.status_code == HTTPStatus.OK
    assert delete_response.get_json()['message'] == 'The issue has been deleted'
    assert get_response.status_code == HTTPStatus.NOT_FOUND
    assert get_response.get_json()['message'] == 'No issue found'


def test_deleting_nonexistent_issue_returns_not_found_error(client, token):
    delete_response = client.delete(f"{ISSUES_ENDPOINT}/1234", headers=_auth_headers(token))

    assert delete_response.status_code == HTTPStatus.NOT_FOUND
    assert delete_response.get_json()['message'] == 'No issue found'
