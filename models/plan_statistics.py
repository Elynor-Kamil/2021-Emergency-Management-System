from models.base.document import Document, ReferenceDocumentsField
from models.camp import Camp
from models.refugee import Refugee
from models.volunteer import Volunteer
from models.plan import Plan
import math


plandict = {}
plan_statistics = {"camp_name": [info], "camp2": [info2]}

def find_volunteer(Camp):
    """
    Function to find the number of active volunteers at a camp.
    If a volunteer is not active then they will not be included in the count.
    """
    volunteer_count = 0
    for volunteer in Camp.volunteers:
        if availibility == true:
            volunteer_count += 1
    return volunteer_count


def find_refugee(Camp):
    """
    Function to find the number of refugees at a camp.
    Includes the count of both the head of family and the family members in a single count.
    """
    refugee_count = 0
    for refugee in Camp.refugees:
        refugee_count += refugee.num_of_family_member
    return refugee_count


def plan_statistics_function(plan):
    """
    Review the plan data for a specific plan and return each camp in a plan with total active volunteers
    and total refugees. Done as a dictionary
    """
    plan_statistics = {}
    for camp in plan.camps:
        num_of_volunteer = find_volunteer(camp)
        num_of_refugee = find_refugee(camp)
        plan_statistics[camp.name] = [num_of_volunteer, num_of_refugee]
        #calculateVolunteerNeeded(plan_statistics)
    return plan_statistics

def calculateVolunteerNeeded(plan_statistics):
    for camp in plan_statistics.values():
        num_of_volunteer, num_of_refugee = camp
        extra_volunteer_needed, remaining_volunteer = 0, 0
        ideal_volunteers_num = int(math.ceil(num_of_refugee / 20))
        if idealVolunteersNum < num_of_volunteer:
            remaining_volunteer = num_of_volunteer - ideal_volunteers_num
        elif num_of_volunteer < ideal_volunteers_num:
            extra_volunteer_needed = ideal_volunteers_num - num_of_volunteer
        camp.append(remaining_volunteer)
        camp.append(extra_volunteer_needed)
    return plan_statistics

#controller

def view_plan_statistics(Plan):
    """
    """
    for plan in Plan:
        print planInfo
        if plan.camp is not None:
            result = plan_statistics_function(plan)
            print result

    #convert it to string?




# Build unit tests - can import the unittest classes