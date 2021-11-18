import unittest

from models import volunteer
from models.volunteer import Volunteer

class TestVolunteer(unittest.TestCase):

    def test_create_volunteer(self):
        volunteerA = Volunteer(firstname="Yunsy", lastname="Yin", phone="+4477123456", volunteercamp="UCL")
        self.assertEqual(type(volunteerA), Volunteer)

    def test_invalid_firstname(self):
        with self.assertRaises(Volunteer.InvalidFirstnameException):
            Volunteer(firstname="V", lastname="Chan", phone="+4477123456", volunteercamp="UCL")


    def test_invalid_lastname(self):
        with self.assertRaises(Volunteer.InvalidLastnameException):
            Volunteer(firstname="Vanessa", lastname="C", phone="4477123456", volunteercamp="UCL")

    def test_invalid_phone1(self):
        with self.assertRaises(Volunteer.InvalidPhoneException):
            Volunteer(firstname="Yunsy", lastname="Yin", phone="+123", volunteercamp="UCL")

    def test_invalid_phone2(self):
        with self.assertRaises(Volunteer.InvalidPhoneException):
            Volunteer(firstname="Yunsy", lastname="Yin", phone="077123456", volunteercamp="UCL")




if __name__ == '__main__':
    unittest.main()
