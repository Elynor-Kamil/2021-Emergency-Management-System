from models.base.document import Document, ReferenceDocumentsField
from models.camp import Camp
from models.refugee import Refugee
from models.volunteer import Volunteer
from models.plan import Plan


plandict = {}
plan_statistics = {"camp_name": [info], "camp2":[info2]}

def find_volunteer(camp):
    """Function to find the number of active volunteers at a camp"""
    volunteer_count = 0
    for volunteer in camp.Volunteers:
        if status != "deactivated":
            volunteer_count += 1
    return volunteer_count


def find_refugee(camp):
    refugee_count = 0
    for refugee in camp.Refugee:
        refugee_count += refugee.familyMemberNo
    return refugee_count


def plan_statistics_function(plandict):
    plan_statistics = {}
    for plan in plandict:
        for camp in plan.camp:
            num_of_Volunteer = find_volunteer(camp)
            num_of_refugee = find_refugee(camp)
            plan_statistics[camp.name] = [num_of_Volunteer, num_of_refugee]
    return plan_statistics


# Build unit tests - can import the unittest classes


