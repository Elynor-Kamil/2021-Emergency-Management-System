from __future__ import annotations

import os
import pickle
from typing import Union

from models.base.field import ReferenceDocumentsField
from models.base.meta_document import MetaDocument, MetaIndexedDocument


def persist(func):
    """
    Decorator for saving the document after the function call.
    """

    def wrapper_persist(*args, **kwargs):
        instance: Document = args[0]
        func(*args, **kwargs)
        instance.save()

    return wrapper_persist


class Document(metaclass=MetaDocument):
    """
    Base class for all documents.
    Directly subclass this class only for embedded documents.
    For root level documents (i.e. tables), use the IndexedDocument class.
    This class is only persisted when they are referenced by IndexedDocument instances.

    To define a document, subclass this class and define attributes as Fields.
    For example:

        class User(Document):
            username = Field(primary_key=True)
            password_hash = Field()

    The attributes are defined with the Field class so that helper function can analyze them.
    For example, a helper function verifies that only one primary key is defined.

    The __init__ method automatically set field names and values.
    for example, the above User class can be directly instantiated with the following:

        user = User(username='admin', password_hash='1321A7FE01')

    To customize class initialization, override the __init__ method. For example:

        def __init__(self, username, password):
            self.validate_username(username)
            password_hash = self.hash_password(password)
            super().__init__(username=username, password_hash=password_hash)

    After updating the document, call the save method to persist the change. For example:

        user.username = 'admin2'
        user.save()

    To delete the document, use the delete method. For example:

        user.delete()

    Deleting a document also automatically removes all references to it.
    """
    _initialised = False

    class PrimaryKeyNotDefinedError(Exception):
        def __init__(self, document):
            super().__init__(f"Primary key not defined for {document.__class__.__name__}")

    class PrimaryKeyNotSetError(Exception):
        def __init__(self, field_name):
            super().__init__(f"Primary key {field_name} not set")

    class ReferrerNotFound(Exception):
        def __init__(self, referrer_type=None, attribute_name=None):
            super().__init__(f"Instanced is not referenced by "
                             f"{attribute_name or 'any field'} in {referrer_type or 'Any type'}")

    @persist
    def __init__(self, **kwargs):
        """
        Initialize the document.
        All fields are assigned automatically.
        :param kwargs: value to each field
        """
        self._data = {}
        for field_name, field in self._fields.items():
            if field.primary_key and field_name not in kwargs:
                raise self.PrimaryKeyNotSetError(field_name)
            self.__setattr__(field_name, kwargs.get(field_name))
        self._initialised = True
        self._referenced_by: list[Document] = []

    def save(self) -> None:
        """
        Recursively call save on the root-level document
        """
        for referrer in self._referenced_by:
            referrer.save()

    def delete(self) -> None:
        """
        Remove all references to this document and persist the change.
        """
        for referrer in list(self._referenced_by):  # copy with list() to avoid issues with removing items
            referrer.__unlink_referee(self)
            referrer.save()

    @property
    def key(self):
        """
        The primary key value of the document.
        """
        return getattr(self, self._primary_key)

    def find_referred_by(self, referrer_type: type = None, field_name: str = None) -> Document:
        """
        Find the first document that references this document matching the criteria.
        ReferrerNotFound exception is raised if no referrer matching the criteria is found.
        :param referrer_type: optional type of the referrer as a criteria
        :param field_name: optional field name of the referrer where the instance is referred as a criteria
        :return: the first referrer matching the criteria
        """
        for referrer in self._referenced_by:
            if referrer_type is not None and not isinstance(referrer, referrer_type):
                continue
            if field_name is not None and not self in getattr(referrer, field_name):
                continue
            return referrer
        raise self.ReferrerNotFound(referrer_type, field_name)

    def __eq__(self, other):
        return self._data == other._data

    def _add_referrer(self, referer):
        if referer not in self._referenced_by:
            self._referenced_by.append(referer)

    def _remove_referrer(self, referer):
        if referer in self._referenced_by:
            self._referenced_by.remove(referer)

    def __unlink_referee(self, referee):
        for field_name, field in self._fields.items():
            if isinstance(field, ReferenceDocumentsField):
                documents = getattr(self, field_name)
                if referee in documents:
                    documents.remove(referee)
        self.save()

    def __str__(self):
        return f'{self.__class__.__name__}({self._data})'


class IndexedDocument(Document, metaclass=MetaIndexedDocument):
    """
    Base class for all root level documents, directly persisted to disk.
    A primary key must be defined to index all active documents.
    To define the primary key, define an attribute with:
    my_field = Field(primary=True)
    Documents are persisted as the index to all documents in this class.
    The default persistence path is data/{classname}
    to change the path, override the _persistence_path property.
    """

    def __init__(self, **kwargs):
        self.reload()
        if not self._primary_key:
            raise Document.PrimaryKeyNotDefinedError(self)
        super().__init__(**kwargs)

    @classmethod
    def reload(cls) -> None:
        """
        Reload the index from disk.
        """
        try:
            with open(cls._persistence_path, 'rb') as f:
                cls.__objects = pickle.load(f)
        except FileNotFoundError:
            cls.__objects = {}

    @classmethod
    def check_and_load_data(cls):
        """
        Check if the index is loaded, if not, load it.
        """
        if not getattr(cls, '__objects', None):
            cls.reload()

    def save(self) -> None:
        """
        Save all documents of the same type (i.e. the index) to disk.
        Also save all root-level documents referencing this document.
        """
        self.__class__.check_and_load_data()
        self.__class__.__objects[self.key] = self
        os.makedirs(os.path.dirname(self._persistence_path), exist_ok=True)
        with open(self._persistence_path, 'wb') as f:
            pickle.dump(self.__class__.__objects, f)

        # Also save to parent indices
        for persistence_base in self._persistence_bases:
            persistence_base.__save_child(self)
        super().save()

    @classmethod
    def __save_child(cls, child: Document) -> None:
        """
        Save a child document to the parent index.
        to be called from subclass.
        :param child: child instance to be saved
        """
        cls.check_and_load_data()
        cls.__objects[child.key] = child
        os.makedirs(os.path.dirname(cls._persistence_path), exist_ok=True)
        with open(cls._persistence_path, 'wb') as f:
            pickle.dump(cls.__objects, f)

    @classmethod
    def find(cls, key) -> Union[None, IndexedDocument]:
        """
        Find a document by its primary key.
        :param key: the primary key value
        :return: the document, or None if not found
        """
        cls.check_and_load_data()
        return cls.__objects.get(key)

    @classmethod
    def all(cls) -> list[IndexedDocument]:
        """
        Get all documents of this type.
        :return: a list of all documents
        """
        cls.check_and_load_data()
        return list(cls.__objects.values())

    def delete(self) -> None:
        """
        Remove the document from the index, all references to it, and persist the change.
        """
        self.__class__.check_and_load_data()
        del self.__class__.__objects[self.key]
        with open(self._persistence_path, 'wb') as f:
            pickle.dump(self.__class__.__objects, f)
        super().delete()

    @classmethod
    def delete_all(cls) -> None:
        """
        Remove all documents of this type and persist the change.
        """
        cls.check_and_load_data()
        for document in cls.all():
            super().delete(document)
        try:
            os.remove(cls._persistence_path)
        except FileNotFoundError:
            pass
        cls.__objects = {}

    def __str__(self):
        return f'{self.__class__.__name__}({self._primary_key}={self.key})'
