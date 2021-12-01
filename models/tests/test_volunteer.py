import unittest
from models.volunteer import Volunteer
from models.plan_statistics import find_volunteers
from models.plan import Plan
from models.plan import Camp


class TestVolunteer(unittest.TestCase):

    def test_create_volunteer(self):
        volunteer_a = Volunteer(username='yunsy', password='root', firstname='Yunsy', lastname='Yin',
                                phone='+447519953189')
        self.assertEqual(type(volunteer_a), Volunteer)

    def test_delete_volunteer(self):
        volunteer_a = Volunteer.find('yunsy')
        volunteer_a.delete()
        self.assertIsNone(Volunteer.find('yunsy'))

    def test_deactivate_volunteer(self):
        volunteer_a = Volunteer(username='yunsy', password='root', firstname='Yunsy', lastname='Yin',
                                phone='+447519953189')
        volunteer_a.accountActivated = False
        volunteer_a.save()
        self.assertFalse(volunteer_a.accountActivated)

    def test_reactivate_volunteer(self):
        volunteer_a = Volunteer(username='yunsy', password='root', firstname='Yunsy', lastname='Yin',
                                phone='+447519953189')
        volunteer_a.accountActivated = True
        volunteer_a.save()
        self.assertTrue(volunteer_a.accountActivated)

    def test_invalid_username(self):
        with self.assertRaises(Volunteer.InvalidUsernameException):
            Volunteer(username='yun', password='root', firstname='Yunsy', lastname='Yin',
                      phone='+447519953189')

    def test_invalid_password(self):
        with self.assertRaises(Volunteer.InvalidPasswordException):
            Volunteer(username='yunsy', password='abc', firstname='Yunsy', lastname='Yin',
                      phone='+447519953189')

    def test_invalid_firstname(self):
        with self.assertRaises(Volunteer.InvalidFirstnameException):
            Volunteer(username='yunsy', password='root', firstname='Y', lastname='Yin',
                      phone='+447519953189')

    def test_invalid_lastname(self):
        with self.assertRaises(Volunteer.InvalidLastnameException):
            Volunteer(username='yunsy', password='root', firstname='Yunsy', lastname='Y',
                      phone='+447519953189')

    def test_invalid_phone_without_international_code(self):
        with self.assertRaises(Volunteer.InvalidPhoneException):
            Volunteer(username='yunsy', password='root', firstname='Yunsy', lastname='Yin',
                      phone='07519953189')

    def test_invalid_phone_too_short(self):
        with self.assertRaises(Volunteer.InvalidPhoneException):
            Volunteer(username='yunsy', password='root', firstname='Yunsy', lastname='Yin',
                      phone='+12345')

    def tearDown(self):
        """
        Function to delete stored data after a test has finished running
        to avoid corrupting other tests
        """
        Plan.delete_all()

    def test_adding_volunteer_to_camp(self):
        """
        Test to check functionality for adding a volunteer to a camp.
        """
        camp = Camp(name='camp1')
        plan = Plan(name='test_plan1',
             emergency_type=Plan.EmergencyType.EARTHQUAKE,
             description='Test emergency plan',
             geographical_area='London',
             camps=[camp])
        volunteer_a = Volunteer(username='yunsy', password='root', firstname='Yunsy', lastname='Yin',
                                phone='+447519953189')
        camp.volunteers.add(volunteer_a)

        self.assertEqual(volunteer_a.camp.name, camp.name)

if __name__ == '__main__':
    unittest.main()
