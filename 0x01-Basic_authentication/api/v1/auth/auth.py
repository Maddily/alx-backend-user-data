#!/usr/bin/env python3
"""
This module contains the Auth class which handles
authentication and authorization.
"""
import flask
from typing import List, TypeVar


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

        if path not in excluded_paths:
            return True

        return False

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
