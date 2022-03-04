import pytest
from app import create_app
from werkzeug.datastructures import Headers


@pytest.fixture
def client():
    app = create_app('config_tests.py')

    with app.test_client() as client:
        yield client


def test_getCountries(client):
    rv = client.post('/login', json={'username': 'maria', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.get('/api/country', headers=headers, follow_redirects=True)
    rsp = rv.get_json()
    assert len(rsp) == 3
    assert 'Spain' in [country.get('name') for country in rsp]


def test_getCountry(client):
    rv = client.post('/login', json={'username': 'maria', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.get('/api/country/1', headers=headers, follow_redirects=True)
    rsp = rv.get_json()
    assert rsp.get('name') == 'Spain'


def test_postCountry(client):
    rv = client.post('/login', json={'username': 'maria', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.post('/api/country', headers=headers, follow_redirects=True,
                     json={'name': 'España'})
    assert rv.status == '201 CREATED'


def test_putCountry(client):
    rv = client.post('/login', json={'username': 'maria', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.put('/api/country/4', headers=headers, follow_redirects=True,
                    json={'id': 4, 'name': 'España'})
    rsp = rv.get_json()
    assert rv.status == '200 OK'
    assert rsp.get('name') == 'España'


def test_deleteCountru(client):
    rv = client.post('/login', json={'username': 'maria', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.delete('/api/country/4', headers=headers, follow_redirects=True)
    assert rv.status == '204 NO CONTENT'
