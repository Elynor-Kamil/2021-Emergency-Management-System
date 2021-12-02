import time
from datetime import date, datetime
from enum import Enum

from models.base.document import Document
from models.base.field import Field


class Refugee(Document):
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

    user_id = Field(primary_key=True)
    firstname = Field()
    lastname = Field()
    num_of_family_member = Field()
    starting_date = Field()
    medical_condition_type = Field()

    def __init__(self,
                 firstname: str,
                 lastname: str,
                 num_of_family_member: int,
                 starting_date: date,
                 medical_condition_type=None):

        """
        :param firstname: firstname of refugee family
        :param lastname: lastname of refugee family
        :param camp: camp of the refugee family locating at
        :param numOfFamilyMember: param number of family member
        :param startingDate: start date of refugee family creation
        :param medicalConditionType: medical condition type of the refugee
        """
        self.__sanitise_name(firstname, lastname)
        super().__init__(user_id=int(time.time()),  # registration timestamp as unique identifier
                         firstname=firstname,
                         lastname=lastname,
                         num_of_family_member=self.__sanitise_num_of_family_member(num_of_family_member),
                         starting_date=self.__sanitise_starting_date(starting_date),
                         medical_condition_type=self.__sanitise_medical_condition_type(medical_condition_type))

    def __sanitise_name(self, firstname, lastname):
        """
        check if name is valid
        """
        if not isinstance(firstname, str) or not isinstance(lastname, str):
            raise self.InvalidNameException()
        elif not firstname.isalpha() or not lastname.isalpha():
            raise self.InvalidNameException()

    def __sanitise_num_of_family_member(self, num_of_family_member):
        """
        check if number of family member is valid
        """
        if not isinstance(num_of_family_member, int) or num_of_family_member < 1:
            raise self.InvalidNumOfFamilyMemberException()
        return num_of_family_member

    def __sanitise_medical_condition_type(self, medical_condition_type):
        """
        check if set(medical_condition_type) is created if medical_condition_type is not None.
        """
        if medical_condition_type:
            return set(medical_condition_type)
        else:
            return set()

    def __sanitise_starting_date(self, starting_date: date):
        """
        check if starting date is valid
        """
        today = datetime.today().date()
        if not starting_date:
            return today
        elif starting_date > today:
            raise self.InvalidStartingDateException()
        return starting_date

    @property
    def camp(self):
        from models.camp import Camp
        return self.find_referred_by(referrer_type=Camp)

    def __str__(self):
        return f"Refugee family {self.firstname} {self.lastname} located in {self.camp}.\n" \
               f"Number of Family Member: {self.num_of_family_member}\n" \
               f"Camp: {self.camp}\n" \
               f"Creation Date: {self.starting_date}\n" \
               f"Medical Condition: {self.medical_condition_type}\n"

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

    class InvalidCampException(Exception):
        """
         Raise exception when the camp entered does not exist.
        """

        def __init__(self, camp):
            super().__init__(f"Camp {camp} does not exist.")