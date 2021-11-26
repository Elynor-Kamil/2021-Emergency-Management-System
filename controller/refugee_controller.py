###---- Manage Refugee Menu ----
from datetime import date

from models.camp import Camp
from models.refugee import Refugee


def create_refugee(firstname: str,
                   lastname: str,
                   camp: Camp,
                   num_of_family_member: int,
                   starting_date: date,
                   medical_condition_type: Refugee.MedicalCondition) -> Refugee:
    """
    Yingbo, Michelle
    A function used by admin and volunteer.
    """
    pass


def find_refugee(refugee_id: int) -> Refugee:
    """
    Yingbo, Michelle

    """
    pass


def view_refugee(refugee: Refugee) -> str:
    """
    Yingbo, Michelle
    A function used by admin and volunteer.
    """
    pass


def delete_refugee(refugee: Refugee) -> None:
    """
    Yingbo
    A function used by admin and volunteer.
    """
    pass
