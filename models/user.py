from __future__ import annotations

import functools
import os
import hashlib


class User:
    """
    Base class for user with authentication mechanism
    """

    def __init__(self, username: str, password: str):
        self.username = username
        self.salt = os.urandom(32)
        self.__password_hash = self.__hash_password(password)

    def __hash_password(self, password: str) -> bytes:
        return hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), self.salt, 100000)

    class InvalidPassword(Exception):
        pass

    def login(self, password: str) -> User:
        """
        Check if password is correct.
        Returns user instance if password is correct, raises InvalidPassword exception otherwise.
        :param password:
        :return:
        """
        if self.__hash_password(password) == self.__password_hash:
            return self
        else:
            raise User.InvalidPassword()

    def update_password(self, password: str) -> None:
        self.__password_hash = self.__hash_password(password)


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
