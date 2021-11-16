from models.base.field import Field


class MetaDocument(type):

    def __new__(typ, name, bases, attrs):

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
        attrs["_fields"] = doc_fields
