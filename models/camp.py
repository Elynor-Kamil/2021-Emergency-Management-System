from models.base.document import Document
from models.base.field import Field, ReferenceDocumentsField
from models.refugee import Refugee
from models.volunteer import Volunteer


class Camp(Document):
    name = Field(primary_key=True)
    volunteers = ReferenceDocumentsField(data_type=Volunteer)
    refugees = ReferenceDocumentsField(data_type=Refugee)

    def __str__(self):
        return self.name

    @property
    def plan(self):
        from models.plan import Plan
        return self.find_referred_by(referrer_type=Plan)
