from datetime import date, datetime

class Refugee:
    """
    A class to represent a refugee family.
    """
    def __init__(self,
                 name: str,
                 identificationOfCamp: str,
                 medicalCondition: str,
                 numOfFamilyMember: int,
                 dateOfClosing:None):

        """
        Initialise a new refugee.
        :param name of refugee family
        :param number of family member
        :param identification of campus the refugee family locating
        :param medical condition of the refugee
        :param start date of refugee family creation
        :param closing date of refugee family
        """
        self.name = name
        self.numOfFamilyMember = numOfFamilyMember + 1
        self.identificationOfCamp = identificationOfCamp
        self.medicalCondition = medicalCondition
        self.dateOfCreation = datetime.today().date()
        self.dateOfClosing = dateOfClosing #raise InvalidDateError if closing date has past

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
        if numOfFamilyMember > 1:
            self.numOfFamilyMember = numOfFamilyMember + 1

    def formatIdentificationOfCamp(self, identificationOfCamp):
        """
        format identification camp of refugee
        """
        self.identificationOfCamp = identificationOfCamp

    def formatMedicalCondition(self, medicalCondition): #medical condition types provided or a description?
        """
        format refugee family medical condition
        """
        self.medicalCondition = medicalCondition

    def formatDateOfClosing(self, closingDate: date): #for removing and archive
        """
        format closing date of refugee family
        """
        if datetime.today().date() < closingDate:
            self.dateOfClosing = closingDate
        else:
            pass #raise InvalidDateError


    def __str__(self):
        return f"Refugee family {self.name} located in {self.identificationOfCamp}.\n"\
               f"number of family member: {self.numOfFamilyMember}\n" \
               f"medical condition: {self.medicalCondition}\n" \
               f"creation date: {self.dateOfCreation}\n" \
               f"closing date: {self.dateOfClosing}\n"




r = Refugee("Chan", "London", "severe", 3, date(2022,3,4))
r.formatDateOfClosing(date(2020, 4, 5))
print(r.__str__())


