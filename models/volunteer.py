import datetime

class Volunteer:
    """
    A class used to represent a volunteer.

    Attributes
    ----------
    name : str
        the name of the volunteer
    phone : str
        the phone number of the volunteer
    volunteercamp : string
        the camp that the volunteer belongs to
    availability: boolean
        whether the is available to be involved in a new plan
    creationdate : date
        the date when the volunteer account is created


    Methods
    -------
    changeVolunteerName(newName)
        change the name of the volunteer and check if the new name is valid
    changeVolunteerName(newPhone)
        change the phone number of the volunteer
    """

    def __init__(self,
                 name: str,
                 phone: str,
                 volunteercamp: list,
                 availability = True):
        currentdate = datetime.datetime.now()


        self.name = name
        self.phone = phone
        self.camp = volunteercamp
        self.availability = availability
        self.creationdate = currentdate.date()


    def changeVolunteerName(self, newName):
        if len(newName) > 1:
            self.name = newName
        else:
            pass #ask to re-enter valid name

    def changeVolunteerPhone(self,newPhone):
        self.phone = newPhone

    def changeAvailability(self):
        self.availability = False

    def changeCamp(self, newCamp):
        self.camp = newCamp
        #if newCamp not in self.camp:
        #    self.camp.append(newCamp)

    def removeCamp(self, camp):
        if camp in self.camp:
            self.camp.remove(camp)

    def __str__(self):
        return f"Volunteer {self.name} belongs to camp {self.camp}.\n" \
               f"Phone Number: {self.phone}\n" \
               f"Availability: {self.availability}\n" \
               f"Joined date: {self.creationdate}\n"

if __name__ == "__main__":

    volunteerA = Volunteer(name="Vanessa", phone="+4477123456", volunteercamp="UCL")
    print(volunteerA)
    volunteerA.changeCamp("UCL2")
    print(volunteerA)

def createVolunteerAccount():
    volunteerAccount_file = open('volunteerAccount.txt', 'a')
    volunteerAccount_dict = {}
    volunteerAccount_dict_newUsername = input('New Volunteer Username: ')
    volunteerAccount_dict[volunteerAccount_dict_newUsername] = input('New Volunteer Password: ')
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

if __name__ == "__main__":
    createVolunteerAccount()