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
        print("\n\033[100m\033[4m\033[1m{}\033[0m".format("Edit Volunteer Profile"))
        print(
            f"You're editing {volunteer_edit.username}'s profile. Select the information to edit :\n"
            f"[ 1 ] First name: {volunteer_edit.firstname}\n"
            f"[ 2 ] Last name: {volunteer_edit.lastname}\n"
            f"[ 3 ] Phone number: {volunteer_edit.phone}\n"
            f"[ 4 ] Camp: {volunteer_edit.camp}\n"
            f"[ 5 ] Availability: {volunteer_edit.availability}\n\n"
            f"[ R ] Return to previous page\n"
            f"[ 0 ] Log-out\n")

    def precmd(self, option: str) -> str:
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
    def do_edit_firstname(self, arg):
        volunteer_edit = self.check_username()
        print(f"Original first name is {volunteer_edit.firstname}.")
        while True:
            firstname = input("Please enter new first name (or press # to exit this page):")
            if firstname == '#':
                EditVolunteerMenu(self.user).cmdloop()
                break
            try:
                volunteer_controller.edit_firstname(volunteer_edit, firstname)
                print(f"\x1b[6;30;42msuccess!\x1b[0m Volunteer's first name is changed to {volunteer_edit.firstname}")
                self.return_previous_page()
                break
            except ControllerError:
                print(
                    f"\033[31m** Invalid first name {firstname}. First name should have at least 2 characters.\033[00m")
                continue

    def do_edit_lastname(self, arg):
        volunteer_edit = self.check_username()
        print(f"Original last name is {volunteer_edit.lastname}.")
        while True:
            lastname = input("Please enter new last name (or press # to exit this page):")
            if lastname == '#':
                EditVolunteerMenu(self.user).cmdloop()
                break
            try:
                volunteer_controller.edit_lastname(volunteer_edit, lastname)
                print(f"\x1b[6;30;42msuccess!\x1b[0m Volunteer's last name is changed to {volunteer_edit.lastname}")
                self.return_previous_page()
                break
            except ControllerError:
                print(f"\033[31m** Invalid last name {lastname}. Last name should have at least 2 characters.\033[00m")
                continue

    def do_edit_phone(self, arg):
        volunteer_edit = self.check_username()
        print(f"Original phone number is {volunteer_edit.phone}.")
        print("(Phone number should include country code with a + sign.")
        while True:
            phone = input("Please enter new phone number (or press # to exit this page):")
            if phone == '#':
                EditVolunteerMenu(self.user).cmdloop()
                break
            try:
                volunteer_controller.edit_phone(volunteer_edit, phone)
                print(f"\x1b[6;30;42msuccess!\x1b[0m Volunteer's phone number is changed to {volunteer_edit.phone}")
                self.return_previous_page()
                break
            except ControllerError:
                print(f"\033[31m** Invalid phone number {phone}. "
                      f"Phone number should include country code with a + sign.\033[00m")
                continue

    def do_edit_camp(self, arg):
        volunteer_edit = self.check_username()
        print(f"Original assigned camp is {volunteer_edit.camp} for Plan {volunteer_edit.camp.plan}.")
        while True:
            camp = input("Enter New assigned camp:")
            # need to add check camp
            pass
            ### Available camps vary by user role
            volunteer_controller.edit_camp(volunteer_edit, camp, self.is_admin)
            print(f"Updated successfully! New assigned camp is {volunteer_edit.camp}.")

    def do_edit_availability(self, arg):
        # need refinement
        pass
        username = input("Username: ")
        availability = input(
            f"Original availability is {volunteer_controller.find_volunteer(username).availability}. Switch it to: ")
        volunteer = volunteer_controller.find_volunteer(username)
        volunteer_controller.edit_availability(volunteer, availability)
        print(
            f"Updated successfully! The availability is now {volunteer_controller.find_volunteer(username).availability}.")
        pass

    def do_return_menu(self, arg):
        if isinstance(self.user, Admin):
            ManageVolunteerMenu(self.user).cmdloop()
        elif isinstance(self.user, Volunteer):
            VolunteerShell(self.user).cmdloop()
