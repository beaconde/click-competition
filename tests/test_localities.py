import pytest
from app import create_app
from werkzeug.datastructures import Headers


@pytest.fixture
def client():
    app = create_app('config_tests.py')

    with app.test_client() as client:
        yield client


def test_getLocalities(client):
    rv = client.post('/login', json={'username': 'maria', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.get('/api/locality', headers=headers, follow_redirects=True)
    rsp = rv.get_json()
    assert len(rsp) == 3
    assert 'Cádiz' in [locality.get('name') for locality in rsp]


def test_getLocality(client):
    rv = client.post('/login', json={'username': 'maria', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.get('/api/locality/1', headers=headers, follow_redirects=True)
    rsp = rv.get_json()
    assert rsp.get('name') == 'Cádiz'
    assert rsp.get('region') == 1


def test_postLocality(client):
    rv = client.post('/login', json={'username': 'maria', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.post('/api/locality', headers=headers, follow_redirects=True,
                     json={'name': 'Sevilla', 'region': 1})
    assert rv.status == '201 CREATED'


def test_putLocality(client):
    rv = client.post('/login', json={'username': 'maria', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.put('/api/locality/4', headers=headers, follow_redirects=True,
                    json={'id': 4, 'name': 'Sevilla', 'region': 2})
    rsp = rv.get_json()
    assert rv.status == '200 OK'
    assert rsp.get('name') == 'Sevilla'
    assert rsp.get('region') == 2


def test_deleteLocality(client):
    rv = client.post('/login', json={'username': 'maria', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.delete('/api/locality/4', headers=headers, follow_redirects=True)
    assert rv.status == '204 NO CONTENT'
