from controller.controller_error import ControllerError
from interfaces.cmd.cli import EmsShell

from models.refugee import Refugee
from models.plan import Plan
import controller.plan_controller as plan_controller
import controller.refugee_controller as refugee_controller
import controller.volunteer_controller as volunteer_controller


class AdminShell(EmsShell):
    """
    AdminShell is the command line interface for admin role.
    """
    admin_options = {"logout": 0, "profile": 1, "manage_plan": 2,
                     "manage_volunteer_account": 3,
                     "manage_refugee_profile": 4, "exit": "x"}

    def admin_menu(self) -> None:
        print("\n\033[100m\033[4m\033[1m{}\033[0m ".format("Admin Menu"))
        print("\033[1mWelcome to EMS. Please choose an option to continue:\033[0m\n"
              "[ 1 ] View my details\n"
              "[ 2 ] Manage an emergency plan (Create/Close/View)\n"
              "[ 3 ] Manage volunteer accounts and profile (Create/Edit/Deactivate/Delete)\n"
              "[ 4 ] Manage Refugee Profile\n\n"
              "[ 0 ] Log-out\n"
              "[ X ] Exit\n")

    def precmd(self, option: str) -> str:
        """
        Transfer option numbers to function name for Admin Menu
        """
        if option.isdigit() and int(option) in list(self.admin_options.values()):
            return list(self.admin_options.keys())[list(self.admin_options.values()).index(int(option))]
        elif option.upper() == 'X':
            return list(self.admin_options.keys())[list(self.admin_options.values()).index(option.lower())]
        else:
            return "invalid_input"

    def preloop(self) -> None:
        """
        Print out admin_menu before entering the shell.
        :return:
        """
        self.admin_menu()

    @staticmethod
    def do_invalid_input(arg):
        """
        Display error message for invalid input
        """
        CRED = '\033[31m'
        CEND = '\033[0m'
        print(f"{CRED} * Wrong input: Please re-enter an option from the menu, or enter X to exit.{CEND}")

    def return_previous_page(self):
        """
        User returns to previous menu after action completed.
        """
        while True:
            option = input("Enter R to return back to the previous menu.\n > ")
            if option.upper() == 'R':
                AdminShell(self.user).cmdloop()
            else:
                print("\033[31m {}\033[00m".format("** Invalid input. Enter R to return back to main menu."))
                continue

    # ----- basic commands for admins-----
    def do_profile(self, arg):
        """
        Print user info
        """
        print("\n\033[100m\033[4m\033[1m{}\033[0m\n".format("Your details:") +
              f'Username: {self.user.username}\n'
              f'Role: {self.user.__class__.__name__}\n')
        self.return_previous_page()

    def do_manage_plan(self, arg):
        """
        Enter PlanMenu for further actions
        """
        PlanMenu(self.user).cmdloop()

    def do_manage_volunteer_account(self, arg):
        """
        Enter ManageVolunteerMenu for further actions
        """
        ManageVolunteerMenu(self.user).cmdloop()

    def do_manage_refugee_profile(self, arg):
        """
        Enter ManageCampMenu for further actions
        """
        ManageRefugeeMenu(self.user).cmdloop()

    def do_exit(self, arg):
        super().do_exit(self)


