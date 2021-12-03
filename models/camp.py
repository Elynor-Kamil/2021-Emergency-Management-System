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

    def count_volunteers(self) -> int:
        """
        Function to find the number of active volunteers at a camp. If a volunteer is not active then they will not be included in the count.
        """
        volunteer_count = sum([1 for volunteer in self.volunteers if volunteer.availability and volunteer.account_activated])
        return volunteer_count

    def count_refugees(self) -> int:
        """
        Function to find the number of refugees at a camp. Includes the count of both the head of family and the family members in a single count.
        """
        refugee_count = sum([refugee.num_of_family_member for refugee in self.refugees])
        return refugee_count

