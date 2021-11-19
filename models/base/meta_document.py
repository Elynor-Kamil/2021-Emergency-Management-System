import sys

from models.base.field import Field


class MetaDocument(type):
    """
    A metaclass for documents to register all fields and identify the primary key.
    """

    class MultiplePrimaryKeyError(Exception):
        def __init__(self):
            super().__init__(f"Only one primary key is allowed")

    def __new__(cls, name, bases, attrs):

        # Discover document fields
        doc_fields = {}
        primary_key = None
        for attr_name, attr_value in attrs.items():
            if not isinstance(attr_value, Field):
                continue
            attr_value.name = attr_name
            if attr_value.primary_key:
                if primary_key is not None:
                    raise cls.MultiplePrimaryKeyError
                else:
                    primary_key = attr_name
            doc_fields[attr_name] = attr_value
        attrs["_primary_key"] = primary_key
        attrs["_fields"] = doc_fields

        return super().__new__(cls, name, bases, attrs)


class MetaIndexedDocument(MetaDocument):
    """
    A metaclass for IndexedDocument to load the index at class definition.
    """

    def __new__(cls, name, bases, attrs):
        if "_persistence_path" not in attrs:
            attrs["_persistence_path"] = f'data/{name}'

        new_class = super().__new__(cls, name, bases, attrs)
        sys.modules[new_class.__module__].__dict__[name] = new_class
        new_class.reload()
        return new_class