class PlanMenu(AdminShell):
    """
    PlanMenu is the command line interface for emergency plan management.
    """
    plan_options = {"logout": 0, "create_plan": 1, "list_plans": 2, "view_plan": 3,
                    "close_plan": 4,
                    "return_main_menu": "r"}

    def plan_menu(self) -> None:
        print("\033[100m\033[4m\033[1mManage Emergency Plan\033[0m\n"
              "[ 1 ] Create a new emergency plan\n"
              "[ 2 ] View all existing emergency plans\n"
              "[ 3 ] View an emergency plan statistics\n"
              "[ 4 ] Close an emergency plan\n\n"
              "[ R ] Return to Main Menu\n")

    def precmd(self, option: str) -> str:
        """
        Transfer option numbers to function name for Admin Menu
        """
        if option.isdigit() and int(option) in list(self.plan_options.values()):
            return list(self.plan_options.keys())[list(self.plan_options.values()).index(int(option))]
        elif option.upper() == 'X' or option.upper() == 'R':
            return list(self.plan_options.keys())[list(self.plan_options.values()).index(option.lower())]
        else:
            return "invalid_input"

    def preloop(self) -> None:
        """
        Display plan menu.
        """
        self.plan_menu()

    def return_previous_page(self):
        while True:
            option = input("Enter R to return back to the previous menu.\n > ")
            if option.upper() == 'R':
                PlanMenu(self.user).cmdloop()
            else:
                print("\033[31m {}\033[00m".format("** Invalid input. Enter R to return back to main menu."))
                continue

    # ----- basic commands -----
    def do_create_plan(self, arg):
        """
        #1 Create a plan
        """
        print("\033[100m\033[4m\033[1m{}\033[0m ".format("Create a new emergency plan"))
        e_name = input("Enter emergency plan name: ")
        # -- handle emergency type
        print("Enter a emergency type from the list")
        emergency_types = plan_controller.list_emergency_types()
        e_types_dict = {t.value: t for t in emergency_types}  # create a dictionary for Enum
        for key in e_types_dict.keys():
            print(f'- {key}')
        while True:
            e_type = input(">")
            try:
                emergency = e_types_dict[e_type]
                e_type: Plan.EmergencyType = emergency
                break
            except KeyError:
                print(f'Type {e_type} is not on the list. Please re-enter type:')

        e_description = input("Enter description: ")
        e_geo_area = input("Enter geographical area: ")
        while True:
            camps_input = input("Enter camp names (use comma to separate camps): ")
            camp_names = camps_input.replace(', ', ',').split(",")
            if camp_names == '':
                print("\033[31m {}\033[00m".format("** Camp name cannot be empty."))
                continue
            try:
                camps = [plan_controller.create_camps(name) for name in camp_names]
                break
            except ControllerError:
                print("\033[31m {}\033[00m".format("** Failed to create camps. Please check and re-enter"))
                continue
        try:
            plan_controller.create_plan(plan_name=e_name,
                                        emergency_type=e_type,
                                        description=e_description,
                                        geographical_area=e_geo_area,
                                        camps=camps)
            print(f"\x1b[6;30;42m success! \x1b[0m\t Plan {e_name} created.")

            self.return_previous_page()
        except ControllerError:
            print("\033[31m {}\033[00m".format("** Unable to create an emergency plan. Press R to return and retry."))
            self.return_previous_page()

    def do_list_plans(self, arg):
        """
        #2 List out all the existing plans
        """
        plan_controller.list_plans()
        self.return_previous_page()

    def do_view_plan(self, arg):
        """
        #3 View a plan
        """
        while True:
            plan = input("Enter the plan name: ")
            try:
                find_plan = plan_controller.find_plan(plan)
                print("\033[100m\033[4m\033[1m{}\033[0m\n".format("View Plan statistics"))
                print(plan_controller.view_plan_statistics(find_plan))
                self.return_previous_page()
                break
            except ControllerError:
                print(f"\033[31m * Plan {plan} not found. Please re-enter plan name. \033[00m")
                continue

    def do_close_plan(self, arg):
        """
        #4 Delete a plan
        """
        while True:
            plan = input("Enter the plan name: ")
            find_plan = plan_controller.find_plan(plan)
            try:
                plan_controller.close_plan(find_plan)
                print("\x1b[6;30;42m success! \x1b[0m\t")
                print(f"Plan {plan} deleted.")
                self.return_previous_page()
                break
            except ControllerError:
                print(f"\033[31m * Plan {plan} not found. Please re-enter plan name. \033[00m")
                continue

    def do_return_main_menu(self, arg):
        AdminShell(self.user).cmdloop()


