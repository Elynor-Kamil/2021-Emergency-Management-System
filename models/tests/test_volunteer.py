import unittest

from models.user import User
from models.volunteer import Volunteer


class TestVolunteer(unittest.TestCase):

    def setUp(self):
        Volunteer.delete_all()

    def test_create_volunteer(self):
        volunteer = Volunteer(username='yunsy', password='root', firstname='Yunsy', lastname='Yin',
                              phone='+447519953189')
        self.assertIsInstance(volunteer, Volunteer)
        self.assertEqual(User.find('yunsy'), volunteer)

    def test_delete_volunteer(self):
        volunteer = Volunteer(username='peter', password='1234', firstname='Peter', lastname='Green',
                              phone='+447519953189')
        volunteer.delete()
        self.assertIsNone(Volunteer.find('peter'))
        self.assertIsNone(User.find('peter'))

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

    def tearDown(self) -> None:
        Volunteer.delete_all()


if __name__ == '__main__':
    unittest.main()
