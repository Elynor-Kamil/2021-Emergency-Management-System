import unittest
from models.camp import Camp
from models.refugee import Refugee
from models.volunteer import Volunteer
from models.plan import Plan
from datetime import date
from controller.plan_controller import view_plan_statistics

class PlanStatisticsControllerTest(unittest.TestCase):
    """
    Class for unit tests for plan statistics function view_plan_statistics in controller.
    """

    def test_view_plan_statistics_returns_str(self):
        """
        Test to confirm that view_plan_statistics function returns str
        when it combines intermediate variables statistics and plan_info.
        :return: str
        """
        Plan(name='test_plan1',
             emergency_type=Plan.EmergencyType.EARTHQUAKE,
             description='Test emergency plan',
             geographical_area='London',
             camps=[Camp(name='camp1')])
        volunteer_a = Volunteer(username='yunsy', password='root', firstname='Yunsy', lastname='Yin',
                                phone='+447519953189')
        volunteer_b = Volunteer(username='paul', password='root', firstname='Paul', lastname='Shoemaker',
                                phone='+447519955439')
        volunteer_c = Volunteer(username='gerald', password='root', firstname='Gerald', lastname='Smith',
                                phone='+447511111111')
        test_plan = Plan.find('test_plan1')
        test_camp = test_plan.camps.get('camp1')
        test_camp.volunteers.add(volunteer_a, volunteer_b, volunteer_c)
        refugee1 = Refugee(firstname="Tom",
                           lastname="Bond",
                           num_of_family_member=600,
                           starting_date=date(2020, 1, 2),
                           medical_condition_type=[Refugee.MedicalCondition.HIV, Refugee.MedicalCondition.CANCER])
        test_camp.refugees.add(refugee1)
        test_view_plan_statistics = view_plan_statistics(test_plan)
        self.assertEqual(type(test_view_plan_statistics), str)
