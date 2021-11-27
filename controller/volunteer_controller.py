from models.volunteer import Volunteer
from models.camp import Camp
from interfaces.cli import EmsShell


###---- Manage Volunteer Menu ----
def manage_volunteer_menu():
    print("""
         1) Create new volunteer accounts
         2) View volunteers
         3) Edit volunteer profiles
         4) Deactivate volunteer accounts
         5) Re-activate volunteer accounts
         6) Delete volunteer accounts

         R) Return to previous page
         """)


def find_volunteer(username: str) -> Volunteer:
    volunteer_called = Volunteer.find(username)
    return volunteer_called


def create_volunteer(username: str,
                     password: str,
                     firstname: str,
                     lastname: str,
                     phone: str,
                     camp: Camp) -> Volunteer:
    Volunteer(username=username, password=password, firstname=firstname, lastname=lastname, phone=phone)
    Volunteer.camp = camp


def view_volunteer_profile(volunteer: Volunteer) -> str:
    print(volunteer)


def deactivate_volunteer(username:str) -> Volunteer:
    volunteer_called = find_volunteer(username)
    volunteer_called.account_activated = False
    volunteer_called.save()


def reactivate_volunteer(username:str) -> Volunteer:
    volunteer_called = find_volunteer(username)
    volunteer_called.account_activated = True
    volunteer_called.save()


def delete_volunteer(username:str) -> None:
    volunteer_called = find_volunteer(username)
    volunteer_called.camp = None
    volunteer_called.delete()


class EditVolunteerProfileMenu(EmsShell):
    def __init__(self):
        super(EditVolunteerProfileMenu, self).__init__()

    def edit_volunteer_profile_menu(self) -> None:
        print("""
             Select the item you'd like to edit:
             1) Firstname
             2) Lastname
             3) Phone number
             4) Camp
             5) Availability
    
             R) Return to previous page
             """)

    def precmd(self, option: str) -> int:
        edit_volunteer_profile_options = {
            "edit firstname": 1,
            "edit lastname": 2,
            "edit phone": 3,
            "edit camp": 4,
            "edit availability": 5,
            "return": "r"}
        if option.isdigit():
            return list(edit_volunteer_profile_options.keys())[
                list(edit_volunteer_profile_options.values()).index(int(option))]
        elif option == "r" or "R":
            return list(edit_volunteer_profile_options.keys())[
                list(edit_volunteer_profile_options.values()).index(option.lower())]
        else:
            pass

    def do_edit_firstname(self):
        username = input("Username: ")
        firstname = input(f"Original firstname is {find_volunteer(username).firstname}. New firstname: ")
        volunteer_called = find_volunteer(username)
        volunteer_called.firstname = firstname
        volunteer_called.save()
        print(f"Updated successfully! New firstname is {find_volunteer(username).firstname}.")

    def do_edit_lastname(self):
        username = input("Username: ")
        lastname = input(f"Original lastname is {find_volunteer(username).lastname}. New lastname: ")
        volunteer_called = find_volunteer(username)
        volunteer_called.lastname = lastname
        volunteer_called.save()
        print(f"Updated successfully! New lastname is {find_volunteer(username).lastname}.")

    def do_edit_phone(self):
        username = input("Username: ")
        phone = input(f"Original phone number is {find_volunteer(username).phone}. New phone number: ")
        volunteer_called = find_volunteer(username)
        volunteer_called.phone = phone
        volunteer_called.save()
        print(f"Updated successfully! New phone number is {find_volunteer(username).phone}.")

    def do_edit_camp(self):
        username = input("Username: ")
        camp = input(f"Original assigned camp is {find_volunteer(username).camp}. New assigned camp: ")
        volunteer_called = find_volunteer(username)
        volunteer_called.camp = camp
        volunteer_called.save()
        print(f"Updated successfully! New assigned camp is {find_volunteer(username).camp}.")

    def do_edit_availability(self):
        username = input("Username: ")
        availability = input(f"Original availability is {find_volunteer(username).availability}. Switch it to: ")
        volunteer_called = find_volunteer(username)
        volunteer_called.availability = availability
        volunteer_called.save()
        print(f"Updated successfully! The availability is now {find_volunteer(username).availability}.")


'''

volunteer_a = create_volunteer(username='yunsy', password='root', firstname='Yunsy', lastname='Yin',
                               phone='+447519953189', camp=Camp(name='UCL'))
volunteer_b = find_volunteer("yunsy")
print(volunteer_b)
print(type(volunteer_b))
print(volunteer_b.firstname)
print(find_volunteer("yunsy"))
print(find_volunteer("yunsy").firstname)


# print(type(volunteer_b))
# print(volunteer_b_firstname)
# print(type(volunteer_b.camp))
# print(volunteer_b.camp)
# view_volunteer_profile(volunteer_b)

'''


def edit_volunteer_profile(volunteer: Volunteer, firstname: str, lastname: str, phone: str) -> Volunteer:
    """
    Yunsy, Yingbo
    A function used by admin and volunteer
    Should include re-assign volunteer to a camp
    """
    pass


def change_volunteer_camp(volunteer: Volunteer, camp: Camp, is_admin: bool) -> Volunteer:
    """
    The admin role
    :param is_admin: if this method is called by an admin
    :param volunteer:
    :param camp: the new camp
    :return:
    """
    pass


'''
