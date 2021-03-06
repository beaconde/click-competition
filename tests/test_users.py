import pytest
from app import create_app
from werkzeug.datastructures import Headers


@pytest.fixture
def client():
    app = create_app('config_tests.py')

    with app.test_client() as client:
        yield client


def test_prueba(client):
    rv = client.get('/')
    assert "Here is the" in rv.get_data(as_text=True)


def test_login(client):
    rv = client.post('/login', json={'username': 'selena', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.get('/api/user', headers=headers, follow_redirects=True)
    rsp = rv.get_json()
    assert len(rsp) == 4
    assert "selena" in [d.get("username") for d in rsp]


def test_getUser(client):
    rv = client.post('/login', json={'username': 'maria', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.get('/api/user/1', headers=headers, follow_redirects=True)
    rsp = rv.get_json()
    assert rsp.get('username') == 'juan'
    assert rsp.get('roles') == [1]
    assert rsp.get('is_active') is True
    assert rsp.get('email') == "juan@a.a"


def test_postUser(client):
    rv = client.post('/login', json={'username': 'maria', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.post('/api/user', headers=headers, follow_redirects=True,
                     json={'username': 'pepe', 'email': 'email@email.com',
                           'hashed_password': 'pestillo', 'roles': [1, 2, 3]})
    assert rv.status == '201 CREATED'


def test_putUser(client):
    rv = client.post('/login', json={'username': 'maria', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.put('/api/user/4', headers=headers, follow_redirects=True,
                    json={'id': 4, 'username': 'Pepe', 'email': 'pepe@pepe.com', 'roles': [1, 2]})
    rsp = rv.get_json()
    assert rv.status == '200 OK'
    assert rsp.get('username') == 'Pepe'
    assert rsp.get('email') == 'pepe@pepe.com'
    assert rsp.get('roles') == [1, 2]


def test_deleteUser(client):
    rv = client.post('/login', json={'username': 'maria', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.delete('/api/user/5', headers=headers, follow_redirects=True)
    assert rv.status == '204 NO CONTENT'
