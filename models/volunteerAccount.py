import datetime
from models import camp


class Volunteer:
    """
    A class used to represent a volunteer.
    """

    def __init__(self, firstname: str,
                 lastname: str,
                 phone: str,
                 volunteercamp: list,
                 availability = True):
        """
           Initialize a new volunteer.
           :param firstname: the firstname of the volunteer
           :param lastname: the lastname of the volunteer
           :param phone: the phone number of the volunteer
           :param volunteercamp: the camp that the volunteer belongs to
           :param availability:  whether the volunteer is available to join a new emergency plan
           :param creationdate: the date that this volunteer is created
           """
        currentdate = datetime.datetime.now()

        self.name = self.__checkVolunteerName(firstname, lastname)
        self.phone = self.__checkVolunteerPhone(phone)
        self.camp = volunteercamp
        self.availability = availability
        self.creationdate = currentdate.date()


    def __checkVolunteerName(self, firstname, lastname):
        if len(firstname) <= 1:
            raise self.InvalidFirstnameException(firstname)
        elif len(lastname) <= 1:
            raise self.InvalidLastnameException(lastname)
        name = f"({firstname}+' '+{lastname})
        return name

    def __checkVolunteerPhone(self, phone):
        if phone[0] != "+":
            raise self.InvalidPhoneException("Phone should include country code and be in format \"+XXXXXXXXXXX\".")
        elif len(phone) < 5:
            raise self.InvalidPhoneException("The phone number is too short.")
        return phone

    def changeCamp(self, newcamp):
        if newcamp not in camp.Camp.camps:
            raise self.InvalidCampException(newcamp)
        self.camp = newcamp


    def changeAvailability(self):
        self.availability = not (self.availability)



    def __str__(self):
        return f"Volunteer {self.name} belongs to camp {self.camp}.\n" \
               f"Phone Number: {self.phone}\n" \
               f"Availability: {self.availability}\n" \
               f"Joined date: {self.creationdate}\n"


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








def createVolunteerAccount():
    volunteerAccount_file = open('volunteerAccount.txt', 'a')
    volunteerAccount_dict = {}
    volunteerAccount_dict_newUsername = input('New Volunteer Username: ')
    volunteerAccount_dict[volunteerAccount_dict_newUsername] = input('New Volunteer Password: ')
    print(volunteerAccount_dict)
    pickle.dump(volunteerAccount_dict, volunteerAccount_file)

    '''

    for k, v in volunteerAccount_dict.items():
        volunteerAccount_file.write(str(k)+' '+str(v)+'\n')
    volunteerAccount_file.close()
    volunteerAccount_file = open('volunteerAccount.txt', 'r')
    for line in volunteerAccount_file:
        line = line.strip()
        k = line.split(' ')[0]
        v = line.split(' ')[1]
        volunteerAccount_dict[k] = v
        
    
    
    volunteerAccount_file.close()
    name = input('Volunteer Name: ')
    phone = input('Volunteer Phone Number: ')
    volunteer = Volunteer(name, phone, volunteercamp="UCL", availability=True)
    print(volunteer)
    '''


if __name__ == "__main__":
    createVolunteerAccount()