from datetime import datetime
# from enum import Enum
from typing import Iterable

from models.plan import Plan
from models.camp import Camp
from models.base.document import IndexedDocument


# ---- Manage Plan Menu ----
def manage_plan_menu():
    """
    Vanessa
    """
    pass


def list_emergency_types():
    for emergency in Plan.EmergencyType:
        print(emergency)


list_emergency_types()


# Flag to Vanessa - need to add plan attribute to create_camps

def create_camps(camp_name: str, plan_name: str) -> None:
    """
    Add new camp to plan.
    """
    plan = find_plan(plan_name)
    camp = Camp(name=camp_name)
    plan.open_camps(camp)


def create_plan(name: str, emergency_type: Plan.EmergencyType, description: str,
                geographical_area: str,
                camps: Iterable[Camp]) -> Plan:
    """
    Creates plan given relevant inputs.
    """
    return Plan(name=name, emergency_type=emergency_type, description=description,
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
    pass


def find_plan(plan_name: str) -> IndexedDocument:
    """
    Finds the relevant plan with a given plan name.
    """
    plan_document = Plan.find(key=plan_name)
    return plan_document


def close_plan(plan_document: Plan):
    """
    Use find_plan in combination with this function when admin requests for a plan to be closed.
    Inputted plan will be changed to read-only by changing the __is_closed flag in Plan class.
    """
    Plan._Plan__close_date = datetime.today().date()
    return Plan.close(plan_document)
