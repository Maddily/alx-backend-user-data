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
