#!/usr/bin/env python3
"""
This module provides a function to hash a password using bcrypt.
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hashes a password using bcrypt.

    Args:
        password (str): The password to be hashed.

    Returns:
        bytearray: The hashed password as a bytearray.
    """

    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Check if a password matches a hashed password.

    Args:
        hashed_password (bytes): The hashed password to compare against.
        password (str): The password to check.

    Returns:
        bool: True if the password matches the hashed password,
        False otherwise.
    """

    if bcrypt.checkpw(password.encode(), hashed_password):
        return True

    return False
