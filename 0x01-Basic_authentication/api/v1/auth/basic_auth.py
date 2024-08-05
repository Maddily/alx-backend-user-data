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
            or not authorization_header.startswith('Basic ')
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
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except (binascii.Error, UnicodeDecodeError):
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

        credentials = decoded_base64_authorization_header.split(':', 1)
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

        try:
            users = User.search({'email': user_email})
        except Exception:
            return None

        if not users:
            return None

        user = users[0]
        if not user.is_valid_password(user_pwd):
            return None
        return user

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the current user based on the provided request.
        """

        if request is None:
            return None

        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None

        encoded_auth_header = self.extract_base64_authorization_header(
            auth_header)
        if encoded_auth_header is None:
            return None

        decoded_auth_header = self.decode_base64_authorization_header(
            encoded_auth_header)
        if decoded_auth_header is None:
            return None

        user_email, user_pwd = self.extract_user_credentials(
            decoded_auth_header)

        if user_email is None or user_pwd is None:
            return None

        return self.user_object_from_credentials(user_email, user_pwd)
