import abc

from models.base.field import Field


class MetaDocument(abc.ABCMeta):
    class MultiplePrimaryKeyError(Exception):
        def __init__(self):
            super().__init__(f"Only one primary key is allowed")

    def __new__(mcs, name, bases, attrs):

        # Discover document fields
        doc_fields = {}
        primary_key = None
        for attr_name, attr_value in attrs.items():
            if not isinstance(attr_value, Field):
                continue
            attr_value.name = attr_name
            if attr_value.primary_key:
                if primary_key is not None:
                    raise Field.MultiplePrimaryKeyError
                else:
                    primary_key = attr_name
            doc_fields[attr_name] = attr_value
        attrs["_primary_key"] = primary_key
        attrs["_fields"] = doc_fields

        return super().__new__(mcs, name, bases, attrs)
