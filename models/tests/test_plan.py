import unittest
from datetime import date

from models.camp import Camp
from models.plan import Plan


class PlanTest(unittest.TestCase):
    """
    Test Plan class
    """

    def test_create_plan(self):
        """
        Test Plan creation
        """
        plan = Plan(name='My Plan',
                    emergency_type=Plan.EmergencyType.EARTHQUAKE,
                    description='Test emergency plan',
                    geographical_area='',
                    start_date=date(2999, 1, 1),
                    camps=[Camp(name='TestCamp')])
        self.assertEqual("Plan 'My Plan'", str(plan))

    def test_missing_camps(self):
        """
        Test that missing camps are rejected
        """
        with self.assertRaises(Plan.MissingCampsError):
            Plan(name='My Plan',
                 emergency_type=Plan.EmergencyType.EARTHQUAKE,
                 description='Test emergency plan',
                 geographical_area='',
                 start_date=date(2999, 1, 1),
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
                    start_date=date(2999, 1, 1),
                    camps=[camp_1])
        plan.open_camps(camp_2, camp_3)
        self.assertListEqual(list(plan.camps), [camp_1, camp_2, camp_3])
        plan.open_camps(camp_3, camp_4)
        self.assertListEqual(list(plan.camps), [camp_1, camp_2, camp_3, camp_4])

    def test_close_camps(self):
        """
        Test Plan closing camps
        """
        camp_1 = Camp(name='Camp 1')
        camp_2 = Camp(name='Camp 2')
        camp_3 = Camp(name='Camp 3')
        plan = Plan(name='My Plan',
                    emergency_type=Plan.EmergencyType.EARTHQUAKE,
                    description='Test emergency plan',
                    geographical_area='',
                    start_date=date(2999, 1, 1),
                    camps=[camp_1, camp_2, camp_3])
        plan.close_camps(camp_3)
        self.assertListEqual(list(plan.camps), [camp_1, camp_2])
        plan.close_camps(camp_2)
        self.assertListEqual(list(plan.camps), [camp_1])

    def test_invalid_start(self):
        """
        Test that invalid start dates are rejected
        """
        with self.assertRaises(Plan.PastStartDateException):
            Plan(name='My Plan',
                 emergency_type=Plan.EmergencyType.EARTHQUAKE,
                 description='Test emergency plan',
                 geographical_area='',
                 start_date=date(2000, 1, 1),
                 camps=[Camp(name='TestCamp')])
