from models.refugee import Refugee
from models.volunteer import Volunteer
from models.camp import Camp
from models.plan import Plan
from datetime import date
import math

def find_volunteers(Camp):
    """
    Function to find the number of active volunteers at a camp. If a volunteer is not active then they will not be included in the count.
    """
    volunteer_count = 0
    for volunteer in Camp.volunteers:
        if volunteer.availability == True and volunteer.account_activated == True:
            volunteer_count += 1
    return volunteer_count

def find_refugees(Camp):
    """
    Function to find the number of refugees at a camp. Includes the count of both the head of family and the family members in a single count.
    """
    refugee_count = 0
    for refugee in Camp.refugees:
        refugee_count += refugee.num_of_family_member
    return refugee_count

def plan_statistics_function(Plan):
    """
    Review the plan data for a specific plan and return each camp in a plan with total active volunteers and total refugees. Done as a dictionary.
    """
    plan_statistics = {}
    for camp in Plan.camps:
        num_of_volunteers = find_volunteers(camp)
        num_of_refugees = find_refugees(camp)
        plan_statistics[camp.name] = [num_of_volunteers, num_of_refugees]
        calculate_volunteer_needed(camp, plan_statistics)
    return plan_statistics

def calculate_volunteer_needed(Camp, plan_statistics):
    """
    Calculate the extra volunteers needed and remaining volunteers not needed for a camp by 1:20 number of volunteers and number of refugees ratio.
    """
    num_of_volunteers, num_of_refugees = plan_statistics[Camp.name]
    extra_volunteers_needed, remaining_volunteers = 0, 0
    ideal_volunteers_num = int(math.ceil(num_of_refugees / 20))
    if ideal_volunteers_num < num_of_volunteers:
        remaining_volunteers = num_of_volunteers - ideal_volunteers_num
    elif num_of_volunteers < ideal_volunteers_num:
        extra_volunteers_needed = ideal_volunteers_num - num_of_volunteers
    plan_statistics[Camp.name].append(remaining_volunteers)
    plan_statistics[Camp.name].append(extra_volunteers_needed)



