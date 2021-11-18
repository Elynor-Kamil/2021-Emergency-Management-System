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
                           medicalConditionType=Refugee.MedicalCondition.MAJOR,
                           numOfFamilyMember=1,
                           startingDate= date(2020,1,2))
        self.assertEqual(type(refugee1), Refugee)

    def test_invalid_numOfFamilyMember(self):
        """
        Test number of family member
        """
        with self.assertRaises(Refugee.InvalidNumOfFamilyMemberException):
            Refugee(firstname="Tom",
                    lastname="Bond",
                    camp="None",
                    medicalConditionType=Refugee.MedicalCondition.MAJOR,
                    numOfFamilyMember="a",
                    startingDate= date(2020,1,2))

    def test_invalid_numOfFamilyMember1(self):
        """
        Test number of family member
        """
        with self.assertRaises(Refugee.InvalidNumOfFamilyMemberException):
            Refugee(firstname="Tom",
                    lastname="Bond",
                    camp="None",
                    medicalConditionType=Refugee.MedicalCondition.MAJOR,
                    numOfFamilyMember=-10,
                    startingDate= date(2020,1,2))

    def test_invalid_firstname(self):
        with self.assertRaises(Refugee.InvalidNameException):
            Refugee(firstname="a13",
                    lastname="Bond",
                    camp="None",
                    medicalConditionType=Refugee.MedicalCondition.MAJOR,
                    numOfFamilyMember=1,
                    startingDate= date(2020,1,2))

    def test_invalid_firstname1(self):
        with self.assertRaises(Refugee.InvalidNameException):
            Refugee(firstname=12,
                    lastname="Bond",
                    camp="None",
                    medicalConditionType=Refugee.MedicalCondition.MAJOR,
                    numOfFamilyMember=1,
                    startingDate= date(2020,1,2))

    def test_invalid_lastname(self):
        with self.assertRaises(Refugee.InvalidNameException):
            Refugee(firstname="Tom",
                    lastname="a123",
                    camp="None",
                    medicalConditionType=Refugee.MedicalCondition.MAJOR,
                    numOfFamilyMember=1,
                    startingDate= date(2020,1,2))

    def test_invalid_lastname1(self):
        with self.assertRaises(Refugee.InvalidNameException):
            Refugee(firstname="Tom",
                    lastname=1234567,
                    camp="None",
                    medicalConditionType=Refugee.MedicalCondition.MAJOR,
                    numOfFamilyMember=1,
                    startingDate= date(2020,1,2))

    def test_invalid_startingDate(self):
        with self.assertRaises(Refugee.InvalidStartingDateException):
            Refugee(firstname="Tom",
                    lastname="Bond",
                    camp="None",
                    medicalConditionType=Refugee.MedicalCondition.MAJOR,
                    numOfFamilyMember=1,
                    startingDate=date(2023, 1, 2))

    def test_invalid_startingDate1(self):
        with self.assertRaises(Refugee.InvalidStartingDateException):
            Refugee(firstname="Tom",
                    lastname="Bond",
                    camp="None",
                    medicalConditionType=Refugee.MedicalCondition.MAJOR,
                    numOfFamilyMember=1,
                    startingDate=date(2022, 1, 1))

if __name__ == "main":
    unittest.main()
