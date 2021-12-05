from __future__ import annotations

from typing import Sequence, Iterator, TYPE_CHECKING, Union, Iterable, Any, Type

if TYPE_CHECKING:
    from models.base.document import Document


class Field:
    """
    A placeholder for all data attributes in a class.
    The class is created for helper functions like checking for multiple primary keys.
    """
    name = None  # Set by Document.__new__()
    primary_key = False

    class PrimaryKeyMutationError(Exception):
        def __init__(self):
            super().__init__("Primary key cannot be mutated")

    class InvalidValueError(Exception):
        def __init__(self, value):
            super().__init__(f"Invalid value {value}")

    def __init__(self, primary_key=False):
        """
        Declare a data attribute.
        :param primary_key: whether this attribute is a primary key. Only one primary key per class is allowed.
        """
        self.primary_key = primary_key

    def __get__(self, instance, owner):
        if instance is None:
            return self

        # Get value from document instance if available
        return instance._data.get(self.name)

    def __set__(self, instance, value):
        if self.primary_key and instance._initialised:
            raise self.PrimaryKeyMutationError()
        else:
            instance._data[self.name] = value


class ReferenceSet:
    """
    A container for references to other documents.
    The class maintains a two-way binding between the referenced documents and the referencing documents.
    Additionally, the references are automatically indexed if they have a primary key.
    """

    class MultipleTypeError(Exception):
        def __init__(self):
            super().__init__('Multiple types passed to set. Only homogeneous sets are supported. ')

    class UnindexedReferenceError(Exception):
        def __init__(self):
            super().__init__('Operation not supported for references to documents without primary keys')

    def __init__(self, references: Sequence[Document], data_type: Type[Document] = None, owner: Document = None):
        self.__ref_documents: list[Document] = []  # Actual references
        self.data_type = data_type  # Type of the references, updated in the first add if not provided.
        # Primary key name of the referenced documents, updated in the first add if data_type not provided.
        self.__primary_key = self.data_type._primary_key if self.data_type else None
        self.__index: dict[Any, Document] = {}  # Index of the references, if they have a primary key.
        self.__owner = owner  # The document that owns this reference set. Must be set before editing references.
        self.__add_references(*references)

    def _with_owner(self, owner: Document) -> ReferenceSet:
        """
        Update the owner of this reference set, so that references can be updated.
        """
        self.__owner = owner
        for document in self.__ref_documents:
            if getattr(document, '_add_referrer', None) is not None:
                document._add_referrer(owner)
        return self

    def __add_references(self, *documents: Document) -> None:
        """
        Add references to the reference set.
        :param documents: Documents instances of the same type
        """
        if len(documents) == 0:
            return
        if not all(type(document) == (self.data_type or type(documents[0])) for document in documents):
            raise self.MultipleTypeError()
        if not self.data_type:  # set type if not set yet
            self.data_type = type(documents[0])
            self.__primary_key = self.data_type._primary_key
        for document in documents:
            if document not in self.__ref_documents:
                self.__ref_documents.append(document)
            if self.__primary_key:
                key_value = getattr(document, self.__primary_key)
                if key_value in self.__index:
                    from models.base.document import Document
                    raise Document.DuplicateKeyError(self.__primary_key, key_value)
                self.__index[key_value] = document
        for reference in documents:
            reference._add_referrer(self.__owner)

    def __iter__(self) -> Iterator[Document]:
        return iter(self.__ref_documents)

    def add(self, *references) -> None:
        """
        Add documents to the reference set. Changes are automatically saved.
        :param references: documents of the same type
        """
        self.__add_references(*references)
        self.__owner.save()

    def remove(self, item) -> None:
        """
        Remove a referenced document from the reference set. Changes are automatically saved.
        A ValueError is raised if the item is not in the reference set.
        :param item: a document existing in the reference set
        """
        if self.__primary_key:
            self.__index.pop(item.key)
        i = self.__ref_documents.index(item)
        self.__ref_documents[i]._remove_referrer(self.__owner)
        self.__ref_documents[i].save()
        self.__ref_documents.remove(item)
        self.__owner.save()

    def get(self, key) -> Union[Document, None]:
        """
        Get a document from the reference set by its primary key.
        UnindexedReferenceError is raised if the document type does not have a primary key.
        :param key: the primary key of the document
        :return: the document with the given primary key, or None if it does not exist
        """
        if not self.__primary_key:
            raise self.UnindexedReferenceError()
        return self.__index.get(key)

    def __contains__(self, item):
        return item in self.__ref_documents

    def __getitem__(self, item):
        if not self.__primary_key:
            raise self.UnindexedReferenceError()
        return self.__index[item]

    def __delitem__(self, key):
        if not self.__primary_key:
            raise self.UnindexedReferenceError()
        item = self.__index[key]
        self.__ref_documents.remove(item)
        del self.__index[key]
        item._remove_referrer(self.__owner)
        item.save()
        self.__owner.save()

    def __len__(self):
        return len(self.__ref_documents)

    def __str__(self):
        return f'{self.__class__.__name__}[{",".join([str(item) for item in self.__ref_documents])}]'


class ReferenceDocumentsField(Field):
    """
    A field that references a set of documents.
    This field maintains a two-way binding between the owner and the referenced documents.
    """

    def __init__(self, data_type: Type[Document] = None, **kwargs):
        """
        :param data_type: the type of the referenced documents
        """
        super().__init__(**kwargs)
        self._data_type = data_type

    def __set__(self, instance, value: Union[ReferenceSet, Sequence[Document]]):
        if isinstance(value, ReferenceSet):
            if value.data_type is None:
                value.data_type = self._data_type
            elif value.data_type != self._data_type:
                raise ReferenceSet.MultipleTypeError
            super().__set__(instance, value._with_owner(instance))
        else:
            value = value or []  # avoid TypeError when initialising document with optional reference field
            try:
                for doc in value:
                    assert hasattr(doc, "_referenced_by")
            except (TypeError, AssertionError):
                raise self.InvalidValueError(value)
            if instance._initialised:
                for document in self.__get__(instance, instance.__class__):
                    if getattr(document, "_referenced_by", None) is not None:
                        document._remove_referrer(instance)  # Remove the old references
            super().__set__(instance, ReferenceSet(value, self._data_type, instance))

    def __get__(self, instance, owner):
        obj = super().__get__(instance, owner)
        return obj._with_owner(instance)
