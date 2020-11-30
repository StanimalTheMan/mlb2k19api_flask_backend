import pytest 
from flask import url_for

from app import create_app


@pytest.yield_fixture(scope='session')
def app():
    """
    Setup our flask test app, this only gets executed once.

    :return: Flask app
    """
    params = {
        'DEBUG': False,
        'TESTING': True,
    }

    _app = create_app(config_name=params)

    # Establish an application context before running the tests.
    ctx = _app.app_context()
    ctx.push()

    yield _app

    ctx.pop()

@pytest.yield_fixture(scope='function')
def client(app):
    """Setup an app client, this gets executed for each test function.

    :param app: Pytest fixture
    :return: Flask app client
    """
    yield app.test_client()

def test_get_batter(app, client):
    response = client.get('/batting/player', query_string={'first': 'Mike', 'last': 'Trout'})
    assert response.status_code == 200

def test_get_pitcher(app, client):
    response = client.get('/pitching/player', query_string={'first': 'Jacob', 'last': 'deGrom'})
    assert response.status_code == 200