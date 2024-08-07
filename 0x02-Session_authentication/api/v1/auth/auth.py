#!/usr/bin/env python3
"""
This module contains the Auth class which handles
authentication and authorization.
"""
from typing import List, TypeVar
import os


class Auth:
    """
    This class provides methods for authentication and authorization.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Checks if authentication is required for a given path.
        """

        if (
            path is None
            or excluded_paths is None
            or not excluded_paths
        ):
            return True

        if path[-1] != '/':
            path = path + '/'

        for excluded_path in excluded_paths:
            if excluded_path[-1] == '*':
                if path.startswith(excluded_path[:-1]):
                    return False
            elif path == excluded_path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Retrieves the authorization header from the request.
        """

        if request is None:
            return None

        auth_header_key = request.headers.get('Authorization')

        return auth_header_key

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the current user based on the request.
        """

        return None

    def session_cookie(self, request=None):
        """
        Retrieve the session cookie from the request.
        """

        if request is None:
            return None

        return request.cookies.get(os.getenv('SESSION_NAME'))
