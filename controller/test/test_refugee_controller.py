import unittest
from datetime import date
from models.camp import Camp
from models.refugee import Refugee
from models.volunteer import Volunteer
from models.plan import Plan
from controller.refugee_controller import create_refugee, find_refugee, view_refugee


class RefugeeControllerTest(unittest.TestCase):
    """
    Class for testing cases in create refugee function.
    """

    def test_create_refugee(self):
        """
        Test Refugee creation
        """
        Plan(name='test_plan1',
             emergency_type=Plan.EmergencyType.EARTHQUAKE,
             description='Test emergency plan',
             geographical_area='London',
             camps=[Camp(name='camp1')])

        test_plan = Plan.find('test_plan1')
        test_camp = test_plan.camps.get('camp1')
        new_refugee = create_refugee("James", "Bond", test_camp, 6, date(2020, 1, 1), {Refugee.MedicalCondition.HIV, Refugee.MedicalCondition.CANCER})
        self.assertIsInstance(new_refugee, Refugee)



    def test_find_and_return_refugee(self):
        """
        Test case where refugee specified is found in the file.
        """
        Plan(name='test_plan1',
             emergency_type=Plan.EmergencyType.EARTHQUAKE,
             description='Test emergency plan',
             geographical_area='London',
             camps=[Camp(name='camp1')])
        test_plan = Plan.find('test_plan1')
        test_camp = test_plan.camps.get('camp1')
        refugee = Refugee(firstname="Tom",
                          lastname="Bond",
                          num_of_family_member=600,
                          starting_date=date(2020, 1, 2),
                          medical_condition_type=[Refugee.MedicalCondition.HIV, Refugee.MedicalCondition.CANCER])
        test_camp.refugees.add(refugee)
        refugee_user_id = refugee.user_id
        retrieved_refugee = find_refugee(refugee_user_id)
        self.assertEqual(refugee, retrieved_refugee)


    def test_find_refugee_return_no_refugee(self):
        """
        Test case where refugee specified is found in the file.
        """
        Plan(name='test_plan1',
             emergency_type=Plan.EmergencyType.EARTHQUAKE,
             description='Test emergency plan',
             geographical_area='London',
             camps=[Camp(name='camp1')])
        test_plan = Plan.find('test_plan1')
        test_camp = test_plan.camps.get('camp1')
        refugee1 = Refugee(firstname="Tom",
                           lastname="Bond",
                           num_of_family_member=600,
                           starting_date=date(2020, 1, 2),
                           medical_condition_type=[Refugee.MedicalCondition.HIV, Refugee.MedicalCondition.CANCER])
        test_camp.refugees.add(refugee1)
        refugee_user_id = 1111111111
        refugee = find_refugee(refugee_user_id)
        self.assertIsNone(refugee, refugee1)


    def test_view_refugee_return_value(self):
        """
        Test case where refugee view is same as the refugee specified.
        """
        Plan(name='test_plan1',
             emergency_type=Plan.EmergencyType.EARTHQUAKE,
             description='Test emergency plan',
             geographical_area='London',
             camps=[Camp(name='camp1')])
        test_plan = Plan.find('test_plan1')
        test_camp = test_plan.camps.get('camp1')
        refugee1 = Refugee(firstname="Terry",
                           lastname="Bimble",
                           num_of_family_member=2,
                           starting_date=date(2020, 1, 2),
                           medical_condition_type=[Refugee.MedicalCondition.HIV, Refugee.MedicalCondition.CANCER])
        test_camp.refugees.add(refugee1)
        refugee_str = view_refugee(refugee1)
        self.assertEqual(refugee_str, str(refugee1))

if __name__ == '__main__':
    unittest.main()