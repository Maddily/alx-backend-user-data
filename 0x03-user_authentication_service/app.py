#!/usr/bin/env python3
"""
This module contains a Flask application
that serves as a user authentication service.
"""

from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def welcome():
    """
    Endpoint that returns a welcome message.
    """

    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
