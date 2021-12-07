from datetime import date
from enum import Enum
from typing import Type, Iterable

from controller.controller_error import ControllerError
from models.camp import Camp
from models.plan import Plan
from models.refugee import Refugee


def list_medical_condition_types() -> Type[Enum]:
    """
    List all options for medical condition type.
    """
    return Refugee.MedicalCondition


def create_refugee(firstname: str,
                   lastname: str,
                   camp: Camp,
                   num_of_family_member: int,
                   starting_date: date,
                   medical_condition_type: Iterable[Refugee.MedicalCondition]) -> Refugee:
    """
    Function to create and save refugee data.
    """
    if camp.plan.is_closed:
        raise ControllerError(f"Plan '{camp.plan.name}' of the camp '{camp.name}' is closed")
    try:
        new_refugee = Refugee(firstname=firstname,
                              lastname=lastname,
                              num_of_family_member=num_of_family_member,
                              starting_date=starting_date,
                              medical_condition_type=medical_condition_type)
        camp.refugees.add(new_refugee)
        return new_refugee
    except (Refugee.InvalidNameException,
            Refugee.InvalidNumOfFamilyMemberException,
            Refugee.InvalidStartingDateException,
            Refugee.InvalidCampException) as e:
        raise ControllerError(str(e))


def find_refugee(refugee_id: int) -> Refugee:
    """
    Function to find if refugee exists and returns the refugee class profile. Raise error if no such refugee, camp and plan exist .
    """
    for plan in Plan.all():
        for camp in plan.camps:
            refugee = camp.refugees.get(refugee_id)
            if refugee:
                return refugee
    raise ControllerError(f"Invalid refugee_id: {refugee_id}. The refugee is not found.")


def view_refugee(refugee: Refugee) -> str:
    """
    Function to be used by admin and volunteer to return refugee specified as a string.
    """
    return str(refugee)
