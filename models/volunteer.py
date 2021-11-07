import datetime

class Volunteer:
    """

    """
    def __init__(self,
                 name: str,
                 phone: str,
                 volunteercamp: str,
                 availability: bool):
        currentdate = datetime.datetime.now()


        self.name = name
        self.phone = phone
        self.camp = volunteercamp
        self.availability = availability
        self.creationdate = currentdate.date()


    def changeVolunteerName(self, newName):
        self.name = newName

    def changeVolunteerPhone(self,newPhone):
        self.phone = newPhone

    def changeAvailability(self, newStatus):
        self.availability = newStatus


    def __str__(self):
        return f"Volunteer {self.name} belongs to camp {self.camp}. Joined date: {self.creationdate}"

if __name__ == "__main__":

    volunteerA = Volunteer(name="Vanessa", phone="+4477123456", volunteercamp="UCL", availability=True)
    print(volunteerA)