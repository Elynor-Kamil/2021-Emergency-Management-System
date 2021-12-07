from enum import Enum
from typing import Iterable, Type

from models.base.document import Document
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
    try:
        camp = Camp(name=name)
        return camp
    except Camp.InvalidName as e:
        raise controller_error.ControllerError(str(e))


def create_plan(plan_name: str, emergency_type: Plan.EmergencyType, description: str,
                geographical_area: str,
                camps: Iterable[Camp]) -> Plan:
    """
    Creates plan given relevant inputs.
    """
    if Plan.find(key=plan_name) is not None:
        raise controller_error.ControllerError(f'Plan with name {plan_name} already exists.')
    try:
        return Plan(name=plan_name, emergency_type=emergency_type, description=description,
                    geographical_area=geographical_area, camps=camps)
    except (Plan.MissingCampsError, Plan.InvalidName) as e:
        raise controller_error.ControllerError(str(e))
    except Document.DuplicateKeyError:
        raise controller_error.ControllerError('Duplicate camp names are not allowed.')


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

    plan_statistics = plan.statistics()
    plan_name = str(plan.name)
    if plan.is_closed:
        plan_info = f"\nPlan name: '{plan_name}' (closed)\n" \
                    f"Close Date: {plan.close_date}\n"
    else:
        plan_info = f"\nPlan name: '{plan_name}'\n"

    statistics = ""

    for camp in plan_statistics.items():
        camp_name, statistics_info = camp[0], camp[1]
        num_of_refugees, num_of_volunteers, num_volunteers_vs_standard = statistics_info['num_of_refugees'], \
                                                                         statistics_info['num_of_volunteers'], \
                                                                         statistics_info['num_volunteers_vs_standard']

        statistics += f"Camp name: '{camp_name}'\n" \
                      f"Number of refugees: {num_of_refugees}\n" \
                      f"Number of volunteers: {num_of_volunteers}\n" \
                      f"VS recommended number of volunteers: {num_volunteers_vs_standard:+d}\n\n"

    return plan_info + statistics


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
    if plan.is_closed:
        raise controller_error.ControllerError(f"Plan '{plan.name}' is already closed.")
    else:
        plan.close()
        plan.save()


def find_camp(plan: Plan, camp_name: str) -> Camp:
    """
    Finds the relevant camp with a given camp name within the given plan.
    """
    camp = plan.camps.get(camp_name)
    if isinstance(camp, Camp):
        return camp
    raise controller_error.ControllerError('Camp not found.')
