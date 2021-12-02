import controller.volunteer_controller as vc
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
         1) First name
         2) Last name
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
        if option.isdigit() and 0 <= int(option) <= 5:
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
        firstname = input(f"Original first name is {vc.find_volunteer(username).firstname}. New first name: ")
        volunteer = vc.find_volunteer(username)
        vc.edit_firstname(volunteer, firstname)
        print(f"Updated successfully! New first name is {vc.find_volunteer(username).firstname}.")

    def do_edit_lastname(self):
        username = input("Username: ")
        lastname = input(f"Original last name is {vc.find_volunteer(username).lastname}. New last name: ")
        volunteer = vc.find_volunteer(username)
        vc.edit_lastname(volunteer, lastname)
        print(f"Updated successfully! New last name is {vc.find_volunteer(username).lastname}.")

    def do_edit_phone(self):
        username = input("Username: ")
        phone = input(f"Original phone number is {vc.find_volunteer(username).phone}. New phone number: ")
        volunteer = vc.find_volunteer(username)
        vc.edit_phone(volunteer, phone)
        print(f"Updated successfully! New phone number is {vc.find_volunteer(username).phone}.")

    def do_edit_camp(self):
        username = input("Username: ")
        ### Available camps vary by user role
        camp = Camp(input(f"Original assigned camp is {vc.find_volunteer(username).camp}. New assigned camp: "))
        is_admin = self.user.__class__.__name__
        volunteer = vc.find_volunteer(username)
        vc.edit_camp(volunteer, camp, is_admin)
        print(f"Updated successfully! New assigned camp is {vc.find_volunteer(username).camp}.")

    def do_edit_availability(self):
        username = input("Username: ")
        availability = input(f"Original availability is {vc.find_volunteer(username).availability}. Switch it to: ")
        volunteer = vc.find_volunteer(username)
        vc.edit_availability(volunteer, availability)
        print(f"Updated successfully! The availability is now {vc.find_volunteer(username).availability}.")

    def do_return(self):
        ManageVolunteerMenu().cmdloop()
