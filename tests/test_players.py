import pytest
from app import create_app
from werkzeug.datastructures import Headers


@pytest.fixture
def client():
    app = create_app('config_tests.py')

    with app.test_client() as client:
        yield client


def test_getPlayers(client):
    rv = client.post('/login', json={'username': 'maria', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.get('/api/player', headers=headers, follow_redirects=True)
    rsp = rv.get_json()
    assert len(rsp) == 3
    assert 'Juan' in [player.get('name') for player in rsp]


def test_getPlayer(client):
    rv = client.post('/login', json={'username': 'maria', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.get('/api/player/1', headers=headers, follow_redirects=True)
    rsp = rv.get_json()
    assert rsp.get('name') == 'Juan'
    assert rsp.get('locality') == 1
    assert rsp.get('teams') == [1]
    assert rsp.get('user') == 1


def test_postPlayer(client):
    rv = client.post('/login', json={'username': 'maria', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.post('/api/player', headers=headers, follow_redirects=True,
                    json={'name': 'Pepe', 'user': 1, 'locality': 3, 'clicks': 33, 'teams': [1, 2]})
    assert rv.status == '201 CREATED'


def test_putPlayer(client):
    rv = client.post('/login', json={'username': 'maria', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.put('/api/player/4', headers=headers, follow_redirects=True,
                    json={'id': 4, 'name': 'Pepe', 'locality': 3, 'clicks': 85, 'teams': [1]})
    rsp = rv.get_json()
    assert rv.status == '200 OK'
    assert rsp.get('name') == 'Pepe'
    assert rsp.get('locality') == 3
    assert rsp.get('clicks') == 85
    assert rsp.get('teams') == [1]


def test_postPlayerClicks(client):
    rv = client.post('/login', json={'username': 'maria', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")

    rv = client.post('/api/player/score/4', headers=headers, follow_redirects=True, json={'clicks': 20})
    assert rv.status == '201 CREATED'


def test_deletePlayer(client):
    rv = client.post('/login', json={'username': 'maria', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.delete('/api/player/4', headers=headers, follow_redirects=True)
    assert rv.status == '204 NO CONTENT'
