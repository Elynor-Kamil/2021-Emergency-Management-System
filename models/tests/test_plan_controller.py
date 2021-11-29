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
    def test_list_plans_controller(self):
        """
        Test to see if plans are listed correctly.

        NOTE: list_plans is showing 3 plans when it should be showing 2. But none of the plans match.
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

    def test_close_date_set(self):
        """
        Test plan closure date is set to today's date when plan is closed.
        """
        plan = Plan(name='My Plan',
                    emergency_type=Plan.EmergencyType.EARTHQUAKE,
                    description='Test emergency plan',
                    geographical_area='',
                    camps=[Camp(name='TestCamp')])
        close_plan(plan)
        self.assertEqual(date.today(), plan.close_date)

    def test_find_plan_controller(self):
        """
        Test to see if the plan is found by it's name
        """
        test_plan = Plan(name='My Plan',
                         emergency_type=Plan.EmergencyType.EARTHQUAKE,
                         description='Test emergency plan',
                         geographical_area='',
                         camps=[Camp(name='TestCamp')])
        found_plan = find_plan('My Plan')
        self.assertEqual(test_plan, found_plan)

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

    def test_create_camps_controller(self):
        """
        Test that camps are added to plan correctly.

        Camps are being created but test is failing?
        """
        create_camp_plan = Plan(name='My Plan Camp Test',
                                emergency_type=Plan.EmergencyType.EARTHQUAKE,
                                description='Test emergency plan',
                                geographical_area='',
                                camps=[Camp(name='Camp 0')])
        print(create_camp_plan.camps)  # only have 'Camp 0' at first
        create_camps('Camp 1', 'My Plan Camp Test')
        print(create_camp_plan.camps)  # in here we can see that 'Camp 1' has been
        # added to the Plan
        self.assertListEqual([Camp(name='Camp 0'), Camp(name='Camp 1')], list(create_camp_plan.camps))
