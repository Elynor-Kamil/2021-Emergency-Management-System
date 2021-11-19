from datetime import date, datetime
from enum import Enum

class Refugee:
    """
    A class to represent a refugee family.
    """
    class MedicalCondition(Enum):
        CANCER = "Cancer"
        CHRONICKIDNEY = "Chronic kidney disease"
        CHRONICLIVER = "Chronic liver disease"
        CHRONICLUNG = "Chronic lung diseases"
        DEMENTIA_OR_NEUROLOGICAL = "Dementia or other neurological conditions"
        DIABETES = "Diabetes"
        DOWNSYNDROME = "Down Syndrome"
        HEART = "Heart conditions"
        HIV = "HIV infection"
        IMMUNOCOMPROMISED = "Immunocompromised state (weakened immune system)"
        MENTALHEALTH = "Mental health conditions"
        OVERWEIGHT_OR_OBESITY = "Overweight and obesity"
        PREGNANCY = "Pregnancy"
        SICKLECELL_OR_THALASSEMIA = "Sickle cell or thalassemia"
        SMOKING = "Smoking, current or former"
        TRANSPLANT = "Solid organ or blood stem cell transplant"
        STROKE_OR_CEREBROVASCULAR = "Stroke or cerebrovascular disease, which affects blood flow to the brain"
        SUBSTANCE_USE = "Substance use disorders"
        TUBERCULOSIS = "Tuberculosis"
        OTHERS = "Others"

    def __init__(self,
                 firstname: str,
                 lastname:str,
                 camp: str,
                 numOfFamilyMember: int,
                 startingDate:date,
                 medicalConditionType=None):

        """
        :param firstname: firstname of refugee family
        :param lastname: lastname of refugee family
        :param camp: camp of the refugee family locating at
        :param numOfFamilyMember: param number of family member
        :param startingDate: start date of refugee family creation
        :param medicalConditionType: medical condition type of the refugee
        """

        self.name = self.__sanitise_name(firstname, lastname)
        self.numOfFamilyMember = self.__sanitise_num_of_family_member(numOfFamilyMember)
        self.camp = camp
        self.startingDate = self.__sanitise_starting_date(startingDate)
        self.medicalConditionType : set[self.MedicalCondition] = set(medicalConditionType)

    def __sanitise_name(self, firstname, lastname):
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


    def __sanitise_num_of_family_member(self, numOfFamilyMember):
        """
        check if number of family member is valid
        """
        if not isinstance(numOfFamilyMember, int) or numOfFamilyMember < 1:
            raise self.InvalidNumOfFamilyMemberException()
        return numOfFamilyMember

    def __sanitise_medical_condition_type(self, medicalConditionType):
        """
        check if no other options is being selected if None option is chosen.
        """
        list = []
        for medicalCondition.value in medicalConditionType:
            list.append(medicalCondition)
        if len(medicalConditionType) > 1:
            raise self.invalidMedicalConditionTypeException()
        return medicalConditionType

    def __sanitise_starting_date(self, startingDate: date):  # for removing and archive
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
               f"Creation Date: {self.startingDate}\n" \
               f"Medical Condition: {self.medicalConditionType}\n"\


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