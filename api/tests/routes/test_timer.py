from http import HTTPStatus
from test_users import _auth_headers
from test_tasks import _create_task, TASK_1, TASK_2


TIMER_ENDPOINT = 'api/timer'


def test_timer_params_are_initially_not_set(client, issue_token):
    response = client.get(TIMER_ENDPOINT, headers=_auth_headers(issue_token))
    timer = response.get_json()['timer']

    assert response.status_code == HTTPStatus.OK
    assert not timer['is_running']
    assert timer['task_id'] is None
    assert timer['started_at'] is None
    assert timer['elapsed'] == 0


def test_timer_params_are_set_on_start(client, issue_token):
    task_id = _create_task(client, issue_token, TASK_1).get_json()['task']['id']
    response = client.post(TIMER_ENDPOINT, headers=_auth_headers(issue_token), json={'task_id': task_id})
    timer = response.get_json()['timer']

    assert response.status_code == HTTPStatus.OK
    assert timer['is_running']
    assert timer['task_id'] == task_id
    assert timer['started_at'] is not None
    assert timer['elapsed'] == 0


def test_starting_timer_for_nonexistent_task_returns_not_found_error(client, issue_token):
    response = client.post(TIMER_ENDPOINT, headers=_auth_headers(issue_token), json={'task_id': 123})
    json_data = response.get_json()

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert json_data['message'] == 'No task found'
    assert json_data.get('timer') is None


def test_starting_running_timer_resets_params(client, issue_token):
    task_1_id = _create_task(client, issue_token, TASK_1).get_json()['task']['id']
    client.post(TIMER_ENDPOINT, headers=_auth_headers(issue_token), json={'task_id': task_1_id})

    task_2_id = _create_task(client, issue_token, TASK_2).get_json()['task']['id']
    response = client.post(TIMER_ENDPOINT, headers=_auth_headers(issue_token), json={'task_id': task_2_id})
    timer = response.get_json()['timer']

    assert response.status_code == HTTPStatus.OK
    assert timer['is_running']
    assert timer['task_id'] == task_2_id
    assert timer['started_at'] is not None
    assert timer['elapsed'] == 0


def test_stopping_timer_clears_all_params(client, issue_token):
    task_id = _create_task(client, issue_token, TASK_1).get_json()['task']['id']
    response = client.post(TIMER_ENDPOINT, headers=_auth_headers(issue_token), json={'task_id': task_id})

    assert response.get_json()['timer']['is_running']

    response = client.delete(TIMER_ENDPOINT, headers=_auth_headers(issue_token))
    timer = response.get_json()['timer']

    assert response.status_code == HTTPStatus.OK
    assert not timer['is_running']
    assert timer['task_id'] is None
    assert timer['started_at'] is None
    assert timer['elapsed'] == 0
