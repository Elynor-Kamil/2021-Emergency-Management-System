from enum import Enum
from typing import Iterable, Type

from models.plan import Plan
from models.camp import Camp
from controller import controller_error


def list_emergency_types() -> Type[Enum]:
    """
    List all options for emergency type.
    """
    return Plan.EmergencyType


def create_camps(name: str) -> Camp:
    """
    Create new camp.
    """
    camp = Camp(name=name)
    return camp


def create_plan(plan_name: str, emergency_type: Plan.EmergencyType, description: str,
                geographical_area: str,
                camps: Iterable[Camp]) -> Plan:
    """
    Creates plan given relevant inputs.

    Note: once issue #38 is resolved, need to add exception for camps having the same name.
    """
    return Plan(name=plan_name, emergency_type=emergency_type, description=description,
                geographical_area=geographical_area, camps=camps)


def list_plans() -> list:
    """
    List out all the plans.
    This would not be shown on the menu.
    """
    list_plan = Plan.all()
    return list_plan


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
            num_of_volunteers, num_of_refugees, remaining_volunteers, extra_volunteers_needed = statistics_info[0], \
                                                                                                statistics_info[1], \
                                                                                                statistics_info[2], \
                                                                                                statistics_info[3]

            statistics += f"Camp name: {camp_name}\n" \
                          f"Number of volunteers: {num_of_volunteers}\n" \
                          f"Number of refugees: {num_of_refugees}\n" \
                          f"Number of remaining volunteers not needed: {remaining_volunteers}\n" \
                          f"Number of extra volunteers needed: {extra_volunteers_needed}\n\n"

        return plan_info + statistics


def find_plan(plan_name: str) -> Plan:
    """
    Finds the relevant plan with a given plan name.
    """
    plan_document = Plan.find(key=plan_name)
    if plan_document is not None:
        if isinstance(plan_document, Plan):
            return plan_document
    raise controller_error.ControllerError('message')


def close_plan(plan_document: Plan):
    """
    Use find_plan in combination with this function when admin requests for a plan to be closed.
    Inputted plan will be changed to read-only by changing the __is_closed flag in Plan class.
    """
    plan_document.close()
    plan_document.save()
