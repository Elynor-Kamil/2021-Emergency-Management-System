import unittest
from datetime import date

from models.camp import Camp
from models.plan import Plan
from controller.plan_controller import close_plan
from controller.plan_controller import find_plan
from controller.plan_controller import create_plan
from controller.plan_controller import list_plans
from controller.plan_controller import create_camps


class PlanControllerTest(unittest.TestCase):
    def setUp(self):
        Plan.delete_all()

    def test_plan_status(self):
        """
        Test status flag of plan. Should be false is plan is open.
        """
        plan = Plan(name='My Plan',
                    emergency_type=Plan.EmergencyType.EARTHQUAKE,
                    description='Test emergency plan',
                    geographical_area='',
                    camps=[Camp(name='TestCamp')])
        self.assertEqual(False, plan.close_plan_status)
        self.setUp()

    def test_close_plan_controller(self):
        """
        Test status flag of plan. Should be true when plan is closed.
        """
        plan = Plan(name='My Plan',
                    emergency_type=Plan.EmergencyType.EARTHQUAKE,
                    description='Test emergency plan',
                    geographical_area='',
                    camps=[Camp(name='TestCamp')])
        close_plan(plan)
        self.assertEqual(True, plan.close_plan_status)
        self.setUp()

    def test_no_close_date(self):
        """
        Test that close date is not set during plan creation.
        """
        plan = Plan(name='My Plan',
                    emergency_type=Plan.EmergencyType.EARTHQUAKE,
                    description='Test emergency plan',
                    geographical_area='',
                    camps=[Camp(name='TestCamp')])
        self.assertEqual(None, plan.close_date)
        self.setUp()

    def test_close_date_set(self):
        """
        Test plan closure date is set to today's date when plan is closed.
        """
        self.setUp()
        plan = Plan(name='My Plan',
                    emergency_type=Plan.EmergencyType.EARTHQUAKE,
                    description='Test emergency plan',
                    geographical_area='',
                    camps=[Camp(name='TestCamp')])
        print(plan.close_date)
        close_plan(plan)
        print(plan.close_date)
        self.assertEqual(date.today(), plan.close_date)

    def test_find_plan_controller(self):
        """
        Test to see find plan given plan name.
        """
        test_plan = Plan(name='My Plan',
                         emergency_type=Plan.EmergencyType.EARTHQUAKE,
                         description='Test emergency plan',
                         geographical_area='',
                         camps=[Camp(name='TestCamp')])
        found_plan = find_plan('My Plan')
        self.assertEqual(test_plan, found_plan)
        self.setUp()

    def test_create_plan_controller(self):
        """
        Test to see if plan is created correctly with controller.
        """
        plan = create_plan(name='My Plan',
                           emergency_type=Plan.EmergencyType.EARTHQUAKE,
                           description='Test emergency plan',
                           geographical_area='',
                           camps=[Camp(name='TestCamp')])
        self.assertEqual('My Plan', plan.name)
        self.setUp()

    def test_create_camps_controller(self):
        """
        Test that camps are added to plan correctly.
        """
        create_camp_plan = Plan(name='My Plan Camp Test',
                                emergency_type=Plan.EmergencyType.EARTHQUAKE,
                                description='Test emergency plan',
                                geographical_area='',
                                camps=[Camp(name='Camp 0')])
        create_camps('Camp 1', create_camp_plan)
        camp_1 = create_camp_plan.camps.get('Camp 0')
        camp_2 = create_camp_plan.camps.get('Camp 1')
        camps_list = [camp_1.name, camp_2.name]
        self.assertListEqual(['Camp 0', 'Camp 1'], camps_list)
        self.setUp()

    def test_list_plans_controller(self):
        """
        Test to see if plans are listed correctly.
        """
        Plan(name='First Plan',
             emergency_type=Plan.EmergencyType.EARTHQUAKE,
             description='Test emergency plan',
             geographical_area='',
             camps=[Camp(name='TestCamp')])

        Plan(name='Second Plan',
             emergency_type=Plan.EmergencyType.EARTHQUAKE,
             description='Test emergency plan',
             geographical_area='',
             camps=[Camp(name='TestCamp')])

        Plan(name='Third Plan',
             emergency_type=Plan.EmergencyType.EARTHQUAKE,
             description='Test emergency plan',
             geographical_area='',
             camps=[Camp(name='TestCamp')])

        find_list = [Plan.find('First Plan'), Plan.find('Second Plan'), Plan.find('Third Plan')]
        list_plan = list_plans()
        self.assertListEqual(find_list, list_plan)
        self.setUp()