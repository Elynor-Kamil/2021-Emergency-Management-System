from cmd import Cmd

from interfaces.cli import EmsShell
from data.users import users_catalog
from models.admin import Admin
from models.user import User, require_role
from models.volunteer import Volunteer


class VolunteerShell(EmsShell):
    """
    VolunteerShell is the command line interface for volunteer role.
    """

    def __init__(self):
        """
        Initialise the volunteer user menu.
        """
        super(VolunteerShell, self).__init__()

    def volunteer_menu(self) -> None:
        print("""
         1) Edit my details 
         2) Manage refugee profile
         3) View current camp details

         0) Log-out 
         X) Exit
         """)

    def precmd(self, option: str) -> int:
        """
        Transfer option numbers to function name
        """
        volunteer_options = {"logout": 0, "edit_details": 1, "manage_refugee_profile": 2,
                             "view_camp_details": 3, "exit": "x"}

        if option.isdigit():
            return list(volunteer_options.keys())[list(volunteer_options.values()).index(int(option))]
        elif option == 'x' or 'X':
            # ensure the input is in lower-case
            return list(volunteer_options.keys())[list(volunteer_options.values()).index(option.lower())]
        else:
            pass  # Revise error handling

    def preloop(self) -> None:
        """
        Print out admin_menu before entering the shell.
        :return:
        """
        self.volunteer_menu()


    # ----- basic commands for admins-----
    def do_edit_details(self, arg):
        """
        #1: Edit volunteer's details (name, phone, camp, availability)
        """
        print(f""" Your current details:
                """)
        pass #add edit function from Volunteer Class

    def do_manage_refugee_profile(self, arg):
        """
        #2: Enter PlanMenu for further actions
        """
        pass


    def do_view_current_camp_details(self, arg):
        """
        #3: Read camp statistics
        """
        pass


