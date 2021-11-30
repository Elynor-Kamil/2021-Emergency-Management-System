import unittest
from models.plan_statistics import find_volunteers, find_refugees, plan_statistics_function
from models.camp import Camp
from models.refugee import Refugee
from models.volunteer import Volunteer
from models.plan import Plan
from datetime import date

class PlanStatisticsVolunteerTest(unittest.TestCase):
    """
    Class for testing cases involving volunteer counts in plan statistics.
    """

    def tearDown(self):
        """
        Function to delete stored data after a test has finished running
        to avoid corrupting other tests
        """
        Plan.delete_all()

    def test_active_volunteer_count(self):
        """
        Test case where only active volunteers are in the file.
        If this passes, volunteer_count and number of volunteers added in test case should be equal.
        Expecting volunteer_count = 3.
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

        volunteer_count = find_volunteers(test_camp)

        self.assertEqual(volunteer_count, 3)
        self.tearDown()

    def test_deactivated_volunteer_not_counted(self):
        """
        Test case where only deactive volunteers are in the file.
        If this passes, volunteer_count should equal 0, since deactivated volunteers are not counted in this function.
        """
        Plan(name='test_plan2',
             emergency_type=Plan.EmergencyType.EARTHQUAKE,
             description='Test emergency plan',
             geographical_area='London',
             camps=[Camp(name='camp2')])
        volunteer_a = Volunteer(username='yunsy', password='root', firstname='Yunsy', lastname='Yin',
                                phone='+447519953189')
        volunteer_b = Volunteer(username='paul', password='root', firstname='Paul', lastname='Shoemaker',
                                phone='+447519955439')
        volunteer_c = Volunteer(username='gerald', password='root', firstname='Gerald', lastname='Smith',
                                phone='+447511111111')
        test_plan = Plan.find('test_plan2')
        test_camp = test_plan.camps.get('camp2')
        test_camp.volunteers.add(volunteer_a, volunteer_b, volunteer_c)
        volunteer_a.account_activated = False
        volunteer_b.account_activated = False
        volunteer_c.account_activated = False

        volunteer_count = find_volunteers(test_camp)
        self.assertEqual(volunteer_count, 0)
        self.tearDown()

    def test_partially_active_volunteer_count(self):
        """
        Test case where some active and some deactivated volunteers are in the file.
        This test is to make sure that only the active volunteers are counted and the deactivated volunteers
        are disregarded in the count.
        """
        Plan(name='test_plan3',
             emergency_type=Plan.EmergencyType.EARTHQUAKE,
             description='Test emergency plan',
             geographical_area='London',
             camps=[Camp(name='camp3')])
        volunteer_a = Volunteer(username='yunsy', password='root', firstname='Yunsy', lastname='Yin',
                                phone='+447519953189')
        volunteer_b = Volunteer(username='paul', password='root', firstname='Paul', lastname='Shoemaker',
                                phone='+447519955439')
        volunteer_c = Volunteer(username='gerald', password='root', firstname='Gerald', lastname='Smith',
                                phone='+447511111111')
        test_plan = Plan.find('test_plan3')
        test_camp = test_plan.camps.get('camp3')
        test_camp.volunteers.add(volunteer_a, volunteer_b, volunteer_c)
        volunteer_a.account_activated = False

        volunteer_count = find_volunteers(test_camp)
        self.assertEqual(volunteer_count, 2)
        self.tearDown()

    def test_deactivated_volunteer_not_counted(self):
        """
        Test case where only deactive volunteers are in the file.
        If this passes, volunteer_count should equal 0, since deactivated volunteers are not counted in this function.
        """
        Plan(name='test_plan4',
             emergency_type=Plan.EmergencyType.EARTHQUAKE,
             description='Test emergency plan',
             geographical_area='London',
             camps=[Camp(name='camp4')])
        volunteer_a = Volunteer(username='yunsy', password='root', firstname='Yunsy', lastname='Yin',
                                phone='+447519953189')
        volunteer_b = Volunteer(username='paul', password='root', firstname='Paul', lastname='Shoemaker',
                                phone='+447519955439')
        volunteer_c = Volunteer(username='gerald', password='root', firstname='Gerald', lastname='Smith',
                                phone='+447511111111')
        test_plan = Plan.find('test_plan4')
        test_camp = test_plan.camps.get('camp4')
        test_camp.volunteers.add(volunteer_a, volunteer_b, volunteer_c)
        volunteer_a.account_activated = False
        volunteer_b.account_activated = False
        volunteer_c.account_activated = False

        volunteer_count = find_volunteers(test_camp)
        self.assertEqual(volunteer_count, 0)
        self.tearDown()


    def test_available_volunteer_count(self):
        """
        Test case where only active volunteers are in the file.
        If this passes, volunteer_count and number of volunteers added in test case should be equal.
        Expecting volunteer_count = 3.
        """
        Plan(name='test_plan4',
             emergency_type=Plan.EmergencyType.EARTHQUAKE,
             description='Test emergency plan',
             geographical_area='London',
             camps=[Camp(name='camp5')])
        volunteer_a = Volunteer(username='yunsy', password='root', firstname='Yunsy', lastname='Yin',
                                phone='+447519953189')
        volunteer_b = Volunteer(username='paul', password='root', firstname='Paul', lastname='Shoemaker',
                                phone='+447519955439')
        volunteer_c = Volunteer(username='gerald', password='root', firstname='Gerald', lastname='Smith',
                                phone='+447511111111')
        test_plan = Plan.find('test_plan4')
        test_camp = test_plan.camps.get('camp5')
        test_camp.volunteers.add(volunteer_a, volunteer_b, volunteer_c)

        volunteer_count = find_volunteers(test_camp)

        self.assertEqual(volunteer_count, 3)
        self.tearDown()


    def test_unavailable_volunteer_not_counted(self):
        """
        Test case where only deactive volunteers are in the file.
        If this passes, volunteer_count should equal 0, since deactivated volunteers are not counted in this function.
        """
        Plan(name='test_plan5',
             emergency_type=Plan.EmergencyType.EARTHQUAKE,
             description='Test emergency plan',
             geographical_area='London',
             camps=[Camp(name='camp6')])
        volunteer_a = Volunteer(username='yunsy', password='root', firstname='Yunsy', lastname='Yin',
                                phone='+447519953189')
        volunteer_b = Volunteer(username='paul', password='root', firstname='Paul', lastname='Shoemaker',
                                phone='+447519955439')
        volunteer_c = Volunteer(username='gerald', password='root', firstname='Gerald', lastname='Smith',
                                phone='+447511111111')
        test_plan = Plan.find('test_plan5')
        test_camp = test_plan.camps.get('camp6')
        test_camp.volunteers.add(volunteer_a, volunteer_b, volunteer_c)
        volunteer_a.availability = False
        volunteer_b.availability = False
        volunteer_c.availability = False

        volunteer_count = find_volunteers(test_camp)
        self.assertEqual(volunteer_count, 0)
        self.tearDown()


    def test_partially_available_volunteer_count(self):
        """
        Test case where some active and some deactivated volunteers are in the file.
        This test is to make sure that only the active volunteers are counted and the deactivated volunteers
        are disregarded in the count.
        """
        Plan(name='test_plan6',
             emergency_type=Plan.EmergencyType.EARTHQUAKE,
             description='Test emergency plan',
             geographical_area='London',
             camps=[Camp(name='camp7')])
        volunteer_a = Volunteer(username='yunsy', password='root', firstname='Yunsy', lastname='Yin',
                                phone='+447519953189')
        volunteer_b = Volunteer(username='paul', password='root', firstname='Paul', lastname='Shoemaker',
                                phone='+447519955439')
        volunteer_c = Volunteer(username='gerald', password='root', firstname='Gerald', lastname='Smith',
                                phone='+447511111111')
        test_plan = Plan.find('test_plan6')
        test_camp = test_plan.camps.get('camp7')
        test_camp.volunteers.add(volunteer_a, volunteer_b, volunteer_c)
        volunteer_a.availability = False

        volunteer_count = find_volunteers(test_camp)
        self.assertEqual(volunteer_count, 2)
        self.tearDown()


    def test_unavailable_volunteer_not_counted(self):
        """
        Test case where only deactive volunteers are in the file.
        If this passes, volunteer_count should equal 0, since deactivated volunteers are not counted in this function.
        """
        Plan(name='test_plan7',
             emergency_type=Plan.EmergencyType.EARTHQUAKE,
             description='Test emergency plan',
             geographical_area='London',
             camps=[Camp(name='camp8')])
        volunteer_a = Volunteer(username='yunsy', password='root', firstname='Yunsy', lastname='Yin',
                                phone='+447519953189')
        volunteer_b = Volunteer(username='paul', password='root', firstname='Paul', lastname='Shoemaker',
                                phone='+447519955439')
        volunteer_c = Volunteer(username='gerald', password='root', firstname='Gerald', lastname='Smith',
                                phone='+447511111111')
        test_plan = Plan.find('test_plan7')
        test_camp = test_plan.camps.get('camp8')
        test_camp.volunteers.add(volunteer_a, volunteer_b, volunteer_c)
        volunteer_a.availability = False
        volunteer_b.availability = False
        volunteer_c.availability = False

        volunteer_count = find_volunteers(test_camp)
        self.assertEqual(volunteer_count, 0)
        self.tearDown()


    def test_no_volunteers_in_file(self):
        """
        Test case where no volunteers are in the file for a camp.
        In this case, expecting volunteer_count = 0, since there are no volunteers to count.
        """
        Plan(name='test_plan8',
             emergency_type=Plan.EmergencyType.EARTHQUAKE,
             description='Test emergency plan',
             geographical_area='London',
                         camps=[Camp(name='camp9')])
        test_plan = Plan.find('test_plan8')
        test_camp = test_plan.camps.get('camp9')
        volunteer_count = find_volunteers(test_camp)

        self.assertEqual(volunteer_count, 0)
        self.tearDown()


    def test_volunteer_count_multiple_camps(self):
        """
        Test case where only active volunteers are in the file and active volunteers are at multiple camps.
        """
        Plan(name='test_plan8',
             emergency_type=Plan.EmergencyType.EARTHQUAKE,
             description='Test emergency plan',
             geographical_area='London',
             camps=[Camp(name='camp10'), Camp(name='camp11')])
        volunteer_a = Volunteer(username='yunsy', password='root', firstname='Yunsy', lastname='Yin',
                                phone='+447519953189')
        volunteer_b = Volunteer(username='paul', password='root', firstname='Paul', lastname='Shoemaker',
                                phone='+447519955439')
        volunteer_c = Volunteer(username='gerald', password='root', firstname='Gerald', lastname='Smith',
                                phone='+447511111111')
        test_plan = Plan.find('test_plan8')
        test_camp1 = test_plan.camps.get('camp10')
        test_camp1.volunteers.add(volunteer_a)
        test_camp2 = test_plan.camps.get('camp11')
        test_camp2.volunteers.add(volunteer_b, volunteer_c)

        volunteer_count_camp1 = find_volunteers(test_camp1)
        volunteer_count_camp2 = find_volunteers(test_camp2)

        self.assertEqual(volunteer_count_camp1, 1)
        self.assertEqual(volunteer_count_camp2, 2)
        self.tearDown()


class PlanStatisticsRefugeeTest(unittest.TestCase):
    """
    Class for testing cases involving refugee counts in plan statistics.
    """

    def tearDown(self):
        """
        Function to delete stored data after a test has finished running
        to avoid corrupting other tests
        """
        Plan.delete_all()

    def test_refugee_count_single_family(self):
        """
        Test to check that refugee count is correct for a single refugee family.
        """
        Plan(name='test_plan9',
             emergency_type=Plan.EmergencyType.EARTHQUAKE,
             description='Test emergency plan',
             geographical_area='London',
             camps=[Camp(name='camp12')])
        refugee1 = Refugee(firstname="Tom",
                           lastname="Bond",
                           num_of_family_member=6,
                           starting_date=date(2020, 1, 2),
                           medical_condition_type=[Refugee.MedicalCondition.HIV, Refugee.MedicalCondition.CANCER])
        test_plan = Plan.find('test_plan9')
        test_camp = test_plan.camps.get('camp12')
        test_camp.refugees.add(refugee1)

        refugee_count = find_refugees(test_camp)

        self.assertEqual(refugee_count, 6)
        self.tearDown()

    def test_refugee_count_multiple_families_one_camp(self):
        """
        Test to check that refugee count is correct for multiple refugee families at a single camp.
        """
        Plan(name='test_plan10',
             emergency_type=Plan.EmergencyType.EARTHQUAKE,
             description='Test emergency plan',
             geographical_area='London',
             camps=[Camp(name='camp13')])
        refugee1 = Refugee(firstname="Tom",
                           lastname="Bond",
                           num_of_family_member=6,
                           starting_date=date(2020, 1, 2),
                           medical_condition_type=[Refugee.MedicalCondition.HIV, Refugee.MedicalCondition.CANCER])
        refugee2 = Refugee(firstname="Harry",
                           lastname="Ranger",
                           num_of_family_member=1,
                           starting_date=date(2020, 1, 2),
                           medical_condition_type=[Refugee.MedicalCondition.HIV, Refugee.MedicalCondition.CANCER])
        test_plan = Plan.find('test_plan10')
        test_camp = test_plan.camps.get('camp13')
        test_camp.refugees.add(refugee1, refugee2)

        refugee_count = find_refugees(test_camp)

        self.assertEqual(refugee_count, 7)
        self.tearDown()


    def test_refugee_count_multiple_camps(self):
        """
        Test to check that refugee count is correct for a single camp when refugee families exist at multiple
        camps under the same plan.            """
        Plan(name='test_plan11',
             emergency_type=Plan.EmergencyType.EARTHQUAKE,
             description='Test emergency plan',
             geographical_area='London',
             camps=[Camp(name='camp14'), Camp(name='camp15')])
        refugee1 = Refugee(firstname="Tom",
                           lastname="Bond",
                           num_of_family_member=6,
                           starting_date=date(2020, 1, 2),
                           medical_condition_type=[Refugee.MedicalCondition.HIV, Refugee.MedicalCondition.CANCER])
        refugee2 = Refugee(firstname="Harry",
                           lastname="Ranger",
                           num_of_family_member=1,
                           starting_date=date(2020, 1, 2),
                           medical_condition_type=[Refugee.MedicalCondition.HIV, Refugee.MedicalCondition.CANCER])
        test_plan = Plan.find('test_plan11')
        test_camp1 = test_plan.camps.get('camp14')
        test_camp2 = test_plan.camps.get('camp15')
        test_camp2.refugees.add(refugee1, refugee2)


        refugee_count_camp1 = find_refugees(test_camp1)
        refugee_count_camp2 = find_refugees(test_camp2)

        self.assertEqual(refugee_count_camp1, 0)
        self.assertEqual(refugee_count_camp2, 7)
        self.tearDown()


class PlanStatisticsTest(unittest.TestCase):
    """Class for testing cases involving refugee and volunteer counts in plan statistics."""

    def tearDown(self):
        """
        Function to delete stored data after a test has finished running
        to avoid corrupting other tests
        """
        Plan.delete_all()

    def plan_statistics_for_one_camp_test(self):
        """
        Test to check number of volunteers and refugees returned by plan_statistics_function
        for a single camp is correct.
        Also tests the feature to check how many additional volunteers are recommended (number of refugees * 20),
        hence should return 27 in the third list position in the plan_statistics value list.
        """
        Plan(name='test_plan12',
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
        test_plan = Plan.find('test_plan12')
        test_camp = test_plan.camps.get('camp1')
        test_camp.volunteers.add(volunteer_a, volunteer_b, volunteer_c)
        refugee1 = Refugee(firstname="Tom",
                           lastname="Bond",
                           num_of_family_member=600,
                           starting_date=date(2020, 1, 2),
                           medical_condition_type=[Refugee.MedicalCondition.HIV, Refugee.MedicalCondition.CANCER])
        test_camp.refugees.add(refugee1)
        test_plan_statistics = plan_statistics_function(test_plan)
        print(test_plan_statistics)
        test_dictionary = {
            'camp1': [3, 600, 0, 27]
        }
        self.assertDictEqual(test_dictionary, test_plan_statistics)
        self.tearDown()

    def plan_statistics_two_plans_exist_test(self):
        """
        Test to check number of volunteers and refugees returned by plan_statistics_function
        for a single camp is correct, when there is another plan that also exists with volunteers and refugees.
        Also tests where number of volunteers needed is less than the number currently at the camp,
        hence should return 0 extra volunteers required at the end of the plan_statistics dictionary.
        """
        Plan(name='test_plan1',
             emergency_type=Plan.EmergencyType.EARTHQUAKE,
             description='Test emergency plan',
             geographical_area='London',
             camps=[Camp(name='camp1')])
        Plan(name='test_plan2',
             emergency_type=Plan.EmergencyType.EARTHQUAKE,
             description='Test emergency plan',
             geographical_area='London',
             camps=[Camp(name='camp2')])
        volunteer_a = Volunteer(username='yunsy', password='root', firstname='Yunsy', lastname='Yin',
                                phone='+447519953189')
        volunteer_b = Volunteer(username='paul', password='root', firstname='Paul', lastname='Shoemaker',
                                phone='+447519955439')
        volunteer_c = Volunteer(username='gerald', password='root', firstname='Gerald', lastname='Smith',
                                phone='+447511111111')
        test_plan1 = Plan.find('test_plan1')
        test_camp1 = test_plan1.camps.get('camp1')
        test_camp1.volunteers.add(volunteer_a, volunteer_b)
        test_plan2 = Plan.find('test_plan2')
        test_camp2 = test_plan2.camps.get('camp2')
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
        test_camp.refugees.add(refugee1)
        test_plan_statistics1 = plan_statistics_function('test_plan1')
        test_camp.refugees.add(refugee2)
        test_plan_statistics2 = plan_statistics_function('test_plan2')
        print(test_plan_statistics)
        test_dictionary = {
            'camp1': [2, 7, 1, 0]
        }
        self.assertDictEqual(test_dictionary, test_plan_statistics1, test_plan_statistics2)
        self.tearDown()