class ManageVolunteerMenu(AdminShell):
    """
    ManageVolunteerMenu is the sub-class of command line interface for admin role.
    It will be launched when the admin choose #3 and enter do_manage_volunteer_account().
    """
    manage_volunteer = {"logout": 0, "create_volunteer": 1, "view_volunteer": 2,
                        "edit_volunteer": 3, "deactivate_volunteer": 4, "reactivate_volunteer": 5,
                        "delete_volunteer": 6,
                        "return_main_menu": "r"}

    def volunteer_menu(self) -> None:
        print("\n\033[100m\033[4m\033[1m{}\033[0m\n".format("Manage Volunteer Accounts"))
        print(
            "[ 1 ] Create a new volunteer \n"
            "[ 2 ] View a volunteer profile\n"
            "[ 3 ] Edit a volunteer profile\n"
            "[ 4 ] De-activate a volunteer Account\n"
            "[ 5 ] Re-activate a volunteer Account\n"
            "[ 6 ] Delete a volunteer Account\n\n"
            "[ R ] Return to Main Menu\n"
            "[ 0 ] Log-out\n")

    def preloop(self) -> None:
        """
        Display manage volunteer menu.
        """
        self.volunteer_menu()

    def precmd(self, option: str) -> str:
        """
        Transfer option numbers to function name for Admin Menu
        """
        if option.isdigit() and int(option) in list(self.manage_volunteer.values()):
            return list(self.manage_volunteer.keys())[list(self.manage_volunteer.values()).index(int(option))]
        elif option.upper() == 'R':
            return list(self.manage_volunteer.keys())[list(self.manage_volunteer.values()).index(option.lower())]
        else:
            return "invalid_input"

    def return_previous_page(self) -> bool:
        while True:
            option = input("Enter R to return back to main menu. > ")
            if option.isalpha() and option.upper() == 'R':
                ManageVolunteerMenu(self.user).cmdloop()
                break
            else:
                print("\033[31m {}\033[00m".format("** Invalid input. Enter R to return back to main menu."))
                continue

    # ----- basic commands for volunteer account management -----
    def do_create_volunteer(self, arg):
        """
        #1 Create a volunteer
        """
        print("\033[100m\033[4m\033[1m{}\033[0m ".format("Create a new volunteer account"))
        # STEP 1: validate if plan exists
        while True:
            plan = input("Enter the plan that the new volunteer belongs to (or press # to exit): ")
            if plan == '#':
                ManageVolunteerMenu(self.user).cmdloop()
                break
            try:
                find_plan = plan_controller.find_plan(plan)
                plan = find_plan
                break
            except ControllerError:
                print(f"\033[31m * Plan {plan} not found. Please re-enter plan name. \033[00m")
                continue

        # STEP 2: validate if camp exists
        while True:
            camp = input("Enter the camp that the new volunteer belongs to (or press # to exit): ")
            if camp == '#':
                ManageVolunteerMenu(self.user).cmdloop()
                break
            try:
                find_camp = plan_controller.find_camp(plan=plan, camp_name=camp)
                camp = find_camp
                break
            except ControllerError:
                print(f"\033[31m * Camp {camp} not found. Please re-enter camp name. \033[00m")
                continue

        # STEP 3: other user inputs
        while True:
            username = input("Enter volunteer's username: ")
            password = input("Enter volunteer's password: ")
            firstname = input("Enter volunteer's first name: ")
            lastname = input("Enter volunteer's last name: ")
            phone = input("Enter volunteer's phone (start from + sign and national code): ")

            try:
                volunteer_controller.create_volunteer(username=username,
                                                      password=password,
                                                      firstname=firstname,
                                                      lastname=lastname,
                                                      phone=phone, camp=camp)
                print(f"\x1b[6;30;42m success! \x1b[0m Volunteer {username} created.\n")
                self.return_previous_page()
                break
            except ControllerError as e:
                print(f'\033[31mFailed to create volunteer \033[00m{username} due to the following reasons:')
                print(f'\033[31m* {e.message} \033[00m')
                self.return_previous_page()
                break

    def do_view_volunteer(self, arg):
        """
        #2 View a volunteer's details
        """
        while True:
            username = input("Enter the volunteer's username to view (Press # to leave this page): ")
            if username == '#':
                ManageVolunteerMenu(self.user).cmdloop()
            try:
                find_volunteer = volunteer_controller.find_volunteer(username)
                print(volunteer_controller.view_volunteer_profile(find_volunteer))
                self.return_previous_page()
                break
            except ControllerError:
                print(f"\033[31m* Volunteer {username} not found. Please check and re-enter.\033[00m")
                continue

    def do_edit_volunteer(self, arg):
        """
        #3 Edit a volunteer's details via EditVolunteerMenu
        """
        from interfaces.cmd.edit_profile_cli import EditVolunteerMenu
        EditVolunteerMenu(self.user).cmdloop()

    def do_deactivate_volunteer(self, arg):
        """
        #4 Changing a volunteer's status to deactivated
        """
        while True:
            username = input("Enter the volunteer's username to deactivate (Press # to leave this page): ")
            if username == '#':
                ManageVolunteerMenu(self.user).cmdloop()
            try:
                find_volunteer = volunteer_controller.find_volunteer(username)
                volunteer_controller.deactivate_volunteer(find_volunteer)
                print(f"\x1b[6;30;42m success! \x1b[0m Volunteer {username} deactivated.\n")
                self.return_previous_page()
                break
            except ControllerError:
                print(f"\033[31m* Volunteer {username} not found. Please check and re-enter.\033[00m")
                continue

    def do_reactivate_volunteer(self, arg):
        """
        #5 Changing a volunteer's status to active
        """
        while True:
            username = input("Enter the volunteer's username to reactivate (Press # to leave this page): ")
            if username == '#':
                ManageVolunteerMenu(self.user).cmdloop()
            try:
                find_volunteer = volunteer_controller.find_volunteer(username)
                volunteer_controller.reactivate_volunteer(find_volunteer)
                print(f"\x1b[6;30;42m success! \x1b[0mVolunteer {username} reactivated.\n")
                self.return_previous_page()
                break
            except ControllerError:
                print(f"\033[31m* Volunteer {username} not found. Please check and re-enter.\033[00m")
                continue

    def do_delete_volunteer(self, arg):
        """
        #6 Delete a volunteer
        """
        while True:
            username = input("Enter the volunteer's username to delete (Press # to leave this page): ")
            if username == '#':
                ManageVolunteerMenu(self.user).cmdloop()
            try:
                find_volunteer = volunteer_controller.find_volunteer(username)
                volunteer_controller.delete_volunteer(find_volunteer)
                print("\x1b[6;30;42m success! \x1b[0m")
                print(f"Volunteer {username} deleted.")
                self.return_previous_page()
                break
            except ControllerError:
                print(f"\033[31m* Volunteer {username} not found. Please check and re-enter.\033[00m")
                continue

    def do_return_main_menu(self, arg):
        AdminShell(self.user).cmdloop()


