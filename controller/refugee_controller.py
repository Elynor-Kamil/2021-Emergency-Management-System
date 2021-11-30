###---- Manage Refugee Menu ----
from datetime import date

from models.camp import Camp
from models.refugee import Refugee


def list_medical_condition_types() -> dict:
    """
    Dictionary of medical condition type.
    :return:
    """
    medical_condition_types = {'Cancer': Refugee.MedicalCondition.CANCER,
                              'Chronic kidney disease': Refugee.MedicalCondition.CHRONICKIDNEY,
                              'Chronic liver disease': Refugee.MedicalCondition.CHRONICLIVER,
                              'Chronic lung diseases': Refugee.MedicalCondition.CHRONICLUNG,
                              'Dementia or other neurological conditions': Refugee.MedicalCondition.DEMENTIA_OR_NEUROLOGICAL,
                              'Diabetes': Refugee.MedicalCondition.DIABETES,
                              'Down Syndrome': Refugee.MedicalCondition.DOWNSYNDROME,
                              'Heart conditions': Refugee.MedicalCondition.HEART,
                              'HIV infection': Refugee.MedicalCondition.HIV,
                              'Immunocompromised state': Refugee.MedicalCondition.IMMUNOCOMPROMISED,
                              'Mental health conditions': Refugee.MedicalCondition.MENTALHEALTH,
                              'Overweight and obesity': Refugee.MedicalCondition.OVERWEIGHT_OR_OBESITY,
                              'Pregnancy': Refugee.MedicalCondition.PREGNANCY,
                              'Sickle cell or thalassemia': Refugee.MedicalCondition.SICKLECELL_OR_THALASSEMIA,
                              'Smoking, current or former': Refugee.MedicalCondition.SMOKING,
                              'Solid organ or blood stem cell transplant': Refugee.MedicalCondition.TRANSPLANT,
                              'Stroke or cerebrovascular disease, which affects blood flow to the brain': Refugee.MedicalCondition.STROKE_OR_CEREBROVASCULAR,
                              'Substance use disorders': Refugee.MedicalCondition.SUBSTANCE_USE,
                              'Tuberculosis': Refugee.MedicalCondition.TUBERCULOSIS,
                              'Others': Refugee.MedicalCondition.OTHERS}
    return medical_condition_types


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
    new_refugee = Refugee(user_id = user_id,
                          firstname = firstname,
                          lastname = lastname,
                          num_of_family_member = num_of_family_member,
                          starting_date = starting_date,
                          medical_condition_type = medical_condition_type)
    camp.refugees.add(new_refugee)
    return new_refugee


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
