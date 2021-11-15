from datetime import date, datetime

class Refugee:
    """
    A class to represent a refugee family.
    """
    def __init__(self,
                 name: str,
                 camp: str,
                 medicalCondition: str,
                 numOfFamilyMember: int,
                 dateOfClosing=None):

        """
        Initialise a new refugee.
        :param name of refugee family
        :param number of family member
        :param camp of the refugee family locating at
        :param medical condition of the refugee
        :param start date of refugee family
        :param closing date of refugee family
        """
        self.name = name
        self.numOfFamilyMember = numOfFamilyMember + 1
        self.camp =camp
        self.medicalCondition = medicalCondition
        self.dateOfCreation = datetime.today().date()
        self.dateOfClosing = dateOfClosing

    def formatName(self, name):
        """
        format name to a new name
        """
        self.name = name
        #error handling if invalid name is inputed

    def formatNumOfFamilyMember(self, numOfFamilyMember):
        """
        format number of family member
        """
        if numOfFamilyMember is not int or numOfFamilyMember < 0:
            raise self.InvalidNumIfFamilyMemberException()
        self.numOfFamilyMember = numOfFamilyMember + 1

    def formatCamp(self, newCamp):
        """
        format identification camp of refugee
        """
        if newCamp not in camp.Camp.camps:
            raise self.InvalidCampException(newCamp)
        self.camp = newCamp

    def formatMedicalCondition(self, medicalCondition): #medical condition types provided or a description?
        """
        format refugee family medical condition
        """
        self.medicalCondition = medicalCondition

    def formatDateOfClosing(self, dateOfClosing: date): #for removing and archive
        """
        format closing date of refugee family
        """
        today = datetime.today().date()
        if today >= dateOfClosing:
            raise self.InvalidClosingDateException()
        self.dateOfClosing = dateOfClosing


    def __str__(self):
        return f"Refugee family {self.name} located in {self.camp}.\n"\
               f"number of family member: {self.numOfFamilyMember}\n" \
               f"medical condition: {self.medicalCondition}\n" \
               f"creation date: {self.dateOfCreation}\n" \
               f"closing date: {self.dateOfClosing}\n"


    class InvalidNumOfFamilyMemberException(Exception):
        """
        Raise exception when number of family member entered.
        """
        def __init__(self):
            super().__init__(f"Invalid number of family member. Family member must be an positive integer.")


    class InvalidCampException(Exception):
        """
        Raise exception when camp entered does not exist.
        """

        def __init__(self, camp):
            super().__init__(f"Camp {camp} does not exist.")


    class InvalidClosingDateException(Exception):
        """
        Raise exception when the close date is invalid.
        """
        def __init__(self):
            super().__init__(f"Invalid closing date. Closing date must be after current date.")









r = Refugee("Chan", "London", "severe", 3, date(2022,3,4))
r.formatDateOfClosing(date(2020, 4, 5))
print(r.__str__())



