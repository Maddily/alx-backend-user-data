#!/usr/bin/env python3
"""
This module contains the Auth class which handles
authentication and authorization.
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """
    This class provides methods for authentication and authorization.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Checks if authentication is required for a given path.
        """

        return False

    def authorization_header(self, request=None) -> str:
        """
        Retrieves the authorization header from the request.
        """

        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the current user based on the request.
        """

        return None
