from __future__ import annotations

import functools
import os
import hashlib

from models.base.document import IndexedDocument
from models.base.field import Field


class User(IndexedDocument):
    """
    Base class for user with authentication mechanism
    """
    username = Field(primary_key=True)
    __salt = Field()
    __password_hash = Field()

    def __init__(self, username: str, password: str):
        salt = os.urandom(32)
        super().__init__(username=username,
                         _User__salt=salt,
                         _User__password_hash=self.__hash_password(password, salt))

    @staticmethod
    def __hash_password(password: str, salt: bytes) -> bytes:
        return hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)

    class InvalidPassword(Exception):
        pass

    def login(self, password: str) -> User:
        """
        Check if password is correct.
        Returns user instance if password is correct, raises InvalidPassword exception otherwise.
        :param password:
        :return:
        """
        if self.__hash_password(password, self.__salt) == self.__password_hash:
            return self
        else:
            raise User.InvalidPassword()

    def update_password(self, password: str) -> None:
        self.__password_hash = self.__hash_password(password, self.__salt)


def require_role(*roles: type):
    """
    Decorator for checking user role.
    Control permission to a shell session method by specifying required roles in the decorator.
    Example:
        @require_role(Admin)
        def create_volunteer(self, volunteer):
            ...
    Class owning the method must have an attribute 'user' of type User.
    A error message will be printed if the user is not an instance of the specified role.
    """

    def decorator_require_role(func):
        @functools.wraps(func)
        def wrapper_require_role(*args, **kwargs):
            session = args[0]
            if isinstance(session.user, roles):
                return func(*args, **kwargs)
            else:
                print('You do not have permission to perform this action.')

        return wrapper_require_role

    return decorator_require_role
