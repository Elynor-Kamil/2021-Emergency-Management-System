from cmd import Cmd
import sys
from interfaces.cli import EmsShell
from data.users import users_catalog
from models.admin import Admin
from models.user import User, require_role
from models.volunteer import Volunteer


class AdminShell(EmsShell):
    """
    AdminShell is the command line interface for admin role.
    """

    def admin_menu(self) -> None:
        print("\033[100m\033[4m\033[1m{}\033[0m ".format("Admin Menu"))
        print("\033[1mWelcome to EMS. Please choose an option to continue:\033[0m\n"
              "[ 1 ] View my details\n"
              "[ 2 ] Manage emergency plan (Create/Close/View)\n"
              "[ 3 ] Manage volunteer accounts and profile (Create/Edit/Deactivate/Delete)\n"
              "[ 4 ] View camp details\n"
              "[ 5 ] Assign volunteer to a new plan\n"
              "[ 6 ] Manage refugee profile\n\n"
              "[ 0 ] Log-out\n"
              "[ X ] Exit\n")


    def precmd(self, option: str) -> str:
        """
        Transfer option numbers to function name for Admin Menu
        """
        admin_options = {"logout": 0, "profile": 1, "manage_plan": 2,
                         "manage_volunteer_account": 3,
                         "view_camp_details": 4,
                         "assign_volunteer": 5,
                         "manage_refugee_profile": 6, "exit": "x"}

        if option.isdigit() and int(option) in list(admin_options.values()):
            return list(admin_options.keys())[list(admin_options.values()).index(int(option))]
        elif option == ('x' or 'X'):
            print(option)
            # ensure the input is in lower-case
            return list(admin_options.keys())[list(admin_options.values()).index(option.lower())]
        else:
            return "invalid_input"

    def preloop(self) -> None:
        """
        Print out admin_menu before entering the shell.
        :return:
        """
        self.admin_menu()

    # ----- basic commands for admins-----
    @staticmethod
    def do_invalid_input(arg):
        """
        Display error message for invalid input
        """
        CRED = '\033[31m'
        CEND = '\033[0m'
        print(f"{CRED} * Wrong input: Please re-enter an option from the menu, or enter X to exit.{CEND}")

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

    def do_manage_camp_details(self, arg):
        """
        Enter ManageCampMenu for further actions
        """
        pass

    def do_assign_volunteer(self, arg):
        """
        Call assign_volunteer() function from Admin class
        """
        print("Assign a volunteer to a camp:")
        pass  # add on function

    def do_return(self, arg):
        """
        Return to AdminShell, for sub-classes
        """
        print("Return to main menu...\n")
        AdminShell(self.user).cmdloop()



class PlanMenu(AdminShell):

    def plan_menu(self) -> None:
        print("\033[100m\033[4m\033[1mManage Emergency Plan\033[0m"
              "[ 1 ] Create a new emergency plan\n"
              "[ 2 ] View an emergency plan\n"
              "[ 3 ] Close an emergency plan\n\n"
              "[ R ] Return to previous page\n")

    def precmd(self, option: str) -> str:
        """
        Transfer option numbers to function name
        """
        admin_options = {"logout": 0, "create_plan": 1, "view_plan": 2,
                         "close_plan": 3,
                         "return": "r"}
        if option.isdigit() and int(option) in list(admin_options.values()):
            return list(admin_options.keys())[list(admin_options.values()).index(int(option))]
        elif option == ('x' or 'X') or ('r' or "R"):
            return list(admin_options.keys())[list(admin_options.values()).index(option.lower())]
        else:
            return "invalid_input"

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
        print("connect to create plan...") #add function
        pass

    def do_view_plan(self, arg):
        """
        View a plan
        """
        print("connect to view plan...") #add function
        pass

    def do_close_plan(self, arg):
        """
        Delete a plan
        """
        print("connect to close plan...") #add function
        pass

    def do_return(self, arg):
        """
        Return to AdminShell
        """
        print("Return to main menu...")
        AdminShell(self.user).cmdloop()


class ManageVolunteerMenu(AdminShell):
    """
    ManageVolunteerMenu is the sub-class of command line interface for admin role.
    It will be launched when the admin choose #3 and enter do_manage_volunteer_account().
    """

    def volunteer_menu(self) -> None:
        print("\033[100m\033[4m\033[1m{}\033[0m\n".format("Manage Emergency Plan"))
        print(
            "[ 1 ] Create a new volunteer "
            "[ 2 ] Edit a volunteer profile\n"
            "[ 3 ] De-activate a volunteer Account\n"
            "[ 4 ] Re-activate a volunteer Account\n"
            "[ 5 ] Delete a volunteer Account\n\n"
            "[ R ] Return to previous page\n"
            "[ 0 ] Log-out\n")

    def precmd(self, option: str) -> str:
        """
        Handles two-word commands made with action words
        """
        admin_options = {"logout": 0, "create_volunteer": 1, "edit_volunteer": 2,
                         "deactivate_volunteer": 3, "reactivate_volunteer": 4, "delete_volunteer": 5,
                         "return": "r"}

        ### Add input error handling
        if option.isdigit() and int(option) in list(admin_options.values()):
            return list(admin_options.keys())[list(admin_options.values()).index(int(option))]
        elif option == ('x' or 'X'):
            return list(admin_options.keys())[list(admin_options.values()).index(option.lower())]
        elif option == ('r' or 'R'):
            return "return"
        else:
            return "invalid_input"


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
