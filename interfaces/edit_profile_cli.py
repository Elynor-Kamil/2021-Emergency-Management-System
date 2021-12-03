from controller.controller_error import ControllerError
from interfaces.volunteer_cli import VolunteerShell
from models.admin import Admin
from models.plan import Plan
import controller.plan_controller as plan_controller
import controller.refugee_controller as refugee_controller
import controller.volunteer_controller as volunteer_controller
from models.camp import Camp
from interfaces.admin_cli import ManageVolunteerMenu

###---- Manage Volunteer Menu ----
from models.volunteer import Volunteer


class EditVolunteerMenu(ManageVolunteerMenu):
    edit_options = {"logout": 0,
                    "edit_firstname": 1,
                    "edit_lastname": 2,
                    "edit_phone": 3,
                    "edit_camp": 4,
                    "edit_availability": 5,
                    "return_menu": "r"}

    def check_username(self) -> Volunteer:
        if isinstance(self.user, Admin):
            self.is_admin = True
            while True:
                username = input("Enter Volunteer's username (or enter # to leave this page): ")
                if username == "#":
                    ManageVolunteerMenu(self.user).cmdloop()
                    break
                else:
                    try:
                        find_volunteer = volunteer_controller.find_volunteer(username)
                        return find_volunteer
                    except ControllerError:
                        print(f"\033[31m** Volunteer {username} not found. Please check and re-enter.\033[00m")
                        continue
        elif isinstance(self.user, Volunteer):
            self.is_admin = False
            return self.user

    def edit_volunteer_menu(self) -> None:
        volunteer_edit = self.check_username()
        print("\n\033[100m\033[4m\033[1m{}\033[0m\n".format("Edit Volunteer Profile"))
        print(
            "Select the information to edit :\n"
            f"[ 1 ] First name: {volunteer_edit.firstname}\n"
            f"[ 2 ] Last name: {volunteer_edit.lastname}\n"
            f"[ 3 ] Phone number: {volunteer_edit.lastname}\n"
            f"[ 4 ] Camp: {volunteer_edit.camp}\n"
            f"[ 5 ] Availability: {volunteer_edit.availability}\n"
            f"[ R ] Return to previous page\n"
            f"[ 0 ] Log-out\n")

    def precmd(self, option: str) -> int:
        if option.isdigit() and int(option) in list(self.edit_options.values()):
            return list(self.edit_options.keys())[list(self.edit_options.values()).index(int(option))]
        elif option.upper() == 'R':
            return list(self.edit_options.keys())[list(self.edit_options.values()).index(option.lower())]
        else:
            return "invalid_input"

    def preloop(self) -> None:
        """
        Check user's role before showing edit_volunteer_menu
        :return:
        """
        self.edit_volunteer_menu()

    def return_previous_page(self):
        super().return_previous_page()

    # ----- basic commands for volunteer account management -----
    def do_edit_firstname(self, volunteer):
        volunteer_edit = self.check_username()
        firstname = input(f"Original first name is {volunteer_edit.firstname}. Please enter new first name: ")
        volunteer_controller.edit_firstname(volunteer_edit, firstname)
        print("\x1b[6;30;42m success! \x1b[0m")
        print(f"Volunteer's first name is changed to {volunteer_edit.firstname}")
        self.return_previous_page()

    def do_edit_lastname(self):
        username = input("Username: ")
        lastname = input(
            f"Original last name is {volunteer_controller.find_volunteer(username).lastname}. New last name: ")
        volunteer = volunteer_controller.find_volunteer(username)
        volunteer.edit_lastname(volunteer, lastname)
        print(f"Updated successfully! New last name is {volunteer_controller.find_volunteer(username).lastname}.")
        pass

    def do_edit_phone(self):
        username = input("Username: ")
        phone = input(
            f"Original phone number is {volunteer_controller.find_volunteer(username).phone}. New phone number: ")
        volunteer = volunteer_controller.find_volunteer(username)
        volunteer_controller.edit_phone(volunteer, phone)
        print(f"Updated successfully! New phone number is {volunteer_controller.find_volunteer(username).phone}.")
        pass

    def do_edit_camp(self):
        volunteer_edit = self.check_username()
        print(f"Original assigned camp is {volunteer_edit.camp} for Plan {volunteer_edit.camp.plan}.")
        while True:
            camp = input("Enter New assigned camp:")
            ### Available camps vary by user role
            volunteer_controller.edit_camp(volunteer_edit, camp, self.is_admin)
            print(f"Updated successfully! New assigned camp is {volunteer_edit.camp}.")

    def do_edit_availability(self):
        username = input("Username: ")
        availability = input(
            f"Original availability is {volunteer_controller.find_volunteer(username).availability}. Switch it to: ")
        volunteer = volunteer_controller.find_volunteer(username)
        volunteer_controller.edit_availability(volunteer, availability)
        print(
            f"Updated successfully! The availability is now {volunteer_controller.find_volunteer(username).availability}.")
        pass

    def do_return_menu(self):
        if isinstance(self.user, Admin):
            ManageVolunteerMenu(self.user).cmdloop()
        elif isinstance(self.user, Volunteer):
            VolunteerShell(self.user).cmdloop()
