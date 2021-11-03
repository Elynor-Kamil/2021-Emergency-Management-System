class Refugee:
    def __init__(self, familyName, familyMember):
        self.familyName = familyName
        self.familyMember = familyMember

    def findFamilyMember(self):
        return self.familyMember

    def changeFamilyMember(self, familyMemberName):
        self.familyMember()

    def __str__(self):
        return self.family

family = Refugee("Chan", 3)

print(family.findFamilyMember())





    