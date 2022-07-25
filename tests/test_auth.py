import pytest

from flask import g, session

from flaskr.db import get_db


def test_register(client, app):
    assert client.get('/auth/register').status_code == 200  # makes a GET request and returns the Response object returned by Flask
    response = client.post(
        '/auth/register', data={'username': 'a', 'password': 'a'}
    )  # makes a POST request, converting the data dict into form data
    assert response.headers['Location'] == '/auth/login'  # will have  a Location with the login URL when the register view redirects to the login view

    with app.app_context():
        assert get_db().execute(
            'SELECT * FROM user WHERE username = "a"',
        ).fetchone() is not None


@pytest.mark.parametrize(('username', 'password', 'message'), (
        ('', '', b'Username is required!'),
        ('a', '', b'Password is required!'),
        ('test', 'test', b'Already registered!'),
))  # Tells pytest to run the same test function with different arguments
def test_register_validate_input(client, username, password, message):
    response = client.post(
        '/auth/register',
        data={'username': username, 'password': password}
    )
    assert message in response.data  # contains the body of the response as bytes


def test_login(client, auth):
    assert client.get('/auth/login').status_code == 200
    response = auth.login()
    assert response.headers['Location'] == '/'

    with client:
        client.get('/')
        assert session['user_id'] == 1
        assert g.user['username'] == 'test'


@pytest.mark.parametrize(('username', 'password', 'message'), (
        ('a', 'test', b'Incorrect username!'),
        ('test', 'a', b'Incorrect password!'),
))
def test_login_validate_input(auth, username, password, message):
    response = auth.login(username, password)
    assert message in response.data


def test_logout(client, auth):
    auth.login()

    with client:  # Using client in a with block allows accessing context variables such as session after the response is returned
        auth.logout()
        assert 'user_id' not in session  # Normally, accessing session outside a request would raise an error
