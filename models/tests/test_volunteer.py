import unittest

from models.camp import Camp
from models.volunteer import Volunteer


class TestVolunteer(unittest.TestCase):

    def test_create_volunteer(self):
        volunteer_a = Volunteer(username='yunsy', password='abc', firstname='Yunsy', lastname="Yin",
                                phone="+4477123456", camp=Camp("UCL"), availability=True)
        self.assertEqual(type(volunteer_a), Volunteer)

    def test_invalid_firstname(self):
        with self.assertRaises(Volunteer.InvalidFirstnameException):
            Volunteer(username='yunsy', password='abc', firstname='Y', lastname="Yin",
                                phone="+4477123456", camp=Camp("UCL"), availability=True)

    def test_invalid_lastname(self):
        with self.assertRaises(Volunteer.InvalidLastnameException):
            Volunteer(username='yunsy', password='abc', firstname='Yunsy', lastname="Y",
                                phone="+4477123456", camp=Camp("UCL"), availability=True)

    def test_invalid_phone1(self):
        with self.assertRaises(Volunteer.InvalidPhoneException):
            Volunteer(username='yunsy', password='abc', firstname='Yunsy', lastname="Yin",
                                phone="+123", camp=Camp("UCL"), availability=True)

    def test_invalid_phone2(self):
        with self.assertRaises(Volunteer.InvalidPhoneException):
            Volunteer(username='yunsy', password='abc', firstname='Yunsy', lastname="Yin",
                                phone="4477123456", camp=Camp("UCL"), availability=True)


if __name__ == '__main__':
    unittest.main()
