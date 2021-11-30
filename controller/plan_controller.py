from enum import Enum
from typing import Iterable, Type

from models.plan import Plan
from models.camp import Camp


def list_emergency_types() -> Type[Enum]:
    """
    List all options for emergency type.
    """
    pass


def create_camps(name: str) -> Camp:
    pass


def create_plan(plan_name: str, emergency_type: Plan.EmergencyType, description: str,
                geographical_area: str,
                camps: Iterable[Camp]) -> Plan:
    """
    Shalaka, Elynor
    """
    pass


def list_plans() -> list:
    """
    Shalaka, Elynor
    List out all the plans.
    This would not be shown on the menu.
    """
    pass


def view_plan_statistics(plan: Plan) -> str:
    """
    Display plan statistics.
    """
    pass


def find_plan(plan_name: str) -> Plan:
    """
    Shalaka, Elynor
    """
    pass


def close_plan(plan: Plan):
    """
    Shalaka, Elynor
    """
    pass
