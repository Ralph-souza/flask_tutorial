import os
import tempfile

import pytest
from flaskr import create_app
from flaskr.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()  # creates and open a temporary file, returning the file descriptor and the path to it

    app = create_app({
        'TESTING': True,  # tells Flask that the app is in test mode
        'DATABASE': db_path,
    })

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):  # the client fixture calls app.test_client() with the application object created by the app fixture
    return app.test_client()  # Tests will use the client to make requests to the application without running the server


@pytest.fixture
def runner(app):  # The runner fixture is similar to client
    return app.test_cli_runner()  # creates a runner that can call the Click commands registered with the application
