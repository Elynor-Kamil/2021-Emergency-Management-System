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
                           num_of_family_member=1,
                           starting_date=date(2020, 1, 2),
                           medical_condition_type=[Refugee.MedicalCondition.HIV, Refugee.MedicalCondition.CANCER])
        self.assertEqual(type(refugee1), Refugee)

    def test_invalid_numOfFamilyMember(self):
        """
        Test number of family member
        """
        with self.assertRaises(Refugee.InvalidNumOfFamilyMemberException):
            Refugee(firstname="Tom",
                    lastname="Bond",
                    num_of_family_member="a",
                    starting_date=date(2020, 1, 2),
                    medical_condition_type=[Refugee.MedicalCondition.HIV])

    def test_invalid_numOfFamilyMember1(self):
        """
        Test number of family member
        """
        with self.assertRaises(Refugee.InvalidNumOfFamilyMemberException):
            Refugee(firstname="Tom",
                    lastname="Bond",
                    num_of_family_member=-10,
                    starting_date=date(2020, 1, 2),
                    medical_condition_type=[Refugee.MedicalCondition.HIV])

    def test_invalid_firstname(self):
        with self.assertRaises(Refugee.InvalidNameException):
            Refugee(firstname="a13",
                    lastname="Bond",
                    num_of_family_member=1,
                    starting_date=date(2020, 1, 2),
                    medical_condition_type=[Refugee.MedicalCondition.HIV])

    def test_invalid_firstname1(self):
        with self.assertRaises(Refugee.InvalidNameException):
            Refugee(firstname=12,
                    lastname="Bond",
                    num_of_family_member=1,
                    starting_date=date(2020, 1, 2),
                    medical_condition_type=[Refugee.MedicalCondition.HIV])

    def test_invalid_lastname(self):
        with self.assertRaises(Refugee.InvalidNameException):
            Refugee(firstname="Tom",
                    lastname="a123",
                    num_of_family_member=1,
                    starting_date=date(2020, 1, 2),
                    medical_condition_type=[Refugee.MedicalCondition.HIV])

    def test_invalid_lastname1(self):
        with self.assertRaises(Refugee.InvalidNameException):
            Refugee(firstname="Tom",
                    lastname=1234567,
                    num_of_family_member=1,
                    starting_date=date(2020, 1, 2),
                    medical_condition_type=[Refugee.MedicalCondition.HIV])

    def test_invalid_startingDate(self):
        with self.assertRaises(Refugee.InvalidStartingDateException):
            Refugee(firstname="Tom",
                    lastname="Bond",
                    num_of_family_member=1,
                    starting_date=date(2023, 1, 2),
                    medical_condition_type=[Refugee.MedicalCondition.HIV])

    def test_invalid_startingDate1(self):
        with self.assertRaises(Refugee.InvalidStartingDateException):
            Refugee(firstname="Tom",
                    lastname="Bond",
                    num_of_family_member=1,
                    starting_date=date(2022, 1, 1),
                    medical_condition_type=[Refugee.MedicalCondition.HIV])
