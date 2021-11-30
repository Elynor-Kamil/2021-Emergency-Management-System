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
                           identificationOfCamp="None",
                           medicalCondition="None",
                           numOfFamilyMember="1",
                           dateOfClosing=date(2022, 1, 1))
        self.assertEqual(type(refugee1), Refugee)

    def test_invalid_name(self):