#!/usr/bin/env python3
"""
This module contains the SessionDBAuth class,
which is responsible for session-based authentication
using a database to store user sessions.
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """
    This class inherits from the SessionExpAuth class
    and implements session-based authentication
    using a database to store user sessions.
    """

    def create_session(self, user_id=None):
        """
        Creates a new session for the given user ID
        and saves it in the database.
        """

        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        session = UserSession(user_id=user_id, session_id=session_id)
        session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Retrieves the user ID associated with
        the given session ID from the database.
        """

        if session_id is None:
            return None

        UserSession.load_from_file()
        sessions = UserSession.search({'session_id': session_id})
        if not sessions:
            return None

        session = sessions[0]

        if self.session_duration <= 0:
            return session.user_id

        if not hasattr(session, 'created_at'):
            return None

        if (session.created_at + timedelta(
                seconds=self.session_duration)) < datetime.now():
            return None

        return session.user_id

    def destroy_session(self, request=None):
        """
        Removes the session associated with the
        given request from the database.
        """

        if not request:
            return False

        session_id = self.session_cookie(request)
        if not session_id:
            return False

        UserSession.load_from_file()

        sessions = UserSession.search({'session_id': session_id})
        if not sessions:
            return False

        session = sessions[0]
        session.remove()
        return True
