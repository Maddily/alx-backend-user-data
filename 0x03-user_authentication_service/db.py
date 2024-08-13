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

    def add_user(self, email: str, hashed_password: str) -> User:
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

        try:
            user = self._session.query(User).filter_by(**kwargs).one()
            return user
        except NoResultFound:
            raise NoResultFound("No user found with the provided arguments.")
        except InvalidRequestError:
            raise InvalidRequestError("Invalid query arguments provided.")

    def update_user(self, user_id, **kwargs) -> None:
        """
        Update the attributes of a user.
        """

        user = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            if not hasattr(user, key):
                raise ValueError(
                    f"{key} is not an attribute of the User class"
                    )
            setattr(user, key, value)

        self._session.commit()
