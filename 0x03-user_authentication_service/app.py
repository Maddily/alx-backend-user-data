#!/usr/bin/env python3
"""
This module contains a Flask application
that serves as a user authentication service.
"""

from flask import Flask, jsonify, request, abort, make_response
from flask import url_for, redirect
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/")
def welcome():
    """
    Endpoint that returns a welcome message.
    """

    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def users():
    """
    Register a new user.
    """

    email = request.form['email']
    password = request.form['password']

    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login():
    """
    Handle user login.
    """

    email = request.form['email']
    password = request.form['password']

    if not AUTH.valid_login(email, password):
        abort(401)

    session_id = AUTH.create_session(email)

    response = make_response(
        jsonify({"email": email, "message": "logged in"})
        )
    response.set_cookie('session_id', session_id)

    return response


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout():
    """
    Handle user logout.
    """

    session_id = request.cookies.get('session_id', None)
    user = AUTH.get_user_from_session_id(session_id)

    if not user:
        abort(403)

    AUTH.destroy_session(user.id)
    return redirect(url_for('welcome'))


@app.route("/profile", strict_slashes=False)
def profile():
    """
    Retrieves the user's profile information.
    """

    session_id = request.cookies.get('session_id', None)
    user = AUTH.get_user_from_session_id(session_id)

    if not user:
        abort(403)

    return jsonify({"email": user.email}), 200


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token():
    """
    Get the reset password token for a user.
    """

    email = request.form['email']
    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token}), 200
    except ValueError:
        abort(403)


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password():
    """
    Update the password for a user.
    """

    email = request.form['email']
    reset_token = request.form['reset_token']
    new_password = request.form['new_password']

    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
