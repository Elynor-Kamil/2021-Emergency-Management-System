from datetime import date, datetime
from enum import Enum
from typing import Iterable, Union
import math

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
    __is_closed = Field()
    __close_date = Field()
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
                         _Plan__close_date=None,
                         _Plan__is_closed=False,
                         camps=camps)

    @property
    def start_date(self) -> date:
        """
        Get the read-only start date of the plan.
        """
        return self.__start_date  # Name mangling to access private field

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

    def close(self):
        """
        Set __is_closed flag to be True if plan is closed.
        """
        self.__is_closed = True
        self.__close_date = datetime.today().date()
        self.save()

    @property
    def close_date(self) -> Union[date, None]:
        """
        Get the read only close date of the plan.
        It will return None if plan is not closed.
        """
        if self.__is_closed:
            return self.__close_date

    @property
    def is_closed(self) -> bool:
        """
        Get the read only status of the plan.
        """
        return self.__is_closed

    def plan_statistics_function(self):
        """
        Review the plan data and return each camp in the plan with total active volunteers and total refugees.
        :return: {'Camp': {'num_of_refugees': int, 'num_of_volunteers': int, 'num_volunteers_vs_standard': int}}
        """
        plan_statistics_dict = {}
        for camp in self.camps:
            num_of_volunteers = camp.count_volunteers()
            num_of_refugees = camp.count_refugees()
            num_volunteers_vs_standard = self.__find_num_of_volunteers_vs_ideal_volunteers_num(num_of_volunteers,
                                                                                               num_of_refugees)
            plan_statistics_dict[camp.name] = {'num_of_refugees': num_of_refugees,
                                               'num_of_volunteers': num_of_volunteers,
                                               'num_volunteers_vs_standard': num_volunteers_vs_standard}
        return plan_statistics_dict

    def __find_num_of_volunteers_vs_ideal_volunteers_num(self, num_of_volunteers, num_of_refugees) -> str:
        """
        Function to find number of volunteers:ideal number of volunteers ratio by ideal 1:20 number volunteer ratio.
        """
        TARGET_REFUGEE_VOLUNTEER_RATIO = 20
        ideal_volunteers_num = int(math.ceil(num_of_refugees / TARGET_REFUGEE_VOLUNTEER_RATIO))

        return f"{num_of_volunteers}:{ideal_volunteers_num}"