class ManageRefugeeMenu(AdminShell):
    refugee_menu = {"logout": 0, "create_refugee": 1, "view_refugee": 2,
                    "return_main_menu": "r"}

    def plan_menu(self) -> None:
        print("\n\033[100m\033[4m\033[1mManage Refugee Profile\033[0m\n"
              "[ 1 ] Create a refugee profile\n"
              "[ 2 ] View a refugee profile\n\n"
              "[ R ] Return to Main Menu\n")

    def preloop(self) -> None:
        """
        Display plan menu.
        :return:
        """
        self.plan_menu()

    def precmd(self, option: str) -> str:
        """
        Transfer option numbers to function name for Admin Menu
        """
        if option.isdigit() and int(option) in list(self.refugee_menu.values()):
            return list(self.refugee_menu.keys())[list(self.refugee_menu.values()).index(int(option))]
        elif option.upper() == 'R':
            return list(self.refugee_menu.keys())[list(self.refugee_menu.values()).index(option.lower())]
        else:
            return "invalid_input"

    # ----- basic commands -----
    def do_create_refugee(self, arg):
        """
        #1 Create a refugee profile
        """
        print("\n\033[100m\033[4m\033[1m{}\033[0m ".format("Create a new refugee profile"))

        # STEP 1: validate if plan exists
        while True:
            plan = input("Enter the plan that the refugee belongs to (or press # to exit): ")
            if plan == '#':
                ManageRefugeeMenu(self.user).cmdloop()
                break
            try:
                find_plan = plan_controller.find_plan(plan)
                plan = find_plan
                break
            except ControllerError:
                print(f"\033[31m * Plan {plan} not found. Please re-enter plan name. \033[00m")
                continue

        # STEP 2: validate if camp exists
        while True:
            camp = input("Enter the camp that the new refugee belongs to (or press # to exit): ")
            if camp == '#':
                ManageRefugeeMenu(self.user).cmdloop()
                break
            try:
                find_camp = plan_controller.find_camp(plan=plan, camp_name=camp)
                r_camp = find_camp
                break
            except ControllerError:
                print(f"\033[31m * Camp {camp} not found. Please re-enter camp name. \033[00m")
                continue

        # STEP 3: get refugee info
        r_firstname = input("Enter refugee's first name: ")
        r_lastname = input("Enter refugee's last name: ")
        num_of_family_member = int(input("Enter the number of family members:"))

        # STEP 4: handle medical_condition
        print("Enter refugee's medical condition from the list")
        medical_condition_types = list(refugee_controller.list_medical_condition_types())
        for i, option in enumerate(medical_condition_types):
            print(f'[ {i} ] {option.value}')

        while True:
            medical_input = input("Enter refugee's medical condition from the list "
                                  "(use comma to separate multiple inputs): ")
            medical_conditions = medical_input.replace(', ', ',').split(",")
            r_conditions = []
            for condition in medical_conditions:
                try:
                    r_condition = medical_condition_types[int(condition)]
                    r_conditions.append(r_condition)
                except (IndexError, ValueError):
                    print(f'\033[31m* Type {condition} is not on the list.\033[00m')
                    break
            else:
                break

        # STEP 5: Create refugee
        while True:
            try:
                refugee = refugee_controller.create_refugee(firstname=r_firstname, lastname=r_lastname, camp=r_camp,
                                                            num_of_family_member=num_of_family_member,
                                                            medical_condition_type=r_conditions,
                                                            starting_date=None)
                print(f"\x1b[6;30;42m success! \x1b[0m\r "
                      f"Refugee {r_firstname} {r_lastname} created. Refugee ID: {refugee.user_id}")
                print(f"Please note down refugee ID as it is required when viewing refugee profile.\n")
                self.return_previous_page()
                break
            except ControllerError:
                print(f'\033[31m* Failed to create a refugee profile for\033[00m {r_firstname} {r_lastname}')
                continue

    def do_view_refugee(self, arg):
        """
        #2 View a refugee profile
        """
        while True:
            try:
                refugee_id = int(input("Enter the refugee's ID to view: "))
                try:
                    find_refugee = refugee_controller.find_refugee(refugee_id)
                    refugee_controller.view_refugee(find_refugee)
                    self.return_previous_page()
                    break
                except ControllerError:
                    print(f"{refugee_id} not found. Please check and re-enter.")
                    continue
            except ValueError:
                print(f'\033[31m* Invalid refugee ID {refugee_id}. Please check and re-enter.\033[00m')

    def do_return_main_menu(self, arg):
        AdminShell(self.user).cmdloop()
