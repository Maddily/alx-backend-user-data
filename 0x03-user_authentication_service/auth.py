#!/usr/bin/env python3
"""
This module provides functions for user authentication.
"""
import bcrypt


def _hash_password(password) -> bytes:
    """
    Hashes a password using bcrypt.
    """

    hashed_password = bcrypt.hashpw(str.encode(password), bcrypt.gensalt())
    return hashed_password
