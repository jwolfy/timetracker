from urllib.parse import urlencode
from http import HTTPStatus
from test_users import _auth_headers
from test_issues import _create_issue, ISSUE_1, ISSUE_2


TASKS_ENDPOINT = '/tasks'

TASK_1 = {'issue_id': 1442, 'comment': 'Have fun', 'spent_on': '2021-04-01'}
TASK_2 = {'issue_id': 1444, 'comment': 'Beat about the bush', 'spent_on': '2021-04-02', 'duration': 10}
TASK_3 = {'issue_id': 1444, 'comment': 'Discussions', 'spent_on': '2021-04-03'}
TASK_4 = {'issue_id': 1444, 'comment': 'More discussions', 'spent_on': '2021-04-05'}


def _create_task(client, token, task):
    return client.post(TASKS_ENDPOINT, headers=_auth_headers(token), json=task)


def test_task_gets_created(client, token):
    _create_issue(client, token, ISSUE_1)
    response = _create_task(client, token, TASK_1)
    task = response.get_json()['task']

    assert response.status_code == HTTPStatus.CREATED
    assert task['issue_id'] == TASK_1['issue_id']
    assert task['comment'] == TASK_1['comment']
    assert task['spent_on'] == TASK_1['spent_on']
    assert task['duration'] == 0


def test_returned_tasks_are_filtered_by_query_params(client, token):
    _create_issue(client, token, ISSUE_1)
    _create_issue(client, token, ISSUE_2)

    _create_task(client, token, TASK_1)
    _create_task(client, token, TASK_2)
    task_3 = _create_task(client, token, TASK_3).get_json()['task']
    _create_task(client, token, TASK_4)

    params = urlencode({'issue_id': 1444, 'start_date': '2021-04-03', 'end_date': '2021-04-04'})

    get_response = client.get(f'{TASKS_ENDPOINT}?{params}', headers=_auth_headers(token))
    tasks = get_response.get_json()['tasks']

    assert get_response.status_code == HTTPStatus.OK
    assert len(tasks) == 1
    assert tasks[0]['id'] == task_3['id']
    assert tasks[0]['issue_id'] == TASK_3['issue_id']
    assert tasks[0]['comment'] == TASK_3['comment']
    assert tasks[0]['spent_on'] == TASK_3['spent_on']


def test_created_task_is_found_by_id(client, token):
    _create_issue(client, token, ISSUE_1)
    created_task = _create_task(client, token, TASK_1).get_json()['task']
    task_id = created_task['id']

    get_response = client.get(f"{TASKS_ENDPOINT}/{task_id}", headers=_auth_headers(token))
    task = get_response.get_json()['task']

    assert get_response.status_code == HTTPStatus.OK
    assert task['id'] == task_id
    assert task['issue_id'] == TASK_1['issue_id']
    assert task['comment'] == TASK_1['comment']
    assert task['spent_on'] == TASK_1['spent_on']


def test_requesting_nonexistent_task_returns_not_found_error(client, token):
    response = client.get(f"{TASKS_ENDPOINT}/1234", headers=_auth_headers(token))
    json_data = response.get_json()

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert json_data['message'] == 'No task found'
    assert json_data.get('task') is None


def test_task_gets_updated(client, token):
    _create_issue(client, token, ISSUE_1)
    created_task = _create_task(client, token, TASK_1).get_json()['task']
    task_id = created_task['id']

    update_response = client.put(f'{TASKS_ENDPOINT}/{task_id}', headers=_auth_headers(token), json=TASK_2)
    updated_task = update_response.get_json()['task']

    assert update_response.status_code == HTTPStatus.OK
    assert updated_task['id'] == task_id
    assert updated_task['issue_id'] == TASK_2['issue_id']
    assert updated_task['comment'] == TASK_2['comment']
    assert updated_task['spent_on'] == TASK_2['spent_on']
    assert updated_task['duration'] == TASK_2['duration']


def test_updating_nonexistent_task_returns_not_found_error(client, token):
    update_response = client.put(f"{TASKS_ENDPOINT}/1234", headers=_auth_headers(token), json=TASK_2)

    assert update_response.status_code == HTTPStatus.NOT_FOUND
    assert update_response.get_json()['message'] == 'No task found'


def test_task_gets_deleted(client, token):
    _create_issue(client, token, ISSUE_1)
    created_task = _create_task(client, token, TASK_1).get_json()['task']
    task_id = created_task['id']

    delete_response = client.delete(f"{TASKS_ENDPOINT}/{task_id}", headers=_auth_headers(token))
    get_response = client.get(f'{TASKS_ENDPOINT}/{task_id}', headers=_auth_headers(token))

    assert delete_response.status_code == HTTPStatus.OK
    assert delete_response.get_json()['message'] == 'The task has been deleted'
    assert get_response.status_code == HTTPStatus.NOT_FOUND
    assert get_response.get_json()['message'] == 'No task found'


def test_deleting_nonexistent_task_returns_not_found_error(client, token):
    delete_response = client.delete(f"{TASKS_ENDPOINT}/1234", headers=_auth_headers(token))

    assert delete_response.status_code == HTTPStatus.NOT_FOUND
    assert delete_response.get_json()['message'] == 'No task found'
