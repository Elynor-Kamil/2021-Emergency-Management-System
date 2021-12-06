from controller import plan_controller
from controller.controller_error import ControllerError
from interfaces.cmd.volunteer_cli import VolunteerShell
from models.admin import Admin
import controller.volunteer_controller as volunteer_controller
from interfaces.cmd.admin_cli import ManageVolunteerMenu

###---- Manage Volunteer Menu ----
from models.volunteer import Volunteer


class EditVolunteerMenu(ManageVolunteerMenu):
    edit_options = {"edit_firstname": 1,
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
                        self.volunteer = find_volunteer
                        break
                    except ControllerError:
                        print(f"\033[31m** Volunteer {username} not found. Please check and re-enter.\033[00m")
                        continue
        elif isinstance(self.user, Volunteer):
            self.is_admin = False
            self.volunteer = self.user

    def edit_volunteer_menu(self) -> None:

        print("\n\033[100m\033[4m\033[1m{}\033[0m".format("Edit Volunteer Profile"))
        print(
            f"You're editing {self.volunteer.username}'s profile. Select the information to edit :\n"
            f"[ 1 ] First name: {self.volunteer.firstname}\n"
            f"[ 2 ] Last name: {self.volunteer.lastname}\n"
            f"[ 3 ] Phone number: {self.volunteer.phone}\n"
            f"[ 4 ] Camp: {self.volunteer.camp}\n"
            f"[ 5 ] Availability: {self.volunteer.availability}\n\n"
            f"[ R ] Return to previous page\n")

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
        self.check_username()
        self.edit_volunteer_menu()

    def return_previous_page(self):
        super().return_previous_page()

    # ----- basic commands for volunteer account management -----
    def do_edit_firstname(self, arg):
        print(f"Original first name is {self.volunteer.firstname}.")
        while True:
            firstname = input("Please enter new first name (or press # to exit this page):")
            if firstname == '#':
                EditVolunteerMenu(self.user).cmdloop()
                break
            try:
                volunteer_controller.edit_firstname(self.volunteer, firstname)
                print(f"\x1b[6;30;42msuccess!\x1b[0m Volunteer's first name is changed to {self.volunteer.firstname}")
                self.return_previous_page()
                break
            except ControllerError:
                print(
                    f"\033[31m** Invalid first name {firstname}. First name should have at least 2 characters.\033[00m")
                continue

    def do_edit_lastname(self, arg):
        print(f"Original last name is {self.volunteer.lastname}.")
        while True:
            lastname = input("Please enter new last name (or press # to exit this page):")
            if lastname == '#':
                EditVolunteerMenu(self.user).cmdloop()
                break
            try:
                volunteer_controller.edit_lastname(self.volunteer, lastname)
                print(f"\x1b[6;30;42msuccess!\x1b[0m Volunteer's last name is changed to {self.volunteer.lastname}")
                self.return_previous_page()
                break
            except ControllerError:
                print(f"\033[31m** Invalid last name {lastname}. Last name should have at least 2 characters.\033[00m")
                continue

    def do_edit_phone(self, arg):
        print(f"Original phone number is {self.volunteer.phone}.")
        print("(Phone number should include country code with a + sign.")
        while True:
            phone = input("Please enter new phone number (or press # to exit this page):")
            if phone == '#':
                EditVolunteerMenu(self.user).cmdloop()
                break
            try:
                volunteer_controller.edit_phone(self.volunteer, phone)
                print(f"\x1b[6;30;42msuccess!\x1b[0m Volunteer's phone number is changed to {self.volunteer.phone}")
                self.return_previous_page()
                break
            except ControllerError:
                print(f"\033[31m** Invalid phone number {phone}. "
                      f"Phone number should include country code with a + sign.\033[00m")
                continue

    def do_edit_camp(self, arg):
        print(f"Original assigned camp is {self.volunteer.camp} for Plan {self.volunteer.camp.plan}.")
        if self.is_admin:
            while True:
                plan_name = input("Enter the name of the new plan (or press # to exit): ")
                if plan_name == '#':
                    EditVolunteerMenu(self.user).cmdloop()
                    break
                try:
                    plan = plan_controller.find_plan(plan_name)
                    break
                except ControllerError:
                    print(f"\033[31m * Plan {plan_name} not found. Please re-enter plan name. \033[00m")
                    continue
        else:
            plan = self.volunteer.camp.plan

        # STEP 2: validate if camp exists
        while True:
            camp_name = input("Enter the name of the new camp (or press # to exit): ")
            if camp_name == '#':
                ManageVolunteerMenu(self.user).cmdloop()
                break
            try:
                camp = plan_controller.find_camp(plan=plan, camp_name=camp_name)
                break
            except ControllerError:
                print(f"\033[31m * Camp {camp_name} not found. Please re-enter camp name. \033[00m")
                continue

        try:
            volunteer_controller.edit_camp(self.volunteer, camp, self.is_admin)
            print(f"\x1b[6;30;42m success! \x1b[0m New assigned camp is {self.volunteer.camp}.")
        except ControllerError as e:
            print(f'Cannot change camp: {str(e)}')

    def do_edit_availability(self, arg):
        print(f"Original availability is {self.volunteer.availability}.")
        while True:
            print('[1] - Available\n'
                  '[0] - Unavailable')
            availability = input("Please select new availability:")
            if availability == '1':
                availability = True
            elif availability == '0':
                availability = False
            else:
                print(f"\033[31m** Invalid option {availability}.\033[00m")
                continue
            break
        volunteer = volunteer_controller.edit_availability(self.volunteer, availability)
        status = 'available' if volunteer.availability else 'unavailable'
        print(f"\x1b[6;30;42m success! \x1b[0m Volunteer {volunteer.firstname} is now {status}.")
        self.return_previous_page()

    def do_return_menu(self, arg):
        if isinstance(self.user, Admin):
            ManageVolunteerMenu(self.user).cmdloop()
        elif isinstance(self.user, Volunteer):
            VolunteerShell(self.user).cmdloop()
