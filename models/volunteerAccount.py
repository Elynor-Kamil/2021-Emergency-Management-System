
import datetime
from models import camp
from models.base.document import IndexedDocument
from models.base.field import Field

class volunteer(IndexedDocument):
    username = Field(primary_key=True)
    password = Field()
    firstname = Field()
    lastname = Field()
    phone = Field()
    camp = Field()
    availability = Field()
    creationdate = Field()

    def __init__(self,
                 username: str,
                 password: str,
                 firstname: str,
                 lastname: str,
                 phone: str,
                 camp: list,
                 availability = True):

        """
        Initialize a new volunteer account.
        :param username: username of the volunteer account
        :param password: password of the volunteer account
        :param firstname: the firstname of the volunteer
        :param lastname: the lastname of the volunteer
        :param phone: the phone number of the volunteer (only numbers with international code are accepted)
        :param camp: the camp that the volunteer belongs to
        :param availability:  whether the volunteer is available to join a new emergency plan
        :param creationdate: the date that this volunteer is created
        """

        self.__checkVolunteerUsername(username)
        self.__checkVolunteerPassword(password)
        self.__checkVolunteerName(firstname, lastname)
        self.__checkVolunteerPhone(phone)

        super().__init__(username=username,
                         password=password,
                         firstname=firstname,
                         lastname=lastname,
                         phone=phone,
                         camp=camp,
                         availability=availability,
                         creationdate=datetime.datetime.now().date())


    def __checkVolunteerUsername(self, username):
        if len(username) <= 1:
            raise self.InvalidUsernameException(username)

    def __checkVolunteerPassword(self, password):
        if len(password) <= 1:
            raise self.InvalidPasswordException(password)

    def __checkVolunteerName(self, firstname, lastname):
        if len(firstname) <= 1:
            raise self.InvalidFirstnameException(firstname)
        elif len(lastname) <= 1:
            raise self.InvalidLastnameException(lastname)

    def __checkVolunteerPhone(self, phone):
        if phone[0] != "+":
            raise self.InvalidPhoneException("Phone should include country code and be in format \"+XXXXXXXXXXX\".")
        elif len(phone) < 5:
            raise self.InvalidPhoneException("The phone number is too short.")

    def changeCamp(self, newcamp):
        if newcamp not in camp.Camp.camps:
            raise self.InvalidCampException(newcamp)
        self.camp = newcamp

    def changeAvailability(self):
        self.availability = not (self.availability)


    def __str__(self):
        return f"Volunteer username: {self.username}\n" \
               f"Volunteer {self.firstname} {self.lastname} belongs to camp {self.camp}.\n" \
               f"Phone Number: {self.phone}\n" \
               f"Availability: {self.availability}\n" \
               f"Date joined: {self.creationdate}\n"


    class InvalidUsernameException(Exception):
        """
         Raise exception when the username entered is too short.
        """

        def __init__(self, username):
            super().__init__(f"Invalid username: {username}. Username should be more than 1 character.")


    class InvalidPasswordException(Exception):
        """
         Raise exception when the password entered is too short.
        """

        def __init__(self, password):
            super().__init__(f"Invalid password: {password}. Password should be more than 1 character.")


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

        def __init__(self, msg):
            super().__init__(msg)


    class InvalidCampException(Exception):
        """
         Raise exception when the camp entered does not exist.
        """

        def __init__(self, camp):
            super().__init__(f"Camp {camp} does not exist.")



volunteerA = volunteer(username='yunsy', password='root', firstname='Yunsy', lastname='Yin', phone='+012345', camp='UCL')
print(volunteerA)

volunteerA.firstname = 'Yun-Tzu'
volunteerA.save()
print(volunteerA)

# print(volunteer.all())
# print(volunteer.find('yunsy'))
# volunteer.delete()
print(volunteer.find('yunsy'))
