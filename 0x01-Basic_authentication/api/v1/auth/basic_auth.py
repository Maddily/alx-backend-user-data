#!/usr/bin/env python3
"""
This module contains the BasicAuth class for basic authentication.
"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """
    This class represents the basic authentication mechanism.
    It inherits from the Auth class.
    """

    def extract_base64_authorization_header(
              self, authorization_header: str) -> str:
        """
        Extracts the base64 encoded authorization header from the given
        authorization_header string.
        """

        if (
            authorization_header is None
            or not isinstance(authorization_header, str)
            or authorization_header.split(' ')[0] != 'Basic'
        ):
            return None

        return authorization_header.split(' ')[1]
