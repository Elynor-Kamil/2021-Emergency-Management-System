from datetime import date, datetime
from enum import Enum

class Refugee:
    """
    A class to represent a refugee family.
    """
    class MedicalCondition(Enum):
        MINOR = "minor"
        MAJOR = "major"
        MODERATE = "moderate"
        EXTREME = "extreme"

    class MissingMedicalConditionError(Exception):
        """
        It is mandatory to supply one medical condition only.
        When no medical condition is provided, this exception will be raised.
        """
        def __init__(self):
            super().__init__(f"It is mandatory to provide only one medical condition")


    def __init__(self,
                 firstname: str,
                 lastname:str,
                 camp: str,
                 medicalConditionType: MedicalCondition,
                 numOfFamilyMember: int,
                 startingDate=datetime.today().date()):

        """
        :param firstname: firstname of refugee family
        :param lastname: lastname of refugee family
        :param camp: camp of the refugee family locating at
        :param medicalConditionType: medical condition type of the refugee
        :param numOfFamilyMember: param number of family member
        :param startingDate: start date of refugee family creation
        """

        self.name = self.__checkName(firstname, lastname)
        self.numOfFamilyMember = self.__checkNumOfFamilyMember(numOfFamilyMember)
        self.camp = camp
        self.medicalConditionType = medicalConditionType
        self.startingDate = self.__checkStartingDate(startingDate)


    def __checkName(self, firstname, lastname):
        """
        check if name is valid
        """
        if not isinstance(firstname, str) or not isinstance(lastname, str):
            raise self.InvalidNameException()
        elif not firstname.isalpha() or not lastname.isalpha():
            raise self.InvalidNameException()
        else:
            fullname = firstname + " " + lastname
            return fullname


    def __checkNumOfFamilyMember(self, numOfFamilyMember):
        """
        check if number of family member is valid
        """
        if not isinstance(numOfFamilyMember, int) or numOfFamilyMember < 1:
            raise self.InvalidNumOfFamilyMemberException()
        return numOfFamilyMember


    def __checkStartingDate(self, startingDate: date):  # for removing and archive
        """
        check if starting date is valid
        """
        today = datetime.today().date()
        if not startingDate:
            return today
        elif startingDate > today:
            raise self.InvalidStartingDateException()
        return startingDate


    def __str__(self):
        return f"Refugee family {self.name} located in {self.camp}.\n"\
               f"Number of Family Member: {self.numOfFamilyMember}\n" \
               f"Camp: {self.camp}\n" \
               f"Medical Condition: {self.medicalConditionType}\n" \
               f"Creation Date: {self.startingDate}\n" \


    class InvalidNumOfFamilyMemberException(Exception):
        """
        Raise exception when number of family member entered.
        """
        def __init__(self):
            super().__init__(f"Invalid input: the number of family members must be a positive integer.")

    class InvalidNameException(Exception):
        """
        Raise exception when the firstname or/and lastname is invalid.
        """
        def __init__(self):
            super().__init__(f"Invalid name. The firstname and lastname must be alphabets.")


    class InvalidStartingDateException(Exception):
        """
        Raise exception when the start date is invalid.
        """

        def __init__(self):
            super().__init__(f"Invalid starting date. Starting date must be before/on current date.")