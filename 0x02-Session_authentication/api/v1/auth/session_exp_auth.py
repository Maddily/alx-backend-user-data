#!/usr/bin/env python3
"""
This module contains the SessionExpAuth class,
which is a subclass of SessionAuth.
It provides session-based authentication
with session expiration functionality.
"""
from api.v1.auth.session_auth import SessionAuth
import os
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """
    This class provides session-based authentication
    with session expiration functionality.
    """

    def __init__(self):
        """
        Initializes a new instance of the SessionExpAuth class.
        """

        session_duration = os.getenv('SESSION_DURATION')
        try:
            self.session_duration = int(session_duration)
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """
        Creates a new session for the specified user.
        """

        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        session_dict = {
            'user_id': user_id,
            'created_at': datetime.now()
        }

        self.user_id_by_session_id[session_id] = session_dict

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Retrieves the user ID associated with the specified session ID.
        """

        if session_id is None:
            return None

        session_dict = self.user_id_by_session_id.get(session_id)
        if session_dict is None:
            return None

        if self.session_duration <= 0:
            return session_dict.get('user_id')

        created_at = session_dict.get('created_at')
        if created_at is None:
            return None

        if created_at + timedelta(
                seconds=self.session_duration) < datetime.now():
            return None

        return session_dict.get('user_id')
