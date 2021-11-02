from collections import Iterable
from datetime import date
from enum import Enum

from models.camp import Camp


class Plan:
    class EmergencyType(Enum):
        EARTHQUAKE = 'earthquake'
        FIRE = 'fire'
        TSUNAMI = 'tsunami'
        STORM = 'storm'

    def __init__(self,
                 name: str,
                 emergency_type: EmergencyType,
                 description: str,
                 geographical_area: str,
                 start_date: date,
                 camps: Iterable[Camp] = None):
        self.name = name
        self.emergency_type = emergency_type
        self.description = description
        self.geographical_area = geographical_area
        self.start_date = start_date
        self.camps: set[Camp] = set(camps) or set()

    def __str__(self):
        return f'Plan "{self.name}"'

    def open_camps(self, *camps):
        self.camps.update(*camps)

    def close_camps(self, *camps):
        self.camps.difference_update(*camps)
