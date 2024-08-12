#!/usr/bin/env python3
"""
This module contains the DB class for managing user data in an SQLite database.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from user import Base, User


class DB:
    """
    The DB class provides methods for interacting with the user database.
    """

    def __init__(self) -> None:
        """
        Initialize a new DB instance.
        """

        self._engine = create_engine("sqlite:///a.db")
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """
        Memoized session object.
        """

        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email, hashed_password) -> User:
        """
        Add a new user to the database.
        """

        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """
        Find a user in the database based on the provided arguments.
        """

        user = self._session.query(User).filter_by(**kwargs).first()

        if not user:
            raise NoResultFound("No user found with the provided arguments.")

        try:
            user = self._session.query(User).filter_by(**kwargs).first()

            if not user:
                raise NoResultFound(
                    "No user found with the provided arguments."
                    )

            return user
        except InvalidRequestError:
            raise InvalidRequestError("Invalid query arguments provided.")
