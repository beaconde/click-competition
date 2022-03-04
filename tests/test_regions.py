import pytest
from app import create_app
from werkzeug.datastructures import Headers


@pytest.fixture
def client():
    app = create_app('config_tests.py')

    with app.test_client() as client:
        yield client


def test_getRegions(client):
    rv = client.post('/login', json={'username': 'maria', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.get('/api/region', headers=headers, follow_redirects=True)
    rsp = rv.get_json()
    assert len(rsp) == 3
    assert 'Andalucía' in [region.get('name') for region in rsp]


def test_getRegion(client):
    rv = client.post('/login', json={'username': 'maria', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.get('/api/region/1', headers=headers, follow_redirects=True)
    rsp = rv.get_json()
    assert rsp.get('name') == 'Andalucía'
    assert rsp.get('country') == 1


def test_postRegion(client):
    rv = client.post('/login', json={'username': 'maria', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.post('/api/region', headers=headers, follow_redirects=True,
                     json={'name': 'Asturias', 'country': 1})
    assert rv.status == '201 CREATED'


def test_putRegion(client):
    rv = client.post('/login', json={'username': 'maria', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.put('/api/region/4', headers=headers, follow_redirects=True,
                    json={'id': 4, 'name': 'Asturias', 'country': 3})
    rsp = rv.get_json()
    assert rv.status == '200 OK'
    assert rsp.get('name') == 'Asturias'
    assert rsp.get('country') == 3


def test_deleteRegion(client):
    rv = client.post('/login', json={'username': 'maria', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.delete('/api/region/4', headers=headers, follow_redirects=True)
    assert rv.status == '204 NO CONTENT'
