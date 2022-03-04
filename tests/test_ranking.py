import pytest
from app import create_app
from werkzeug.datastructures import Headers


@pytest.fixture
def client():
    app = create_app('config_tests.py')

    with app.test_client() as client:
        yield client


def test_getRankingPlayers(client):
    rv = client.post('/login', json={'username': 'maria', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.get('/api/ranking/players', headers=headers, follow_redirects=True)
    rsp = rv.get_json()
    assert 'Ana' == rsp[0].get('name')


def test_getRankingPlayer(client):
    rv = client.post('/login', json={'username': 'maria', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.get('/api/ranking/players/3', headers=headers, follow_redirects=True)
    rsp = rv.get_json()
    assert 85 == rsp


def test_getRankingTeams(client):
    rv = client.post('/login', json={'username': 'maria', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.get('/api/ranking/teams', headers=headers, follow_redirects=True)
    rsp = rv.get_json()
    assert 'Equipo 1' in [team for team in rsp]
    assert rsp['Equipo 1'] == 70


def test_getRankingTeam(client):
    rv = client.post('/login', json={'username': 'maria', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.get('/api/ranking/teams/1', headers=headers, follow_redirects=True)
    rsp = rv.get_json()
    assert 'Equipo 1' in [team for team in rsp]
    assert rsp['Equipo 1'] == 70


def test_getRankingCountries(client):
    rv = client.post('/login', json={'username': 'maria', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.get('/api/ranking/countries', headers=headers, follow_redirects=True)
    rsp = rv.get_json()
    assert 'Spain' in [country for country in rsp]
    assert rsp['Spain'] == 50


def test_getRankingCountry(client):
    rv = client.post('/login', json={'username': 'maria', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.get('/api/ranking/countries/1', headers=headers, follow_redirects=True)
    rsp = rv.get_json()
    assert 'Spain' in [country for country in rsp]
    assert rsp['Spain'] == 50


def test_detRankingRegions(client):
    rv = client.post('/login', json={'username': 'maria', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.get('/api/ranking/regions', headers=headers, follow_redirects=True)
    rsp = rv.get_json()
    assert 'Andalucía' in [region for region in rsp]
    assert rsp['Andalucía'] == 50


def test_getRankingRegion(client):
    rv = client.post('/login', json={'username': 'maria', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.get('/api/ranking/regions/1', headers=headers, follow_redirects=True)
    rsp = rv.get_json()
    assert 'Andalucía' in [region for region in rsp]
    assert rsp['Andalucía'] == 50


def test_getRankingLocalities(client):
    rv = client.post('/login', json={'username': 'maria', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.get('/api/ranking/localities', headers=headers, follow_redirects=True)
    rsp = rv.get_json()
    assert 'Cádiz' in [locality for locality in rsp]
    assert rsp['Cádiz'] == 50


def test_getRankingLocality(client):
    rv = client.post('/login', json={'username': 'maria', 'password': 'pestillo'})
    rsp = rv.get_json()
    assert 'access_token' in rsp.keys()

    headers = Headers()
    headers.add('Authorization', f"Bearer {rsp['access_token']}")
    rv = client.get('/api/ranking/localities/1', headers=headers, follow_redirects=True)
    rsp = rv.get_json()
    assert 'Cádiz' in [locality for locality in rsp]
    assert rsp['Cádiz'] == 50
