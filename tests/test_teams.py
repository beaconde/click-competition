import pytest
from app import create_app
from werkzeug.datastructures import Headers


@pytest.fixture
def client():
    app = create_app('config_tests.py')

    with app.test_client() as client:
        yield client


def test_getTeams(client):
    rv = client.post('/login', json={'username': 'maria', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.get('api/team', headers=headers, follow_redirects=True)
    rsp = rv.get_json()
    assert len(rsp) == 3
    assert 'Equipo 1' in [team.get('name') for team in rsp]


def test_getTeam(client):
    rv = client.post('/login', json={'username': 'maria', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.get('api/team/1', headers=headers, follow_redirects=True)
    rsp = rv.get_json()
    assert rsp.get('id') == 1
    assert rsp.get('name') == 'Equipo 1'


def test_postTeam(client):
    rv = client.post('/login', json={'username': 'maria', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.post('/api/team', headers=headers, follow_redirects=True,
                    json={'name': 'Equipo 1 test'})
    assert rv.status == '201 CREATED'


def test_putTeam(client):
    rv = client.post('/login', json={'username': 'maria', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.put('/api/team/3', headers=headers, follow_redirects=True,
                    json={'id': 3, 'name': 'Equipo 1 test'})
    rsp = rv.get_json()
    assert rv.status == '200 OK'
    assert rsp.get('name') == 'Equipo 1 test'


def test_deleteTeam(client):
    rv = client.post('/login', json={'username': 'maria', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.delete('api/team/3', headers=headers, follow_redirects=True)
    assert rv.status == '204 NO CONTENT'
