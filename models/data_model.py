import os
import pickle
from abc import ABC, abstractmethod


def persist(func):
    def wrapper_persist(*args, **kwargs):
        instance: BaseModel = args[0]
        func(*args, **kwargs)
        instance.save()

    return wrapper_persist


class BaseModel(ABC):

    @abstractmethod
    def save(self):
        pass


class Document(BaseModel):
    __key = None

    @classmethod
    @property
    def persistence_path(cls) -> str:
        return f'data/{cls.__name__}'

    try:
        __objects = pickle.load(open(f'{persistence_path}.p', 'rb'))
    except FileNotFoundError:
        __objects = {}

    @persist
    def __init__(self, key):
        self.__key = key

    @property
    def key(self):
        return self.__key

    def save(self):
        self.__class__.__objects[self.key] = self
        os.makedirs(os.path.dirname(self.persistence_path), exist_ok=True)
        pickle.dump(self.__class__.__objects, open(self.persistence_path, 'wb'))

    def delete(self):
        del self.__class__.__objects[self.key]
        pickle.dump(self.__class__.__objects, open(self.persistence_path, 'wb'))

    @classmethod
    def find(cls, key):
        return cls.__objects.get(key)

    @classmethod
    def all(cls):
        return cls.__objects.values()

    @classmethod
    def reload(cls):
        try:
            cls.__objects = pickle.load(open(f'{cls.persistence_path}', 'rb'))
        except FileNotFoundError:
            cls.__objects = {}

    @classmethod
    def delete_all(cls):
        try:
            os.remove(cls.persistence_path)
        except FileNotFoundError:
            pass

    def __del__(self):
        self.delete()


class EmbeddedDocument(BaseModel):
    parent = set()

    def save(self):
        for parent in self.parent:
            parent.save()

    # TODO: is delete possible for embedded documents?
