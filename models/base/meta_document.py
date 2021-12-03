import sys

from models.base.field import Field


class MetaDocument(type):
    """
    A metaclass for documents to register all fields and identify the primary key.
    """

    class MultiplePrimaryKeyError(Exception):
        def __init__(self):
            super().__init__("Only one primary key is allowed")

    def __new__(cls, name, bases, attrs):

        # Discover document fields
        doc_fields = {}

        # Add all fields from superclasses
        for base in bases:
            if hasattr(base, '_fields'):
                for field_name, field in base._fields.items():
                    doc_fields[field_name] = field

        primary_key = None

        # set primary key from parent class
        for base in bases:
            if hasattr(base, '_primary_key'):
                if primary_key is not None:
                    raise MetaDocument.MultiplePrimaryKeyError()
                primary_key = base._primary_key

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

        # record persistence bases, so that subclasses are also persisted to parent classes
        persistence_bases = []
        for base in bases:
            if hasattr(base, '_persistence_path'):
                persistence_bases.append(base)
        attrs["_persistence_bases"] = persistence_bases

        new_class = super().__new__(cls, name, bases, attrs)
        return new_class
