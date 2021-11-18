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
    start_date = Field()
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

    def __init__(self,
                 name: str,
                 emergency_type: EmergencyType,
                 description: str,
                 geographical_area: str,
                 start_date: date,
                 camps: Iterable[Camp]):
        """
        Initialize a new plan.
        :param name: name of the plan
        :param emergency_type: type of emergency, one of the predefined types
        :param description: description of the plan
        :param geographical_area: geographical area affected by the emergency
        :param start_date: start date of the plan
        :param camps: camps to be included in the plan
        """
        self.__check_start_date(start_date)
        if not camps:
            raise self.MissingCampsError()
        super().__init__(name=name,
                         emergency=emergency_type,
                         description=description,
                         geographical_area=geographical_area,
                         start_date=start_date,
                         camps=camps)

    def __str__(self):
        return f"Plan '{self.name}'"

    def open_camps(self, *camps: Camp) -> None:
        """
        Open one or more camps.
        """
        self.camps.add(*camps)
        self.save()

    def close_camps(self, *camps: Camp) -> None:
        """
        Close one or more camps.
        """
        for camp in camps:
            self.camps.remove(camp)
        if len(self.camps) == 0:
            self.reload()
            raise self.MissingCampsError()
        else:
            self.save()

    class PastStartDateException(Exception):
        """
        Exception raised when start date entered is in the past.
        """

        def __init__(self):
            super().__init__('Start date is in the past. Please enter a valid start date.')

    def __check_start_date(self, start_date: date) -> None:
        """
        Validate start date. PastStartDateException is raised if start date is in the past.
        """
        today = datetime.today().date()
        if start_date < today:
            raise self.PastStartDateException()
