import unittest
from datetime import date
from models.refugee import Refugee
from models.volunteer import Volunteer
from models.camp import Camp
from models.plan import Plan


class PlanTest(unittest.TestCase):
    """
    Test Plan class
    """

    def setUp(self) -> None:
        Plan.delete_all()

    def test_create_plan(self):
        """
        Test Plan creation
        """
        plan = Plan(name='My Plan',
                    emergency_type=Plan.EmergencyType.EARTHQUAKE,
                    description='Test emergency plan',
                    geographical_area='',
                    camps=[Camp(name='TestCamp')])
        self.assertEqual("Plan 'My Plan'\nEmergency Type: 'Earthquake'\n", str(plan))

    def test_missing_camps(self):
        """
        Test that missing camps are rejected
        """
        with self.assertRaises(Plan.MissingCampsError):
            Plan(name='My Plan',
                 emergency_type=Plan.EmergencyType.EARTHQUAKE,
                 description='Test emergency plan',
                 geographical_area='',
                 camps=[])

    def test_open_camps(self):
        """
        Test Plan opening camps
        """
        camp_1 = Camp(name='Camp 1')
        camp_2 = Camp(name='Camp 2')
        camp_3 = Camp(name='Camp 3')
        camp_4 = Camp(name='Camp 4')
        plan = Plan(name='My Plan',
                    emergency_type=Plan.EmergencyType.EARTHQUAKE,
                    description='Test emergency plan',
                    geographical_area='',
                    camps=[camp_1])
        plan.open_camps(camp_2, camp_3)
        self.assertListEqual([camp_1, camp_2, camp_3], list(plan.camps))
        plan.open_camps(camp_4)
        self.assertListEqual([camp_1, camp_2, camp_3, camp_4], list(plan.camps))

    def test_close_camps(self):
        """
        Test Plan closing camps
        """
        camp_1 = Camp(name='Camp 1')
        camp_2 = Camp(name='Camp 2')
        camp_3 = Camp(name='Camp 3')
        plan = Plan('My Plan',
                    emergency_type=Plan.EmergencyType.EARTHQUAKE,
                    description='Test emergency plan',
                    geographical_area='',
                    camps=[camp_1, camp_2, camp_3])
        plan.close_camps(camp_3)
        self.assertListEqual([camp_1, camp_2], list(plan.camps))

    def test_close_nonexistent_camp(self):
        """
        Test that closing a camp that is not open is rejected
        """
        camp_1 = Camp(name='Camp 1')
        camp_2 = Camp(name='Camp 2')
        plan = Plan(name='My Plan',
                    emergency_type=Plan.EmergencyType.EARTHQUAKE,
                    description='Test emergency plan',
                    geographical_area='',
                    camps=[camp_1])
        with self.assertRaises(Plan.CampNotFoundError):
            plan.close_camps(camp_2)

    def test_close_all_camps(self):
        """
        Test that closing all camps is rejected
        """
        camp_1 = Camp(name='Camp 1')
        camp_2 = Camp(name='Camp 2')
        camp_3 = Camp(name='Camp 3')
        plan = Plan(name='My Plan',
                    emergency_type=Plan.EmergencyType.EARTHQUAKE,
                    description='Test emergency plan',
                    geographical_area='',
                    camps=[camp_1, camp_2, camp_3])
        with self.assertRaises(Plan.MissingCampsError):
            plan.close_camps(camp_1, camp_2, camp_3)

    def test_start_date_today(self):
        """
        Test that start date is today
        """
        plan = Plan(name='My Plan',
                    emergency_type=Plan.EmergencyType.EARTHQUAKE,
                    description='Test emergency plan',
                    geographical_area='',
                    camps=[Camp(name='TestCamp')])
        self.assertEqual(date.today(), plan.start_date)

    def test_initialised_plan_not_closed(self):
        """
        Test status flag of plan. Should be false is plan is open.
        """
        plan = Plan(name='My Plan',
                    emergency_type=Plan.EmergencyType.EARTHQUAKE,
                    description='Test emergency plan',
                    geographical_area='',
                    camps=[Camp(name='TestCamp')])
        self.assertEqual(False, plan.is_closed)

    def test_close_plan(self):
        """
        Test status flag of plan. Should be true when plan is closed.
        """
        plan = Plan(name='My Plan',
                    emergency_type=Plan.EmergencyType.EARTHQUAKE,
                    description='Test emergency plan',
                    geographical_area='',
                    camps=[Camp(name='TestCamp')])
        plan.close()
        self.assertEqual(True, plan.is_closed)

    def test_initialised_plan_no_close_date(self):
        """
        Test that close date is not set during plan creation.
        """
        plan = Plan(name='My Plan',
                    emergency_type=Plan.EmergencyType.EARTHQUAKE,
                    description='Test emergency plan',
                    geographical_area='',
                    camps=[Camp(name='TestCamp')])
        self.assertEqual(None, plan.close_date)

    def test_close_date_set(self):
        """
        Test plan closure date is set to today's date when plan is closed.
        """
        plan = Plan(name='My Plan',
                    emergency_type=Plan.EmergencyType.EARTHQUAKE,
                    description='Test emergency plan',
                    geographical_area='',
                    camps=[Camp(name='TestCamp')])
        plan.close()
        self.assertEqual(date.today(), plan.close_date)

    def test_plan_statistics_for_one_camp(self):
        """
        Test to check number of volunteers and refugees returned by statistics function
        for a single camp is correct.
        Also tests the feature to check how many additional volunteers are recommended (number of refugees / 20),
        hence should return 27 in the third list position in the plan_statistics value list.
        """
        test_camp = Camp(name='camp1')
        test_plan = Plan(name='test_plan1',
                         emergency_type=Plan.EmergencyType.EARTHQUAKE,
                         description='Test emergency plan',
                         geographical_area='London',
                         camps=[test_camp])
        volunteer_a = Volunteer(username='William', password='root', firstname='William', lastname='Yin',
                                phone='+447519953189')
        volunteer_b = Volunteer(username='Mary', password='root', firstname='Mary', lastname='Shoemaker',
                                phone='+447519955439')
        volunteer_c = Volunteer(username='Lily', password='root', firstname='Lily', lastname='Smith',
                                phone='+447511111111')
        test_camp.volunteers.add(volunteer_a, volunteer_b, volunteer_c)
        refugee1 = Refugee(firstname="Tom",
                           lastname="Bond",
                           num_of_family_member=600,
                           starting_date=date(2020, 1, 2),
                           medical_condition_type=[Refugee.MedicalCondition.HIV, Refugee.MedicalCondition.CANCER])
        test_camp.refugees.add(refugee1)
        test_plan_statistics = test_plan.statistics()
        test_dictionary = {'camp1': {'num_of_refugees': 600,
                                     'num_of_volunteers': 3,
                                     'num_volunteers_vs_standard': '3:30'}
                           }
        self.assertDictEqual(test_dictionary, test_plan_statistics)

    def test_plan_statistics_two_plans_exist(self):
        """
        Test to check number of volunteers and refugees returned by statistics fucntion
        for a single camp is correct, when there is another plan that also exists with volunteers and refugees.
        Also tests where number of volunteers needed is less than the number currently at the camp,
        hence should return 0 extra volunteers required at the end of the plan_statistics dictionary.
        """
        test_camp1 = Camp(name='camp1')
        test_camp2 = Camp(name='camp2')
        test_plan1 = Plan(name='test_plan1',
                          emergency_type=Plan.EmergencyType.EARTHQUAKE,
                          description='Test emergency plan',
                          geographical_area='London',
                          camps=[test_camp1])
        test_plan2 = Plan(name='test_plan2',
                          emergency_type=Plan.EmergencyType.EARTHQUAKE,
                          description='Test emergency plan',
                          geographical_area='London',
                          camps=[test_camp2])
        volunteer_a = Volunteer(username='William', password='root', firstname='William', lastname='Yin',
                                phone='+447519953189')
        volunteer_b = Volunteer(username='Mary', password='root', firstname='Mary', lastname='Shoemaker',
                                phone='+447519955439')
        volunteer_c = Volunteer(username='Lily', password='root', firstname='Lily', lastname='Smith',
                                phone='+447511111111')
        test_camp1.volunteers.add(volunteer_a, volunteer_b)
        test_camp2.volunteers.add(volunteer_c)
        refugee1 = Refugee(firstname="Tom",
                           lastname="Bond",
                           num_of_family_member=6,
                           starting_date=date(2020, 1, 2),
                           medical_condition_type=[Refugee.MedicalCondition.HIV, Refugee.MedicalCondition.CANCER])
        refugee2 = Refugee(firstname="Terry",
                           lastname="Bimble",
                           num_of_family_member=2,
                           starting_date=date(2020, 1, 2),
                           medical_condition_type=[Refugee.MedicalCondition.HIV, Refugee.MedicalCondition.CANCER])
        test_camp1.refugees.add(refugee1)
        test_plan_statistics1 = test_plan1.statistics()
        test_camp2.refugees.add(refugee2)
        test_dictionary = {'camp1': {'num_of_refugees': 6,
                                     'num_of_volunteers': 2,
                                     'num_volunteers_vs_standard': '2:1'}}
        self.assertDictEqual(test_dictionary, test_plan_statistics1)

    def tearDown(self):
        """
        Function to delete stored data after a test has finished running
        to avoid corrupting other tests
        """
        Plan.delete_all()
        Volunteer.delete_all()
