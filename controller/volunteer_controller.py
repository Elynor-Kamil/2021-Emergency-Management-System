from models.volunteer import Volunteer
from models.camp import Camp
from interfaces.admin_cli import ManageVolunteerMenu


###---- Manage Volunteer Menu ----
class EditVolunteerMenu(ManageVolunteerMenu):
    def __init__(self):
        super(EditVolunteerMenu, self).__init__()

    def edit_volunteer_menu(self) -> None:
        print("""
         Select an item you'd like to edit:
         --------
         1) Firstname
         2) Lastname
         3) Phone number
         4) Camp
         5) Availability

         R) Return to previous page
         0) Log-out
         """)

    def precmd(self, option: str) -> int:
        edit_volunteer_options = {"logout": 0,
                                  "edit_firstname": 1,
                                  "edit_lastname": 2,
                                  "edit_phone": 3,
                                  "edit_camp": 4,
                                  "edit_availability": 5,
                                  "return": "r"}

        ### Add input error handling
        if option.isdigit():
            return list(edit_volunteer_options.keys())[list(edit_volunteer_options.values()).index(int(option))]
        elif option == "r" or "R":
            return list(edit_volunteer_options.keys())[list(edit_volunteer_options.values()).index(option.lower())]
        else:
            pass

    def preloop(self) -> None:
        self.edit_volunteer_menu()

    # ----- basic commands for volunteer account management -----
    def do_edit_firstname(self):
        username = input("Username: ")
        firstname = input(f"Original firstname is {find_volunteer(username).firstname}. New firstname: ")
        edit_firstname(username, firstname)
        print(f"Updated successfully! New firstname is {find_volunteer(username).firstname}.")

    def do_edit_lastname(self):
        username = input("Username: ")
        lastname = input(f"Original lastname is {find_volunteer(username).lastname}. New lastname: ")
        edit_lastname(username, lastname)
        print(f"Updated successfully! New lastname is {find_volunteer(username).lastname}.")

    def do_edit_phone(self):
        username = input("Username: ")
        phone = input(f"Original phone number is {find_volunteer(username).phone}. New phone number: ")
        edit_phone(username, phone)
        print(f"Updated successfully! New phone number is {find_volunteer(username).phone}.")

    def do_edit_camp(self):
        username = input("Username: ")
        ### Available camps vary by user role
        camp = Camp(input(f"Original assigned camp is {find_volunteer(username).camp}. New assigned camp: "))
        is_admin = self.user.__class__.__name__
        edit_camp(username, camp, is_admin)
        print(f"Updated successfully! New assigned camp is {find_volunteer(username).camp}.")

    def do_edit_availability(self):
        username = input("Username: ")
        availability = input(f"Original availability is {find_volunteer(username).availability}. Switch it to: ")
        edit_availability(username, availability)
        print(f"Updated successfully! The availability is now {find_volunteer(username).availability}.")

    def do_return(self):
        ManageVolunteerMenu().cmdloop()