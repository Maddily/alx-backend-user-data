#!/usr/bin/env python3
"""
This is a module for filtering sensitive data from a message.
"""

import re
import logging
from typing import List
import os
import mysql.connector
from mysql.connector import connection


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


def filter_datum(
        fields: List[str], redaction: str, message: str, separator: str
        ) -> str:
    """ Filter sensitive data from a message. """
    pattrn = r'(' + '|'.join(fields) + r')=([^' + re.escape(separator) + r']+)'
    return re.sub(
            pattrn, lambda match: f'{match.group(1)}={redaction}', message)


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


def get_db() -> connection.MySQLConnection:
    """
    Get a connection to the MySQL database.

    This function retrieves the necessary credentials from
    environment variables and establishes a connection
    to the MySQL database using the provided credentials.

    Returns:
        connection.MySQLConnection: A connection to the MySQL database.
    """

    db_username = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    db_password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    db_host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')

    connection = mysql.connector.connect(
        user=db_username,
        password=db_password,
        host=db_host,
        database=db_name
    )

    return connection


def main() -> None:
    """
    Main function that retrieves user data from the database and logs it.

    This function retrieves user data from the database,
    constructs a log message for each user, and logs
    the message using the logger.
    """

    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM users;')

    logger = get_logger()

    for row in cursor:
        message = (
            f'name={row[0]}; email={row[1]}; phone={row[2]}; ssn={row[3]}; '
            f'password={row[4]}; ip={row[5]}; last_login={row[6]}; '
            f'user_agent={row[7]};'
        )
        logger.info(message)

    cursor.close()
    db.close()


if __name__ == '__main__':
    main()
