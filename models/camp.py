from models.base.document import Document
from models.base.field import Field


class Camp(Document):
    name = Field(primary_key=True)

    def __str__(self):
        return self.name
