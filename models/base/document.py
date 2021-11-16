import os
import pickle
from abc import ABC, abstractmethod

from models.base.field import Field
from models.base.meta_document import MetaDocument


def persist(func):
    def wrapper_persist(*args, **kwargs):
        instance: BaseDocument = args[0]
        func(*args, **kwargs)
        instance.save()

    return wrapper_persist


class BaseDocument(ABC, metaclass=MetaDocument):
    _initialised = False

    class PrimaryKeyNotDefinedError(Exception):
        def __init__(self, document):
            super().__init__(f"Primary key not defined for {document.__class__.__name__}")

    @persist
    def __init__(self, **kwargs):
        self._data = {}
        for field_name, field in self._fields.items():
            if field.primary_key and field_name not in kwargs:
                raise Field.PrimaryKeyNotSetError(field_name)
            self.__setattr__(field_name, kwargs.get(field_name))
        self._initialised = True
        self._referrers = []

    @abstractmethod
    def save(self):
        pass

    @property
    def key(self):
        return getattr(self, self._primary_key)

    def __eq__(self, other):
        return self._data == other._data

    def add_referrer(self, referer):
        if referer not in self._referrers:
            self._referrers.append(referer)

    def remove_referrer(self, referer):
        if referer in self._referrers:
            self._referrers.remove(referer)


class Document(BaseDocument):

    def __init__(self, **kwargs):
        if not self._primary_key:
            raise BaseDocument.PrimaryKeyNotDefinedError(self)
        super().__init__(**kwargs)

    @classmethod
    @property
    def persistence_path(cls) -> str:
        return f'data/{cls.__name__}'

    try:
        __objects = pickle.load(open(f'{persistence_path}.p', 'rb'))
    except FileNotFoundError:
        __objects = {}

    @classmethod
    def reload(cls):
        try:
            cls.__objects = pickle.load(open(f'{cls.persistence_path}', 'rb'))
        except FileNotFoundError:
            cls.__objects = {}

    def save(self):
        self.__class__.__objects[self.key] = self
        os.makedirs(os.path.dirname(self.persistence_path), exist_ok=True)
        pickle.dump(self.__class__.__objects, open(self.persistence_path, 'wb'))

    @classmethod
    def find(cls, key):
        return cls.__objects.get(key)

    @classmethod
    def all(cls):
        return cls.__objects.values()

    def delete(self):
        del self.__class__.__objects[self.key]
        pickle.dump(self.__class__.__objects, open(self.persistence_path, 'wb'))

    @classmethod
    def delete_all(cls):
        try:
            os.remove(cls.persistence_path)
        except FileNotFoundError:
            pass
        cls.__objects = {}

    def __str__(self):
        return f'{self.__class__.__name__}({self.key})'


class EmbeddedDocument(BaseDocument, metaclass=MetaDocument):
    parent = set()

    def save(self):
        for parent in self.parent:
            parent.save()

    # TODO: is delete possible for embedded documents?
