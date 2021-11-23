import datetime, re
from models.base.document import IndexedDocument
from models.base.field import Field


class Volunteer(IndexedDocument):
    username = Field(primary_key=True)
    password = Field()
    accountActivated = Field()
    firstname = Field()
    lastname = Field()
    phone = Field()
    availability = Field()
    creationDate = Field()

    def __init__(self,
                 username: str,
                 password: str,
                 firstname: str,
                 lastname: str,
                 phone: str,
                 accountActivated=True,
                 availability=True):

        """
        Initialize a new volunteer account.
        :param username: username of the volunteer account
        :param password: password of the volunteer account
        :param accountActivated: activation status of the volunteer account
        :param firstname: the firstname of the volunteer
        :param lastname: the lastname of the volunteer
        :param phone: the phone number of the volunteer (only numbers with international code are accepted)
        :param availability:  whether the volunteer is available to join a new emergency plan
        """

        self.__checkVolunteerUsername(username)
        self.__checkVolunteerPassword(password)
        self.__checkVolunteerName(firstname, lastname)
        self.__checkVolunteerPhone(phone)

        super().__init__(username=username,
                         password=password,
                         accountActivated=accountActivated,
                         firstname=firstname,
                         lastname=lastname,
                         phone=phone,
                         availability=availability,
                         creationDate=datetime.datetime.now().date())

    def __checkVolunteerUsername(self, username):
        if len(username) < 4:
            raise self.InvalidUsernameException(username)

    def __checkVolunteerPassword(self, password):
        if len(password) < 4:
            raise self.InvalidPasswordException(password)

    def __checkVolunteerName(self, firstname, lastname):
        if len(firstname) <= 1:
            raise self.InvalidFirstnameException(firstname)
        elif len(lastname) <= 1:
            raise self.InvalidLastnameException(lastname)

    def __checkVolunteerPhone(self, phone):
        phoneText = "\+(9[976]\d|8[987530]\d|6[987]\d|5[90]\d|42\d|3[875]\d|2[98654321]\d|9[8543210]|8[6421]|6[6543210]|5[87654321]|4[987654310]|3[9643210]|2[70]|7|1)\d{5,14}$"
        if not re.search(phoneText, phone):
            raise self.InvalidPhoneException(phone)

    @property
    def camp(self):
        from models.camp import Camp
        return self.find_referred_by(referrer_type=Camp)

    def __str__(self):
        return f"Volunteer username: {self.username}\n" \
               f"Account activated: {self.accountActivated}\n" \
               f"Volunteer {self.firstname} {self.lastname} belongs to camp {self.camp}.\n" \
               f"Phone Number: {self.phone}\n" \
               f"Availability: {self.availability}\n" \
               f"Date joined: {self.creationDate}\n"

    class InvalidUsernameException(Exception):
        """
         Raise exception when the username entered is less than 4 characters.
        """

        def __init__(self, username):
            super().__init__(f"Invalid username: {username}. Username should be at least 4 characters.")

    class InvalidPasswordException(Exception):
        """
         Raise exception when the password entered is less than 4 characters.
        """

        def __init__(self, password):
            super().__init__(f"Invalid password: {password}. Password should be at least 4 characters.")

    class InvalidFirstnameException(Exception):
        """
         Raise exception when the firstname entered is too short.
        """

        def __init__(self, firstname):
            super().__init__(f"Invalid name: {firstname}. First name should be more than 1 character.")

    class InvalidLastnameException(Exception):
        """
         Raise exception when the lastname entered is too short.
        """

        def __init__(self, lastname):
            super().__init__(f"Invalid name: {lastname}. Last name should be more than 1 character.")

    class InvalidPhoneException(Exception):
        """
         Raise exception when the phone number is invalid (length, no country code).
        """

        def __init__(self, phone):
            super().__init__(f"Invalid phone number: {phone}.")
