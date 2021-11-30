from enum import Enum
from typing import Iterable

from models.plan import Plan
from models.camp import Camp


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
    for plan in Plan.all():
        plan_statistics = plan_statistics_function(plan)
        plan_name = plan.name

        plan_info = f"Plan name: {plan_name}\n"
        statistics = ""

        # {"camp1":[1, 2, 3, 4], "camp2":[6, 7, 8, 9]}
        for camp in plan_statistics.items():
            camp_name, statistics_info = camp[0], camp[1]
            num_of_volunteers, num_of_refugees, remaining_volunteers, extra_volunteers_needed = statistics_info[0], statistics_info[1], statistics_info[2], statistics_info[3]

            statistics += f"Camp name: {camp_name}\n" \
                          f"Number of volunteers: {num_of_volunteers}\n" \
                          f"Number of refugees: {num_of_refugees}\n" \
                          f"Number of remaining volunteers not needed: {remaining_volunteers}\n" \
                          f"Number of extra volunteers needed: {extra_volunteers_needed}\n\n"

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
