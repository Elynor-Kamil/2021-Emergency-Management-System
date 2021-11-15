import unittest

from models import volunteer
from models.volunteer import Volunteer

class TestVolunteer(unittest.TestCase):

    def test_create_volunteer(self):
        volunteerA = Volunteer(name="Yunsy", phone="+4477123456", volunteercamp="UCL")
        self.assertEqual(type(volunteerA), Volunteer)

    def test_invalid_name(self):
        with self.assertRaises(Volunteer.InvalidNameException):
            Volunteer(name="V", phone="+4477123456", volunteercamp="UCL")


    def test_invalid_phone1(self):
        with self.assertRaises(Volunteer.InvalidPhoneException):
            Volunteer(name="Vanessa", phone="4477123456", volunteercamp="UCL")

    def test_invalid_phone2(self):
        with self.assertRaises(Volunteer.InvalidPhoneException):
            Volunteer(name="Vanessa", phone="+123", volunteercamp="UCL")




if __name__ == '__main__':
    unittest.main()
