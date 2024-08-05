#!/usr/bin/env python3
"""
This module contains the BasicAuth class for basic authentication.
"""
from api.v1.auth.auth import Auth
import base64
import binascii
from typing import TypeVar
from models.user import User


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

    def extract_user_credentials(
                self, decoded_base64_authorization_header: str) -> (str, str):
        """
        Extracts credentials from a decoded base64 authorization header.
        """

        if (
            decoded_base64_authorization_header is None
            or not isinstance(decoded_base64_authorization_header, str)
            or ':' not in decoded_base64_authorization_header
        ):
            return None, None

        credentials = decoded_base64_authorization_header.split(':')
        return credentials[0], credentials[1]

    def user_object_from_credentials(
                    self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """
        Retrieve a user object based on the provided email and password.
        """

        if (
            user_email is None
            or not isinstance(user_email, str)
            or user_pwd is None
            or not isinstance(user_pwd, str)
        ):
            return None

        # IF the db contains User instances
        if len(User.all()) != 0:
            try:
                # Search for users with user_email
                users = User.search({'email': user_email})
            except AttributeError:
                return None
            # IF no users are found
            if len(users) == 0:
                return None
            # IF user_pwd isn't the user's password
            if not users[0].is_valid_password(user_pwd):
                return None
            else:
                return users[0]
        else:
            return None
