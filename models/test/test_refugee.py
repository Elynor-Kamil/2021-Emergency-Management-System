import unittest
from datetime import date

from models.refugee import Refugee

class RefugeeTest(unittest.TestCase):
    """
    Test Refugee class
    """

    def test_create_refugee(self):
        """
        Test Refugee creation
        """
        refugee1 = Refugee(firstname="Tom",
                           lastname="Bond",
                           camp="None",
                           medicalCondition="None",
                           numOfFamilyMember=0,
                           dateOfClosing=date(2022, 1, 1))
        self.assertEqual(type(refugee1), Refugee)

    def test_invalid_numOfFamilyMember(self):
        """
        Test number of family member
        """
        with self.assertRaises(Refugee.InvalidNumOfFamilyMemberException):
            Refugee(firstname="Tom",
                    lastname="Bond",
                    camp="None",
                    medicalCondition="None",
                    numOfFamilyMember="a")

    def test_invalid_numOfFamilyMember1(self):
        """
        Test number of family member
        """
        with self.assertRaises(Refugee.InvalidNumOfFamilyMemberException):
            Refugee(firstname="Tom",
                    lastname="Bond",
                    camp="None",
                    medicalCondition="None",
                    numOfFamilyMember=-10,
                    dateOfClosing=date(2022, 1, 1))

    def test_invalid_closingDate(self):
        """
        Test refugee closing date
        """
        with self.assertRaises(Refugee.InvalidClosingDateException):
            Refugee(firstname="Tom",
                    lastname="Bond",
                    camp="None",
                    medicalCondition="None",
                    numOfFamilyMember=1,
                    dateOfClosing=date(2020, 1, 1))

    def test_invalid_firstname(self):
        with self.assertRaises(Refugee.InvalidNameException):
            Refugee(firstname="a13",
                    lastname="Bond",
                    camp="None",
                    medicalCondition="None",
                    numOfFamilyMember=1,
                    dateOfClosing=date(2022, 1, 1))

    def test_invalid_firstname1(self):
        with self.assertRaises(Refugee.InvalidNameException):
            Refugee(firstname=12,
                    lastname="Bond",
                    camp="None",
                    medicalCondition="None",
                    numOfFamilyMember=1,
                    dateOfClosing=date(2022, 1, 1))

    def test_invalid_lastname(self):
        with self.assertRaises(Refugee.InvalidNameException):
            Refugee(firstname="Tom",
                    lastname="a123",
                    camp="None",
                    medicalCondition="None",
                    numOfFamilyMember=1,
                    dateOfClosing=date(2022, 1, 1))

    def test_invalid_lastname1(self):
        with self.assertRaises(Refugee.InvalidNameException):
            Refugee(firstname="Tom",
                    lastname=1234567,
                    camp="None",
                    medicalCondition="None",
                    numOfFamilyMember=1,
                    dateOfClosing=date(2022, 1, 1))

if __name__ == "main":
    unittest.main()
