from __future__ import annotations

import os
import pickle
import sys
from typing import Union

from models.base.field import ReferenceDocumentsField, ReferenceSet
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
        Save all documents associated with this document.
        """
        self._persist()
        self._save_referrers()  # Recursively look for root level documents and save them.
        self._save_referees()  # Also save all documents that this document references.

    def _persist(self) -> None:
        """
        By default, documents are not persisted. To be overridden by subclasses.
        """
        return

    def _save_referrers(self) -> None:
        """
        Recursively call save on the root-level document
        """
        for referrer in self._referenced_by:
            referrer._persist()
            referrer._save_referrers()

    def _save_referees(self) -> None:
        """
        Recursively save all referees.
        """
        for field_name, field in self._fields.items():
            if isinstance(field, ReferenceDocumentsField):
                for referee in getattr(self, field_name):
                    referee._persist()
                    referee._save_referees()

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
        if not isinstance(other, self.__class__):
            return False
        return self._data == other._data

    def _add_referrer(self, referrer):
        if referrer not in self._referenced_by:
            self._referenced_by.append(referrer)

    def _remove_referrer(self, referrer):
        if referrer in self._referenced_by:
            self._referenced_by.remove(referrer)

    def __unlink_referee(self, referee):
        for field_name, field in self._fields.items():
            if isinstance(field, ReferenceDocumentsField):
                documents = getattr(self, field_name)
                if referee in documents:
                    documents.remove(referee)
        self.save()

    def _get_root_document(self):
        """
        Get the root-level document.
        """
        for referrer in self._referenced_by:
            root = referrer._get_root_document()
            if root is not None:
                return root

    def __str__(self):
        return f'{self.__class__.__name__}({self._data})'

    def __getstate__(self):
        """
        Customise pickling: referrers are not pickled to avoid circular references.
        Instead, root-level documents of the referrers are marked and loaded while unpickling.
        referrer pointers are relinked by loading the referrer indices.
        """
        state = self.__dict__.copy()
        referrer_roots = set()
        for referrer in self._referenced_by:
            root = referrer._get_root_document()
            referrer_roots.add((root.__module__, getattr(root.__class__, '__qualname__', root.__class__.__name__)))
        state['_referrer_roots'] = referrer_roots
        state['_referenced_by'] = []
        return state


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

    __objects = None

    class Pickler(pickle.Pickler):
        """
        Custom pickler to persist references to other IndexedDocuments.
        """

        def __init__(self, file, base_class):
            super().__init__(file)
            self.base_class = base_class

        def persistent_id(self, obj):
            if not isinstance(obj, self.base_class) and isinstance(obj, IndexedDocument):
                return obj.__module__, getattr(obj.__class__, '__qualname__', obj.__class__.__name__), obj.key
            else:
                return None

    class Unpickler(pickle.Unpickler):
        """
        Custom unpickler to restore references to other IndexedDocuments.
        """

        def persistent_load(self, pid):
            module, classname, key = pid
            return IndexedDocument.DeferredReference(module, classname, key)

    class DeferredReference:
        """
        A reference to an IndexedDocument that is not yet loaded to avoid circular references.
        These are restored after loading the whole index.
        """

        def __init__(self, module, classname, key):
            self.module = module
            self.classname = classname
            self.key = key

        def restore(self):
            """
            Restore the referenced document.
            """
            __import__(self.module)
            index = pickle._getattribute(sys.modules[self.module], self.classname)[0]
            return index.find(self.key)

    @persist
    def __init__(self, **kwargs):
        self.__class__.check_and_load_data()
        if not self._primary_key:
            raise Document.PrimaryKeyNotDefinedError(self)
        super().__init__(**kwargs)
        self.__class__.__objects[self.key] = self

        # Also save to parent indices
        for persistence_base in self._persistence_bases:
            persistence_base.__index_subclass_add(self)
            persistence_base._persist()

    @classmethod
    def reload(cls) -> None:
        """
        Reload the index from disk.
        """
        try:
            with open(cls._persistence_path, 'rb') as f:
                cls.__objects = cls.Unpickler(f).load()
                for key in cls.__objects:
                    # Restore deferred references to referees
                    cls.__objects[key] = cls.__restore_reference(cls.__objects[key])
                    # Load all indices referring to this document to relink referrers
                    cls.__restore_referrer(cls.__objects[key])
        except FileNotFoundError:
            cls.__objects = {}

    @classmethod
    def __restore_reference(cls, value):
        """
        Restore deferred references to other IndexedDocuments recursively.
        :param value: a DeferredReference, Document, ReferenceSet, or field value
        :return: the restored value, or None if it was a field value
        """
        if isinstance(value, cls.DeferredReference):
            return value.restore()
        elif isinstance(value, Document):
            for field_name, field in value._fields.items():
                restored_field = cls.__restore_reference(getattr(value, field_name))
                if restored_field is not None:
                    setattr(value, field_name, restored_field)
            return value
        elif isinstance(value, ReferenceSet):
            return [cls.__restore_reference(doc) for doc in value]
        else:
            return None

    @classmethod
    def __restore_referrer(cls, obj) -> None:
        """
        Load all indices referring to this document to relink referrers.
        :param obj: an unpickled IndexedDocument instance
        """
        if getattr(obj, '_referrer_roots', None):
            for mod, classname in obj._referrer_roots:
                __import__(mod)
                index = pickle._getattribute(sys.modules[mod], classname)[0]
                index.check_and_load_data()
            delattr(obj, '_referrer_roots')

    @classmethod
    def check_and_load_data(cls):
        """
        Check if the index is loaded, if not, load it.
        """
        if cls.__objects is None:
            cls.reload()

    @classmethod
    def _persist(cls) -> None:
        """
        Save all documents of the same type (i.e. the index) to disk.
        If the class is a subclass of IndexedDocument, also persist to parent indices.
        """
        cls.check_and_load_data()
        os.makedirs(os.path.dirname(cls._persistence_path), exist_ok=True)
        with open(cls._persistence_path, 'wb') as f:
            cls.Pickler(f, cls).dump(cls.__objects)

    def _get_root_document(self):
        return self

    @classmethod
    def __index_subclass_add(cls, child: Document) -> None:
        """
        Save a subclass instance to the index of the parent (this) class.
        To be called from the __init__ method of a subclass of another IndexedDocument,
        such as to replace instances in the index of the parent class with instances of the subclass.
        :param child: child instance to be added
        """
        cls.check_and_load_data()
        cls.__objects[child.key] = child


    @classmethod
    def __index_subclass_remove(cls, child: Document) -> None:
        """
        Remove a subclass instance from the index of the parent (this) class.
        To be called from the delete method of a subclass of another IndexedDocument,
        :param child: child instance to be deleted
        """
        cls.check_and_load_data()
        del cls.__objects[child.key]

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
        self._persist()
        # Also save to parent indices
        for persistence_base in self._persistence_bases:
            persistence_base.__index_subclass_remove(self)
            persistence_base._persist()
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
