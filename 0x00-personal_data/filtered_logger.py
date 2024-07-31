#!/usr/bin/env python3
"""
This is a module for filtering sensitive data from a message.
"""

import re


def filter_datum(fields, redaction, message, separator) -> str:
    """
    Filter sensitive data from a message.

    Args:
        fields (list): A list of strings representing
            the fields to be filtered.
        redaction (str): The string to replace the filtered data with.
        message (str): The message containing the data to be filtered.
        separator (str): The separator used to separate
            the fields and their values.

    Returns:
        str: The filtered message with sensitive data
            replaced by the redaction string.
    """

    pattrn = r'(' + '|'.join(fields) + r')=([^' + re.escape(separator) + r']+)'
    return re.sub(
            pattrn, lambda match: f'{match.group(1)}={redaction}', message
        )
