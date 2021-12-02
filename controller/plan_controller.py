from enum import Enum
from typing import Iterable

from models.plan import Plan
from models.camp import Camp
from models.plan_statistics import plan_statistics_function


###---- Manage Plan Menu ----
def manage_plan_menu():
    """
    Vanessa
    """
    pass


def list_emergency_types() -> Enum:
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
    plan_statistics = plan_statistics_function(plan)
    plan_name = str(plan.name)
    plan_info = f"Plan name: {plan_name}\n"
    statistics = ""

    for camp in plan_statistics.items():
        camp_name, statistics_info = camp[0], camp[1]
        num_of_refugees, num_of_volunteers, num_volunteers_vs_standard = statistics_info['num_of_refugees'], \
                                                                         statistics_info['num_of_volunteers'], \
                                                                         statistics_info['num_volunteers_vs_standard']

        statistics += f"Camp name: {camp_name}\n" \
                      f"Number of refugees: {num_of_refugees}\n" \
                      f"Number of volunteers: {num_of_volunteers}\n" \
                      f"Number of volunteers vs standard: {num_volunteers_vs_standard}\n\n"

    return plan_info + statistics


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

