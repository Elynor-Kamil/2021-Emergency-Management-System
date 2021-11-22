from datetime import date, datetime
from enum import Enum
from typing import Iterable

from models.base.document import IndexedDocument
from models.base.field import Field, ReferenceDocumentsField
from models.camp import Camp


class Plan(IndexedDocument):
    """
    An emergency plan consisting of camps.
    """

    name = Field(primary_key=True)
    emergency = Field()
    description = Field()
    geographical_area = Field()
    __start_date = Field()
    camps = ReferenceDocumentsField(data_type=Camp)

    class EmergencyType(Enum):
        """
        Predefined types of emergencies supported by the system.
        """
        EARTHQUAKE = 'earthquake'
        FIRE = 'fire'
        TSUNAMI = 'tsunami'
        STORM = 'storm'
        PANDEMIC = 'pandemic'
        FLOOD = 'flood'
        OTHER = 'other'

    class MissingCampsError(Exception):
        """
        It is mandatory to supply at least one camp when you are creating an emergency plan.
        When no camps are provided, this exception will be raised.
        """

        def __init__(self):
            super().__init__("It is mandatory to provide at least one camp")

    class PastStartDateException(Exception):
        """
        Exception raised when start date entered is in the past.
        """

        def __init__(self):
            super().__init__('Start date is in the past. Please enter a valid start date.')

    class CampNotFoundError(Exception):
        """
        Exception raised when a camp is not found in the emergency plan.
        """

        def __init__(self, camp):
            super().__init__(f'Camp {camp} is not in the emergency plan.')

    def __init__(self,
                 name: str,
                 emergency_type: EmergencyType,
                 description: str,
                 geographical_area: str,
                 camps: Iterable[Camp]):
        """
        Initialize a new plan.
        :param name: name of the plan
        :param emergency_type: type of emergency, one of the predefined types
        :param description: description of the plan
        :param geographical_area: geographical area affected by the emergency
        :param camps: camps to be included in the plan
        """
        if not camps:
            raise self.MissingCampsError()
        super().__init__(name=name,
                         emergency=emergency_type,
                         description=description,
                         geographical_area=geographical_area,
                         _Plan__start_date=datetime.today().date(),
                         camps=camps)

    @property
    def start_date(self) -> date:
        """
        Get the read-only start date of the plan.
        """
        return self._Plan__start_date  # Name mangling to access private field

    def __str__(self):
        return f"Plan '{self.name}'"

    def open_camps(self, *camps: Camp) -> None:
        """
        Open one or more camps. Camps that are already in the plan are ignored.
        """
        self.camps.add(*camps)
        self.save()

    def close_camps(self, *camps: Camp) -> None:
        """
        Close one or more camps.
        MissingCampsError is raised if the call will close all camps in the plan.
        CampNotFoundError is raised if one or more camps are not found in the plan.
        """
        for camp in camps:
            if camp not in self.camps:
                raise self.CampNotFoundError(camp)
            self.camps.remove(camp)
        if len(self.camps) == 0:
            self.reload()
            raise self.MissingCampsError()
        else:
            self.save()

