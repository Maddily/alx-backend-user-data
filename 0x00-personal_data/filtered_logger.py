#!/usr/bin/env python3
"""
This is a module for filtering sensitive data from a message.
"""

import re
import logging
from typing import List


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]) -> None:
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Formats the log record and applies redaction to sensitive data.

        Args:
            record (logging.LogRecord): The log record to be formatted.

        Returns:
            str: The formatted log message with redacted sensitive data.
        """

        formatted_message = super(RedactingFormatter, self).format(record)
        return filter_datum(self.fields, self.REDACTION,
                            formatted_message, self.SEPARATOR)


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


def get_logger() -> logging.Logger:
    """
    Returns a logger object configured to log user data.

    Returns:
        logging.Logger: The logger object.
    """

    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))

    logger.addHandler(stream_handler)

    return logger
