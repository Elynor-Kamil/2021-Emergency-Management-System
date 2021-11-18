from models.refugee import Refugee
from models.Volunteer import Volunteer

class Camp:
    def __init__(self, name: str):
        self.name = name
        self.refugees = set(Refugee) #Record refugees
        self.volunteers = set(Volunteer) #Record volunteers

    def __str__(self):
        return self.name
