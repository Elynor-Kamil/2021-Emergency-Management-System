from cmd import Cmd
import sys
from interfaces.cli import EmsShell
from data.users import users_catalog
from models.admin import Admin
from models.user import User, require_role
from models.volunteer import Volunteer
from controller.plan_controller import create_plan

class AdminShell(EmsShell):
    """
    AdminShell is the command line interface for admin role.
    """
    admin_options = {"logout": 0, "profile": 1, "manage_plan": 2,
                     "manage_volunteer_account": 3,
                     "manage_refugee_profile": 4, "exit": "x"}

    def admin_menu(self) -> None:
        print("\033[100m\033[4m\033[1m{}\033[0m ".format("Admin Menu"))
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
        elif option.upper() == 'X' or option.upper() == 'R':
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

    # ----- basic commands for admins-----
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


    def do_return(self, arg):
        """
        Return to AdminShell, for sub-classes
        """
        print("Return to main menu.\n")
        AdminShell(self.user).cmdloop()


class PlanMenu(AdminShell):
    """
    PlanMenu is the command line interface for emergency plan management.
    """
    admin_options = {"logout": 0, "create_plan": 1, "view_plan": 2,
                     "close_plan": 3,
                     "return": "r"}

    def plan_menu(self) -> None:
        print("\033[100m\033[4m\033[1mManage Emergency Plan\033[0m\n"
              "[ 1 ] Create a new emergency plan\n"
              "[ 2 ] View an emergency plan\n"
              "[ 3 ] Close an emergency plan\n\n"
              "[ R ] Return to Main Menu\n")

    def preloop(self) -> None:
        """
        Display plan menu.
        :return:
        """
        self.plan_menu()

    # ----- basic commands -----
    def do_create_plan(self, arg):
        """
        Create a plan
        """
        import controller.plan_controller as plan
        print("\033[100m\033[4m\033[1m{}\033[0m ".format("Create a new emergency plan"))
        e_name = input("Enter emergency plan name:")
        e_type = input("Choose a emergency type:")
        e_description = input("Enter description:")
        e_geoarea = input("Enter emergency plan graphical_area:")
        e_camp_number = input("Enter the number of camps:")
        e_camps = input("Enter camp names:")

        plan.create_plan(e_name, e_type, e_description, e_geoarea, e_camps)

    def do_view_plan(self, arg):
        """
        View a plan
        """
        print("connect to view plan...")  # add function
        pass

    def do_close_plan(self, arg):
        """
        Delete a plan
        """
        print("connect to close plan...")  # add function
        pass



class ManageVolunteerMenu(AdminShell):
    """
    ManageVolunteerMenu is the sub-class of command line interface for admin role.
    It will be launched when the admin choose #3 and enter do_manage_volunteer_account().
    """
    admin_options = {"logout": 0, "create_volunteer": 1, "edit_volunteer": 2,
                     "deactivate_volunteer": 3, "reactivate_volunteer": 4, "delete_volunteer": 5,
                     "return": "r"}

    def volunteer_menu(self) -> None:
        print("\033[100m\033[4m\033[1m{}\033[0m\n".format("Manage Emergency Plan"))
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
        :return:
        """
        self.volunteer_menu()

    # ----- basic commands for volunteer account management -----
    def do_create_volunteer(self, username: str, password: str):
        """
        Create a volunteer
        """
        print("connect to create a new volunteer...")
        username = input('Username: ')
        password = input('Password: ')
        new_volunteer = Volunteer(username=username, password=password)
        print(f"Successfully created volunteer {new_volunteer.username}")
        pass  # add function and verification

    def do_edit_volunteer(self, arg):
        """
        Edit a volunteer's details
        """
        print("connect to edit volunteer...")
        pass

    def do_view_volunteer(self, arg):
        """
        View a volunteer's details
        """
        print("connect to view volunteer...")
        pass

    def do_deactivate_volunteer(self, arg):
        """
        Changing a volunteer's status to deactivated
        """
        print("connect to deactivate volunteer...")
        pass

    def do_reactivate_volunteer(self, arg):
        """
        Changing a volunteer's status to active
        """
        print("connect to reactivate volunteer...")
        pass

    def do_delete_volunteer(self, arg):
        """
        Delete a volunteer
        """
        print("connect to delete volunteer...")
        pass


class ManageRefugeeMenu(AdminShell):
    admin_options = {"logout": 0, "create_refugee": 1, "view_refugee": 2,
                     "edit_refugee": 3,
                     "return": "r"}

    def plan_menu(self) -> None:
        print("\033[100m\033[4m\033[1mManage Refugee Profile\033[0m"
              "[ 1 ] Create a refugee profile\n"
              "[ 2 ] View a refugee profile\n"
              "[ 3 ] Edit a refugee profile\n\n"
              "[ R ] Return to Main Menu\n")

    def preloop(self) -> None:
        """
        Display plan menu.
        :return:
        """
        self.plan_menu()

    # ----- basic commands -----
    def do_create_refugee(self, arg):
        """
        Create a refugee profile
        """
        print("connect to create refugee profile...")  # add function
        pass

    def do_view_refugee(self, arg):
        """
        View a refugee profile
        """
        print("connect to view refugee profile...")  # add function
        pass

    def do_edit_refugee(self, arg):
        """
        Edit a refugee profile
        """
        print("connect to edit refugee profile...")  # add function
        pass
