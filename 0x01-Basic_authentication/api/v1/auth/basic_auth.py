#!/usr/bin/env python3
"""
This module contains the BasicAuth class for basic authentication.
"""
from api.v1.auth.auth import Auth
import base64
import binascii


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

    def decode_base64_authorization_header(
                self, base64_authorization_header: str) -> str:
        """
        Decode a base64-encoded authorization header.
        """

        if (
            base64_authorization_header is None
            or not isinstance(base64_authorization_header, str)
        ):
            return None

        try:
            decoded_s = base64.b64decode(base64_authorization_header,
                                         validate=True)
            return decoded_s.decode('utf-8')
        except binascii.Error:
            return None
