#!/usr/bin/env python3
"""
This module contains the SessionAuth class
which is responsible for session-based authentication.
"""
from api.v1.auth.auth import Auth
from uuid import uuid4


class SessionAuth(Auth):
    """
    This class inherits from the Auth class and
    provides session-based authentication functionality.
    """

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a new session for the given user ID.
        """
        if (
            user_id is None
            or not isinstance(user_id, str)
        ):
            return None

        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id
