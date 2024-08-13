#!/usr/bin/env python3
"""
This module contains functions for user authentication and profile management.
"""

import requests

URL = 'http://localhost:5000'


def register_user(email: str, password: str) -> None:
    """
    Register a new user with the given email and password.
    """

    url = f'{URL}/users'
    data = {'email': email, 'password': password}

    response = requests.post(url, data=data)
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "user created"}

    response = requests.post(url, data=data)
    assert response.status_code == 400
    assert response.json() == {"message": "email already registered"}


def log_in_wrong_password(email: str, password: str) -> None:
    """
    Attempt to log in with the given email and wrong password.
    """

    url = f'{URL}/sessions'
    data = {'email': email, 'password': password}

    response = requests.post(url, data=data)
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """
    Log in the user with the given email and password.
    """

    url = f'{URL}/sessions'
    data = {'email': email, 'password': password}

    response = requests.post(url, data=data)
    assert response.json() == {"email": email, "message": "logged in"}
    assert response.status_code == 200

    session_id = response.cookies.get('session_id', None)
    return session_id


def profile_unlogged() -> None:
    """
    Get the profile of an unlogged user.
    """

    url = f'{URL}/profile'

    response = requests.get(url)
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """
    Get the profile of a logged-in user.
    """

    url = f'{URL}/profile'

    cookies = {'session_id': session_id}
    response = requests.get(url, cookies=cookies)

    if not session_id:
        assert response.status_code == 403
    else:
        assert response.status_code == 200
        assert 'email' in response.json()


def log_out(session_id: str) -> None:
    """
    Log out the user with the given session ID.
    """

    url = f'{URL}/sessions'

    cookies = {'session_id': session_id}
    response = requests.delete(url, cookies=cookies)

    if not session_id:
        assert response.status_code == 403
    else:
        assert response.url == 'http://localhost:5000/'
        assert response.status_code == 200
        assert response.json() == {"message": "Bienvenue"}


def reset_password_token(email: str) -> str:
    """
    Request a reset password token for the user with the given email.
    """

    url = f'{URL}/reset_password'
    data = {'email': email}

    response = requests.post(url, data=data)

    assert response.status_code == 200
    assert "email" in response.json() and "reset_token" in response.json()
    assert response.json().get("email") == email
    reset_token = response.json().get("reset_token", None)

    return reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    Update the password of the user with the given email using the reset token.
    """

    url = f'{URL}/reset_password'
    data = {
        "email": email,
        "reset_token": reset_token,
        "new_password": new_password
        }

    response = requests.put(url, data=data)
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "Password updated"}

    response = requests.put(url, data=data)
    assert response.status_code == 403


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
