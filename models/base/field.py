from typing import Sequence


class Field:
    name = None  # Set by Document.__new__()
    primary_key = False

    class PrimaryKeyMutationError(Exception):
        def __init__(self):
            super().__init__("Primary key cannot be mutated")

    class InvalidValueError(Exception):
        def __init__(self, value):
            super().__init__(f"Invalid value {value}")

    def __init__(self, primary_key=False):
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
    class MultipleTypeError(Exception):
        def __init__(self):
            super().__init__('Multiple types passed to set. Only homogeneous sets are supported. ')

    class UnindexedReferenceError(Exception):
        def __init__(self):
            super().__init__('Operation not supported for references to documents without primary keys')

    def __init__(self, references: Sequence, owner=None):
        self.__type = None
        self.__references = []
        self.__index = {}
        self.__primary_key = None
        self.__owner = owner
        self.__add_references(*references)

    def _with_owner(self, owner):
        self.__owner = owner
        for reference in self.__references:
            reference._referrers.append(owner)
        return self

    def __add_references(self, *references):
        if len(references) > 0:
            if not all(type(reference) == (self.__type or type(references[0])) for reference in references):
                raise self.MultipleTypeError()
            if not self.__references:  # First references
                self.__type = type(references[0])
                self.__primary_key = self.__type._primary_key
            if self.__primary_key:
                self.__index.update({reference._data[self.__primary_key]: reference for reference in references})
            self.__references += references
            for reference in references:
                reference.add_referrer(self.__owner)

    def __iter__(self):
        return iter(self.__references)

    def add(self, *references):
        self.__add_references(*references)

    def remove(self, item):
        if self.__primary_key:
            self.__index.pop(item.key)
        i = self.__references.index(item)
        self.__references[i]._referrers.remove(self.__owner)
        self.__references.remove(item)

    def get(self, key):
        if not self.__primary_key:
            raise self.UnindexedReferenceError()
        return self.__index.get(key)

    def __contains__(self, item):
        return item in self.__references

    def __getitem__(self, item):
        if not self.__primary_key:
            raise self.UnindexedReferenceError()
        return self.__index[item]

    def __delitem__(self, key):
        if not self.__primary_key:
            raise self.UnindexedReferenceError()
        item = self.__index[key]
        self.__references.remove(item)
        del self.__index[key]
        item._referrers.discard(self.__owner)

    def __len__(self):
        return len(self.__references)

    def __str__(self):
        return f'{self.__class__.__name__}[{",".join([str(item) for item in self.__references])}]'


class ReferenceDocumentsField(Field):

    def __set__(self, instance, value):
        if isinstance(value, ReferenceSet):
            super().__set__(instance, value._with_owner(instance))
        else:
            try:
                for doc in value:
                    assert hasattr(doc, "_referrers")
            except (TypeError, AssertionError):
                raise self.InvalidValueError(value)
            super().__set__(instance, ReferenceSet(value, instance))

    def __get__(self, instance, owner):
        obj = super().__get__(instance, owner)
        if isinstance(obj, ReferenceSet):
            return obj._with_owner(instance)
        else:
            return obj
