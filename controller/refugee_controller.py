###---- Manage Refugee Menu ----
from datetime import date
from enum import Enum
from typing import Type

from models.camp import Camp
from models.refugee import Refugee
from controller.controller_error import ControllerError


def list_medical_condition_types() -> Type[Enum]:
    """
    List all options for medical condition type.
    :return:
    """
    return Refugee.MedicalCondition()


def create_refugee(user_id: str,
                   firstname: str,
                   lastname: str,
                   camp: Camp,
                   num_of_family_member: int,
                   starting_date: date,
                   medical_condition_type: Refugee.MedicalCondition) -> Refugee:
    """
    Function to create and save refugee.
    """
    try:
        for plan in Plan.all():
            plan_name = str(plan.name)
            curr_plan = Plan.find(plan_name)
            if camp == curr_plan.camps:
                new_refugee = Refugee(user_id = user_id,
                                      firstname = firstname,
                                      lastname = lastname,
                                      num_of_family_member = num_of_family_member,
                                      starting_date = starting_date,
                                      medical_condition_type = medical_condition_type)
                camp.refugees.add(new_refugee)
                return new_refugee
    except:
        ControllerError("Invalid refugee profile. Please try again.")


def find_refugee(refugee_id: int) -> Refugee:
    """
    Function to find if refugee exists and returns the refugee class profile. Return None if no such refugee exist.
    """
    for plan in Plan.all():
        plan_name = str(plan.name)
        curr_plan = Plan.find(plan_name)
        for camp in curr_plan.camps:
            for refugee in camp.refugees:
                if refugee_id == refugee.user_id:
                    return refugee
    return None


def view_refugee(refugee: Refugee) -> str:
    """
    A function used by admin and volunteer.
    """

    # volunteer: 1. to view all refugees in same camp 2. to view one specific refugee in corresponding camp
    # admin: 1. to view all refugees as a whole/by plan/by camps 2. view one specific refugee restriction/free

    return str(refugee)
