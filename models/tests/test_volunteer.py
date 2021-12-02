import unittest
from models.volunteer import Volunteer


class TestVolunteer(unittest.TestCase):

    def test_create_volunteer(self):
        volunteer = Volunteer(username='yunsy', password='root', firstname='Yunsy', lastname='Yin',
                              phone='+447519953189')
        self.assertIsInstance(volunteer, Volunteer)

    def test_delete_volunteer(self):
        volunteer = Volunteer.find('yunsy')
        volunteer.delete()
        self.assertIsNone(Volunteer.find('yunsy'))

    def test_deactivate_volunteer(self):
        volunteer = Volunteer(username='yunsy', password='root', firstname='Yunsy', lastname='Yin',
                              phone='+447519953189')
        volunteer.account_activated = False
        volunteer.save()
        self.assertFalse(volunteer.account_activated)

    def test_reactivate_volunteer(self):
        volunteer = Volunteer(username='yunsy', password='root', firstname='Yunsy', lastname='Yin',
                              phone='+447519953189')
        volunteer.account_activated = True
        volunteer.save()
        self.assertTrue(volunteer.account_activated)

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


if __name__ == '__main__':
    unittest.main()
