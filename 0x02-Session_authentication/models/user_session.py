#!/usr/bin/env python3
"""
This module contains the UserSession class,
which represents a user session.
"""
from models.base import Base


class UserSession(Base):
    """
    Represents a user session.
    """

    def __init__(self, *args: list, **kwargs: dict):
        """
        Initializes a new instance of the UserSession class.
        """

        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
