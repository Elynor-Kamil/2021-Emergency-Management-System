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
        refugee1 = Refugee(name="Tom",
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
            Refugee(name="Tom",
                    camp="None",
                    medicalCondition="None",
                    numOfFamilyMember="a")

    def test_invalid_numOfFamilyMember1(self):
        """
        Test number of family member
        """
        with self.assertRaises(Refugee.InvalidNumOfFamilyMemberException):
            Refugee(name="Tom",
                    camp="None",
                    medicalCondition="None",
                    numOfFamilyMember=-10,
                    dateOfClosing=date(2022, 1, 1))

    def test_invalid_closingDate(self):
        """
        Test refugee closing date
        """
        with self.assertRaises(Refugee.InvalidClosingDateException):
            Refugee(name="Tom",
                    camp="None",
                    medicalCondition="None",
                    numOfFamilyMember=1,
                    dateOfClosing=date(2022, 1, 1))


if __name__ == "main":
    unittest.main()
