#!/usr/bin/env python3
"""
This module provides functions for user authentication.
"""
import bcrypt
from sqlalchemy.orm.exc import NoResultFound
from db import DB
from user import User
from uuid import uuid4


def _hash_password(password) -> bytes:
    """
    Hashes a password using bcrypt.
    """

    hashed_password = bcrypt.hashpw(str.encode(password), bcrypt.gensalt())
    return hashed_password


def _generate_uuid() -> str:
    """
    Generate a UUID (Universally Unique Identifier) and return it as a string.
    """

    return str(uuid4())


class Auth:
    """
    Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email, password) -> User:
        """
        Register a new user.
        """

        try:
            existing_user = self._db.find_user_by(email=email)
            if existing_user:
                raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)

            user = self._db.add_user(email, hashed_password)
            return user

    def valid_login(self, email, password) -> bool:
        """
        Check if the provided email and password combination is valid.
        """

        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(str.encode(password), user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email) -> str:
        """
        Create a session for the user with the given email.
        """

        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)

            return session_id
        except NoResultFound:
            return None
