###---- Manage Refugee Menu ----
from datetime import date
from enum import Enum
from typing import Type
from models.plan import Plan
from models.camp import Camp
from models.refugee import Refugee
from controller.controller_error import ControllerError


def list_medical_condition_types() -> Type[Enum]:
    """
    List all options for medical condition type.
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
    Function to create and save refugee data.
    """
    try:
        for plan in Plan.all():
            plan_name = str(plan.name)
            curr_plan = Plan.find(plan_name)
            if camp in curr_plan.camps:
                new_refugee = Refugee(firstname = firstname,
                                      lastname = lastname,
                                      num_of_family_member = num_of_family_member,
                                      starting_date = starting_date,
                                      medical_condition_type = medical_condition_type)
                camp.refugees.add(new_refugee)
                return new_refugee
    except Refugee.InvalidNameException:
        raise ControllerError(f"Invalid refugee name: {firstname, lastname}. Firstname and lastname should be string.")
    except Refugee.InvalidNumOfFamilyMemberException:
        raise ControllerError(f"Invalid number of family member: {num_of_family_member}. Number of family member should be a positive integer.")
    except Refugee.InvalidStartingDateException:
        raise ControllerError(f"Invalid starting date: {starting_date}. Starting date should before today.")
    except Refugee.InvalidCampException:
        raise ControllerError(f"Invalid camp: {camp}. The camp is not found.")


def find_refugee(refugee_id: int) -> Refugee:
    """
    Function to find if refugee exists and returns the refugee class profile. Return None if no such refugee exist.
    """
    try:
        for plan in Plan.all():
            plan_name = str(plan.name)
            curr_plan = Plan.find(plan_name)
            for camp in curr_plan.camps:
                for refugee in camp.refugees:
                    if refugee_id == refugee.user_id:
                        return refugee
    except:
        raise ControllerError(f"Invalid refugee refugee_id: {refugee_id}. The refugee is not found.")



def view_refugee(refugee: Refugee) -> str:
    """
    Function to be used by admin and volunteer to return refugee specified as a string.
    """
    return str(refugee)