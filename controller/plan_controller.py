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

    TODO : once issue #38 is resolved, need to add exception for camps having the same name.
    """
    try:
        return Plan(name=plan_name, emergency_type=emergency_type, description=description,
                    geographical_area=geographical_area, camps=camps)
    except Plan.MissingCampsError as e:
        raise controller_error.ControllerError(str(e))


def list_plans() -> list:
    """
    List out all the plans.
    This would not be shown on the menu.
    """
    list_plan = Plan.all()
    return list_plan


def find_plan(plan_name: str) -> Plan:
    """
    Finds the relevant plan with a given plan name.
    """
    plan_document = Plan.find(key=plan_name)
    if isinstance(plan_document, Plan):
        return plan_document
    raise controller_error.ControllerError('Plan not found.')


def close_plan(plan: Plan):
    """
    Use find_plan in combination with this function when admin requests for a plan to be closed.
    Inputted plan will be changed to read-only by changing the __is_closed flag in Plan class.
    """
    plan.close()
    plan.save()


def find_camp(plan: Plan, camp_name: str) -> Camp:
    """
    Finds the relevant camp with a given camp name within the given plan.
    """
    camp_document = plan.camps.get(camp_name)
    if isinstance(camp_document, Camp):
        return camp_document
    raise controller_error.ControllerError('Camp not found.')
