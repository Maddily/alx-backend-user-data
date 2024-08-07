#!/usr/bin/env python3
"""
This module contains the routes and functions
related to session authentication.
"""
from api.v1.views import app_views
from flask import request, jsonify
from models.user import User
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """
    Handles the login functionality for session authentication.
    """

    email = request.form.get('email')
    if not email or email == '':
        return jsonify({"error": "email missing"}), 400

    password = request.form.get('password')
    if not password or password == '':
        return jsonify({"error": "password missing"}), 400

    try:
        users = User.search({'email': email})
        if not users or len(users) == 0:
            return jsonify({"error": "no user found for this email"}), 404

        user = users[0]
        if not user.is_valid_password(password):
            return jsonify({"error": "wrong password"}), 401

        from api.v1.app import auth
        session_id = auth.create_session(user.id)
        user_json_repr = user.to_json()
        response = jsonify(user_json_repr)
        session_name = os.getenv('SESSION_NAME')
        response.set_cookie(session_name, session_id)
        return response
    except Exception:
        return None
