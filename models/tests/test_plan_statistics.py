from unittest import TestCase

import models.plan_statistics
from models.base.document import Document, ReferenceDocumentsField
from models.camp import Camp
from models.refugee import Refugee
from models.volunteer import Volunteer
from models.plan import Plan

if __name__ == '__main__':
    unittest.main()


class PlanStatisticsVolunteerTest(unittest.TestCase):
    """
    Class for testing cases involving volunteer counts in plan statistics.
    """

    def test_active_volunteer_count(self):
        """
        Test case where only active volunteers are in the file.
        If this passes, volunteer_count and number of volunteers added in test case should be equal.
        Expecting volunteer_count = 3.
        """
        test_plan = Plan(name='First Plan',
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
        plan = Plan.find('test_plan')
        test_camp = test_plan.camps.get('camp1')
        test_camp.volunteer.add(volunteer_a, volunteer_b, volunteer_c)

        volunteer_count = find_volunteer("camp1")

        self.assertEqual(volunteer_count, 3)

    def test_deactivated_volunteer_not_counted(self):
        """
        Test case where only deactive volunteers are in the file.
        If this passes, volunteer_count should equal 0, since deactivated volunteers are not counted in this function.
        """
        test_plan = Plan(name='First Plan',
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
        plan = Plan.find('test_plan')
        test_camp = test_plan.camps.get('camp1')
        test_camp.volunteer.add(volunteer_a, volunteer_b, volunteer_c)
        setattr(volunteer_a, account_activated, False)
        setattr(volunteer_b, account_activated, False)
        setattr(volunteer_c, account_activated, False)

        volunteer_count = find_volunteer("camp1")
        self.assertEqual(volunteer_count, 0)

    def test_partially_active_volunteer_count(self):
        """
        Test case where some active and some deactivated volunteers are in the file.
        This test is to make sure that only the active volunteers are counted and the deactivated volunteers
        are disregarded in the count.
        """
        test_plan = Plan(name='First Plan',
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
        plan = Plan.find('test_plan')
        test_camp = test_plan.camps.get('camp1')
        test_camp.volunteer.add(volunteer_a, volunteer_b, volunteer_c)
        setattr(volunteer_a, account_activated, False)

        volunteer_count = find_volunteer("camp1")
        self.assertEqual(volunteer_count, 2)

    def test_no_volunteers_in_file(self):
        """
        Test case where no volunteers are in the file for a camp.
        In this case, expecting volunteer_count = 0, since there are no volunteers to count.
        """
        test_plan = Plan(name='First Plan',
                         emergency_type=Plan.EmergencyType.EARTHQUAKE,
                         description='Test emergency plan',
                         geographical_area='London',
                         camps=[Camp(name='camp1')])
        volunteer_count = find_volunteer("camp1")

        self.assertEqual(volunteer_count, 0)

    def test_volunteer_count_multiple_camps(self):
        """
        Test case where only active volunteers are in the file and active volunteers are at multiple camps.
        """
        test_plan = Plan(name='First Plan',
                         emergency_type=Plan.EmergencyType.EARTHQUAKE,
                         description='Test emergency plan',
                         geographical_area='London',
                         camps=[Camp(name='camp1'), Camp(name='camp2')])
        volunteer_a = Volunteer(username='yunsy', password='root', firstname='Yunsy', lastname='Yin',
                                phone='+447519953189')
        volunteer_b = Volunteer(username='paul', password='root', firstname='Paul', lastname='Shoemaker',
                                phone='+447519955439')
        volunteer_c = Volunteer(username='gerald', password='root', firstname='Gerald', lastname='Smith',
                                phone='+447511111111')
        plan = Plan.find('test_plan')
        test_camp1 = test_plan.camps.get('camp1')
        test_camp1.volunteer.add(volunteer_a)
        test_camp2 = test_plan.camps.get('camp2')
        test_camp2.volunteer.add(volunteer_b, volunteer_c)

        volunteer_count_camp1 = find_volunteer('camp1')
        volunteer_count_camp2 = find_volunteer('camp2')

        self.assertEqual(volunteer_count_camp1, 1)
        self.assertEqual(volunteer_count_camp2, 2)


class PlanStatisticsRefugeeTest(unittest.TestCase):
    """
    Class for testing cases involving refugee counts in plan statistics.
    """
# Notes for find_refugee testing:
    def test_refugee_count_single_family(self):
        """
        Test to check that refugee count is correct for a single refugee family.
        """
        test_plan = Plan(name='First Plan',
                         emergency_type=Plan.EmergencyType.EARTHQUAKE,
                         description='Test emergency plan',
                         geographical_area='London',
                         camps=[Camp(name='camp1')])
        refugee1 = Refugee(firstname="Tom",
                           lastname="Bond",
                           num_of_family_member=6,
                           starting_date=date(2020, 1, 2),
                           medical_condition_type=[Refugee.MedicalCondition.HIV, Refugee.MedicalCondition.CANCER])
        plan = Plan.find('test_plan')
        test_camp = test_plan.camps.get('camp1')
        test_camp.refugee.add(refugee1)

        refugee_count = find_refugee("camp1")

        self.assertEqual(refugee_count, 7)
#         NEED TO CHECK THIS 7 IS CORRECT

    def test_refugee_count_multiple_families_one_camp(self):
        """
        Test to check that refugee count is correct for multiple refugee families at a single camp.
        """
        test_plan = Plan(name='First Plan',
                         emergency_type=Plan.EmergencyType.EARTHQUAKE,
                         description='Test emergency plan',
                         geographical_area='London',
                         camps=[Camp(name='camp1')])
        refugee1 = Refugee(firstname="Tom",
                           lastname="Bond",
                           num_of_family_member=6,
                           starting_date=date(2020, 1, 2),
                           medical_condition_type=[Refugee.MedicalCondition.HIV, Refugee.MedicalCondition.CANCER])
        refugee1 = Refugee(firstname="Harry",
                           lastname="Ranger",
                           num_of_family_member=1,
                           starting_date=date(2020, 1, 2),
                           medical_condition_type=[Refugee.MedicalCondition.HIV, Refugee.MedicalCondition.CANCER])
        plan = Plan.find('test_plan')
        test_camp = test_plan.camps.get('camp1')
        test_camp.refugee.add(refugee1, refugee2)

        refugee_count = find_refugee("camp1")

        self.assertEqual(refugee_count, 8)

        def test_refugee_count_multiple_camps(self):
            """
            Test to check that refugee count is correct for a single camp when refugee families exist at multiple
            camps under the same plan.
            """
            test_plan = Plan(name='First Plan',
                             emergency_type=Plan.EmergencyType.EARTHQUAKE,
                             description='Test emergency plan',
                             geographical_area='London',
                             camps=[Camp(name='camp1'), Camp(name='camp2')])
            refugee1 = Refugee(firstname="Tom",
                               lastname="Bond",
                               num_of_family_member=6,
                               starting_date=date(2020, 1, 2),
                               medical_condition_type=[Refugee.MedicalCondition.HIV, Refugee.MedicalCondition.CANCER])
            refugee1 = Refugee(firstname="Harry",
                               lastname="Ranger",
                               num_of_family_member=1,
                               starting_date=date(2020, 1, 2),
                               medical_condition_type=[Refugee.MedicalCondition.HIV, Refugee.MedicalCondition.CANCER])
            plan = Plan.find('test_plan')
            test_camp1 = test_plan.camps.get('camp1')
            test_camp2.refugee.add(refugee1)

            test_camp2 = test_plan.camps.get('camp2')
            test_camp2.refugee.add(refugee2)

            refugee_count = find_refugee("camp1")

            self.assertEqual(refugee_count, 7)


# Notes for plan_statistics_function testing:
# 1. Test volunteer_count and refugee_count correct for each camp
