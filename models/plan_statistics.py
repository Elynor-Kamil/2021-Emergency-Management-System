from models.refugee import Refugee
from datetime import date
from models.volunteer import Volunteer
from models.camp import Camp
from models.plan import Plan
import math

volunteer1 = Volunteer(username='yunsy',
          password='root',
          firstname='Yunsy',
          lastname='Yin',
          phone='+447519953189')


volunteer2 = Volunteer(username='michelle',
          password='uuuu',
          firstname='Michelle',
          lastname='Yin',
          phone='+447519953189')

volunteer3 = Volunteer(username='mike',
          password='root',
          firstname='Mike',
          lastname='Yin',
          phone='+447519953189')


volunteer4 = Volunteer(username='nick',
          password='uuuu',
          firstname='nike',
          lastname='Yin',
          phone='+447519953189')



refugee1 = Refugee(firstname="Tom",
                   lastname="Bond",
                   num_of_family_member=1,
                   starting_date=date(2020, 1, 2),
                   medical_condition_type=[Refugee.MedicalCondition.HIV, Refugee.MedicalCondition.CANCER])

refugee2 = Refugee(firstname="Mary",
                   lastname="Queen",
                   num_of_family_member=4,
                   starting_date=date(2020, 1, 2),
                   medical_condition_type=[Refugee.MedicalCondition.HEART])

refugee3 = Refugee(firstname="Ben",
                   lastname="Arthurs",
                   num_of_family_member=11,
                   starting_date=date(2020, 1, 2),
                   medical_condition_type=[Refugee.MedicalCondition.CHRONICKIDNEY])

refugee4 = Refugee(firstname="Lily",
                   lastname="Low",
                   num_of_family_member=13,
                   starting_date=date(2020, 1, 2),
                   medical_condition_type=[Refugee.MedicalCondition.CHRONICLUNG])

camp1 = Camp(name='camp1')
camp2 = Camp(name='camp2')
camp3 = Camp(name='camp3')

camp1.volunteers = [volunteer1, volunteer2]
camp2.volunteers = [volunteer3, volunteer4]

camp1.refugees = [refugee1, refugee2]
camp2.refugees = [refugee3, refugee4]


plan = Plan(name='My Plan',
            emergency_type=Plan.EmergencyType.EARTHQUAKE,
            description='Test emergency plan',
            geographical_area='',
            camps=[camp1, camp2])


def find_volunteers(Camp):
    """
    Function to find the number of active volunteers at a camp.
    If a volunteer is not active then they will not be included in the count.
    """
    volunteer_count = 0
    for volunteer in Camp.volunteers:
        if volunteer.availability == True:
            volunteer_count += 1
    return volunteer_count

def find_refugees(Camp):
    """
    Function to find the number of refugees at a camp.
    Includes the count of both the head of family and the family members in a single count.
    """
    refugee_count = 0
    for refugee in Camp.refugees:
        refugee_count += refugee.num_of_family_member
    return refugee_count

def plan_statistics_function(Plan):
    plan_statistics = {}
    for camp in Plan.camps:
        num_of_volunteers = find_volunteers(camp)
        num_of_refugees = find_refugees(camp)
        plan_statistics[camp.name] = [num_of_volunteers, num_of_refugees]
        calculate_volunteer_needed(camp, plan_statistics)
    return plan_statistics

def calculate_volunteer_needed(Camp, plan_statistics):
    num_of_volunteers, num_of_refugees = plan_statistics[Camp.name]
    extra_volunteers_needed, remaining_volunteers = 0, 0
    ideal_volunteers_num = int(math.ceil(num_of_refugees / 20))
    if ideal_volunteers_num < num_of_volunteers:
        remaining_volunteers = num_of_volunteers - ideal_volunteers_num
    elif num_of_volunteers < ideal_volunteers_num:
        extra_volunteers_needed = ideal_volunteers_num - num_of_volunteers
    plan_statistics[Camp.name].append(remaining_volunteers)
    plan_statistics[Camp.name].append(extra_volunteers_needed)

r = plan_statistics_function(plan)
print(r)