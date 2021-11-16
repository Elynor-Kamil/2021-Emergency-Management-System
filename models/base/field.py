class Field:
    name = None  # Set by Document.__new__()
    primary_key = False

    class PrimaryKeyMutationError(Exception):
        def __init__(self):
            super().__init__("Primary key cannot be mutated")

    class PrimaryKeyNotSetError(Exception):
        def __init__(self, field_name):
            super().__init__(f"Primary key {field_name} not set")

    class MultiplePrimaryKeyError(Exception):
        def __init__(self):
            super().__init__(f"Only one primary key is allowed")

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
