import unittest
from datetime import date
from models.camp import Camp
from models.plan import Plan
from models.refugee import Refugee
import controller.refugee_controller as rc


class RefugeeControllerTest(unittest.TestCase):
    """
    Class for testing cases in create refugee function.
    """

    def setUp(self):
        Plan.delete_all()

    def test_create_refugee(self):
        """
        Test Refugee creation
        """
        test_camp = Camp(name='camp1')
        Plan(name='test_plan',
             emergency_type=Plan.EmergencyType.EARTHQUAKE,
             description='Test emergency plan',
             geographical_area='London',
             camps=[test_camp])
        new_refugee = rc.create_refugee("James", "Bond", test_camp, 6, date(2020, 1, 1),
                                        [Refugee.MedicalCondition.HIV, Refugee.MedicalCondition.CANCER])
        self.assertIsInstance(new_refugee, Refugee)

    def test_create_refugee_closed_plan(self):
        test_camp = Camp(name='camp1')
        plan = Plan(name='test_plan',
                    emergency_type=Plan.EmergencyType.EARTHQUAKE,
                    description='Test emergency plan',
                    geographical_area='London',
                    camps=[test_camp])
        plan.close()
        with self.assertRaises(rc.ControllerError):
            rc.create_refugee("James", "Bond", test_camp, 6, date(2020, 1, 1),
                              [Refugee.MedicalCondition.HIV, Refugee.MedicalCondition.CANCER])

    def test_find_and_return_refugee(self):
        """
        Test case where refugee specified is found in the file.
        """
        test_camp = Camp(name='camp1')
        Plan(name='test_plan',
             emergency_type=Plan.EmergencyType.EARTHQUAKE,
             description='Test emergency plan',
             geographical_area='London',
             camps=[test_camp])
        refugee = Refugee(firstname="Tom",
                          lastname="Bond",
                          num_of_family_member=600,
                          starting_date=date(2020, 1, 2),
                          medical_condition_type=[Refugee.MedicalCondition.HIV, Refugee.MedicalCondition.CANCER])
        test_camp.refugees.add(refugee)
        refugee_id = refugee.user_id
        retrieved_refugee = rc.find_refugee(refugee_id)
        self.assertEqual(refugee, retrieved_refugee)

    def test_find_nonexistent_refugee(self):
        """
        Test case where refugee specified is not found in the file.
        """
        test_camp = Camp(name='camp1')
        Plan(name='test_plan1',
             emergency_type=Plan.EmergencyType.EARTHQUAKE,
             description='Test emergency plan',
             geographical_area='London',
             camps=[test_camp])
        refugee1 = Refugee(firstname="Tom",
                           lastname="Bond",
                           num_of_family_member=600,
                           starting_date=date(2020, 1, 2),
                           medical_condition_type=[Refugee.MedicalCondition.HIV, Refugee.MedicalCondition.CANCER])
        test_camp.refugees.add(refugee1)
        refugee_user_id = 1111111111
        with self.assertRaises(rc.ControllerError):
            rc.find_refugee(refugee_user_id)

    def test_view_refugee_return_value(self):
        """
        Test case where refugee view is same as the refugee specified.
        """
        test_camp = Camp(name='camp1')
        Plan(name='test_plan',
             emergency_type=Plan.EmergencyType.EARTHQUAKE,
             description='Test emergency plan',
             geographical_area='London',
             camps=[test_camp])
        refugee = Refugee(firstname="Terry",
                          lastname="Bimble",
                          num_of_family_member=2,
                          starting_date=date(2020, 1, 2),
                          medical_condition_type=[Refugee.MedicalCondition.HIV, Refugee.MedicalCondition.CANCER])
        test_camp.refugees.add(refugee)
        refugee_str = rc.view_refugee(refugee)
        self.assertEqual(refugee_str, str(refugee))

    def tearDown(self) -> None:
        Plan.delete_all()
