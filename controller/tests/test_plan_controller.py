import unittest
from datetime import date

from controller.controller_error import ControllerError
from models.camp import Camp
from models.plan import Plan
import controller.plan_controller as pc


class PlanControllerTest(unittest.TestCase):
    def setUp(self):
        Plan.delete_all()

    def test_close_plan_controller(self):
        """
        Test status flag of plan. Should be true when plan is closed.
        """
        plan = Plan(name='My Plan',
                    emergency_type=Plan.EmergencyType.EARTHQUAKE,
                    description='Test emergency plan',
                    geographical_area='',
                    camps=[Camp(name='TestCamp')])
        pc.close_plan(plan)
        self.assertTrue(plan.is_closed)

    def test_initialised_plan_no_close_date(self):
        """
        Test plan closure date is None if a plan has not been closed.
        """
        plan = Plan(name='My Plan',
                    emergency_type=Plan.EmergencyType.EARTHQUAKE,
                    description='Test emergency plan',
                    geographical_area='',
                    camps=[Camp(name='TestCamp')])
        self.assertEqual(None, plan.close_date)

    def test_close_date_set_controller(self):
        """
        Test plan closure date is set to today's date when plan is closed.
        """
        self.setUp()
        plan = Plan(name='My Plan',
                    emergency_type=Plan.EmergencyType.EARTHQUAKE,
                    description='Test emergency plan',
                    geographical_area='',
                    camps=[Camp(name='TestCamp')])
        pc.close_plan(plan)
        self.assertEqual(date.today(), plan.close_date)

    def test_find_plan_controller(self):
        """
        Test to see if find plan function returns the correct plan, given the plan name.
        """
        test_plan = Plan(name='My Plan',
                         emergency_type=Plan.EmergencyType.EARTHQUAKE,
                         description='Test emergency plan',
                         geographical_area='',
                         camps=[Camp(name='TestCamp')])
        found_plan = pc.find_plan('My Plan')
        self.assertEqual(test_plan, found_plan)

    def test_no_plan_found_controller(self):
        """
        Test that if no plan is found then an exception is raised.
        """
        with self.assertRaises(pc.controller_error.ControllerError):
            pc.find_plan('My Plan')

    def test_create_plan_controller(self):
        """
        Test to see if plan is created correctly with controller.
        """
        plan = pc.create_plan(plan_name='My Plan',
                              emergency_type=Plan.EmergencyType.EARTHQUAKE,
                              description='Test emergency plan',
                              geographical_area='',
                              camps=[Camp(name='TestCamp')])
        self.assertEqual('My Plan', plan.name)

    def test_missing_camps_error_controller(self):
        with self.assertRaises(pc.controller_error.ControllerError):
            pc.create_plan(plan_name='My Plan',
                           emergency_type=Plan.EmergencyType.EARTHQUAKE,
                           description='Test emergency plan',
                           geographical_area='',
                           camps=[])

    def test_create_camps_controller(self):
        """
        Test that camps are added to plan correctly.
        """
        self.assertIsInstance(pc.create_camps('Camp 1'), Camp)

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

        expected = [Plan.find('First Plan'), Plan.find('Second Plan'), Plan.find('Third Plan')]
        self.assertListEqual(expected, pc.list_plans())

    def test_find_camp_controller(self):
        camp = Camp(name='TestCamp')
        plan = Plan(name='My Plan',
                    emergency_type=Plan.EmergencyType.EARTHQUAKE,
                    description='Test emergency plan',
                    geographical_area='UK',
                    camps=[camp])
        self.assertEqual(pc.find_camp(plan, 'TestCamp'), camp)

    def test_find_non_existent_camp_controller(self):
        camp = Camp(name='TestCamp')
        plan = Plan(name='My Plan',
                    emergency_type=Plan.EmergencyType.EARTHQUAKE,
                    description='Test emergency plan',
                    geographical_area='UK',
                    camps=[camp])
        with self.assertRaises(ControllerError):
            pc.find_camp(plan, 'NonExistentCamp')

