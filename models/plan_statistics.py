from models.refugee import Refugee
from models.volunteer import Volunteer
from models.camp import Camp
from models.plan import Plan
from datetime import date
import math


def count_volunteers(Camp):
    """
    Function to find the number of active volunteers at a camp. If a volunteer is not active then they will not be included in the count.
    """
    volunteer_count = sum([1 for volunteer in Camp.volunteers if volunteer.availability and volunteer.account_activated])
    return volunteer_count


def count_refugees(Camp):
    """
    Function to find the number of refugees at a camp. Includes the count of both the head of family and the family members in a single count.
    """
    refugee_count = sum([refugee.num_of_family_member for refugee in Camp.refugees])
    return refugee_count


def plan_statistics_function(Plan):
    """
    Review the plan data for a specific plan and return each camp in a plan with total active volunteers and total refugees. Done as a dictionary.
    """
    plan_statistics_dict = {}
    for camp in Plan.camps:
        num_of_volunteers = count_volunteers(camp)
        num_of_refugees = count_refugees(camp)
        num_volunteers_vs_standard = calculate_ideal_volunteers_needed(num_of_volunteers, num_of_refugees)
        plan_statistics_dict[camp.name] = {'num_of_refugees': num_of_refugees,
                                           'num_of_volunteers': num_of_volunteers,
                                           'num_volunteers_vs_standard': num_volunteers_vs_standard}
    return plan_statistics_dict


def calculate_ideal_volunteers_needed(num_of_volunteers, num_of_refugees):
    """
    Calculate the extra volunteers needed and remaining volunteers not needed for a camp by 1:20 number of volunteers and number of refugees ratio.
    """
    TARGET_REFUGEE_VOLUNTEER_RATIO = 20
    ideal_volunteers_num = int(math.ceil(num_of_refugees / TARGET_REFUGEE_VOLUNTEER_RATIO))

    return f"{num_of_volunteers}:{ideal_volunteers_num}"


