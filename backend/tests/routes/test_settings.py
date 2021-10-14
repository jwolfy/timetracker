from http import HTTPStatus
from test_users import _auth_headers


SETTINGS_ENDPOINT = '/settings'

settings_1 = {'redmine_url': 'www.example.com'}
settings_2 = {'redmine_url': 'www.example2.com', 'not_expected': True}


def test_settings_get_returns_default_values_if_not_set(client, token):
    response = client.get(SETTINGS_ENDPOINT, headers=_auth_headers(token))
    settings = response.get_json()['settings']

    assert response.status_code == HTTPStatus.OK
    assert len(settings) == 1
    assert settings['redmine_url'] == ''


def test_settings_get_saved_on_post(client, token):
    response = client.post(SETTINGS_ENDPOINT, headers=_auth_headers(token), json=settings_1)
    settings = response.get_json()['settings']

    assert response.status_code == HTTPStatus.OK
    assert len(settings) == 1
    assert settings['redmine_url'] == settings_1['redmine_url']


def test_settings_get_saved_on_put(client, token):
    response = client.put(SETTINGS_ENDPOINT, headers=_auth_headers(token), json=settings_1)
    settings = response.get_json()['settings']

    assert response.status_code == HTTPStatus.OK
    assert len(settings) == 1
    assert settings['redmine_url'] == settings_1['redmine_url']


def test_unexpected_setting_is_not_saved(client, token):
    response = client.post(SETTINGS_ENDPOINT, headers=_auth_headers(token), json=settings_2)
    settings = response.get_json()['settings']

    assert response.status_code == HTTPStatus.OK
    assert len(settings) == 1
    assert settings['redmine_url'] == settings_2['redmine_url']
    assert 'not_expected' not in settings
