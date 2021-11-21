from cmd import Cmd

from interfaces.cli import EmsShell
from data.users import users_catalog
from models.admin import Admin
from models.user import User, require_role
from models.volunteer import Volunteer



class AdminShell(EmsShell):
    """
    AdminShell is the command line interface for admin role.
    """

    def __init__(self):
        """
        Initialise the admin user menu.
        """
        super(AdminShell, self).__init__()


    def admin_menu(self) -> None:
        print("""
         1) View my details 
         2) Manage emergency plan (Create/Close/View)
         3) Manage volunteer accounts and profile (Create/Edit/Deactivate/Delete)
         4) View camp details
         5) Assign volunteer to a new plan
         6) Manage refugee profile 
         
         0) Log-out 
         X) Exit
         """)


    def precmd(self, option: str) -> int:
        """
        Transfer option numbers to function name
        """
        admin_options = {"logout": 0, "profile": 1, "manage_plan": 2,
                         "manage_volunteer_account": 3,
                         "view_camp_details": 4,
                         "assign_volunteer": 5,
                         "manage_refugee_profile": 6, "exit": "x"}

        if option.isdigit():
            return list(admin_options.keys())[list(admin_options.values()).index(int(option))]
        elif option == 'x' or 'X':
            # ensure the input is in lower-case
            return list(admin_options.keys())[list(admin_options.values()).index(option.lower())]
        else:
            pass # Revise error handling


    def preloop(self) -> None:
        """
        Print out admin_menu before entering the shell.
        :return:
        """
        self.admin_menu()



    # ----- basic commands for admins-----
    def do_profile(self, arg):
        """
        Print user info
        """
        print(f'username: {self.user.username}\n'
              f'role: {self.user.__class__.__name__}')

    def do_manage_plan(self, arg):
        """
        Enter PlanMenu for further actions
        """
        PlanMenu().cmdloop()

    def do_manage_volunteer_account(self, arg):
        """
        Enter ManageVolunteerMenu for further actions
        """
        ManageVolunteerMenu().cmdloop()

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
        pass # add on function




class PlanMenu(AdminShell):
    def __init__(self):
        super(PlanMenu, self).__init__()

    def plan_menu(self) -> None:
        print("""
         Manage Emergency Plan
         --------
         1) Create a new emergency plan 
         2) View an emergency plan 
         3) Close an emergency plan

         R) Return to previous page
         """)


    def precmd(self, option: str) -> int:
        """
        Handles two-word commands made with action words
        """
        admin_options = {"logout": 0, "create_plan": 1, "view_plan": 2,
                         "close_plan": 3,
                         "return": "r"}
        if option.isdigit():
            return list(admin_options.keys())[list(admin_options.values()).index(int(option))]
        else:
            return list(admin_options.keys())[list(admin_options.values()).index(option.lower())]

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
        AdminShell().cmdloop()


class ManageVolunteerMenu(AdminShell):
    """
    ManageVolunteerMenu is the sub-class of command line interface for admin role.
    It will be launched when the admin choose #3 and enter do_manage_volunteer_account().
    """
    def __init__(self):
        super(ManageVolunteerMenu, self).__init__()

    def volunteer_menu(self) -> None:
        print("""
         Manage Emergency Plan
         --------
         1) Create a new volunteer 
         2) Edit a volunteer profile 
         3) De-activate a volunteer Account
         4) Re-activate a volunteer Account
         5) Delete a volunteer Account

         R) Return to previous page
         0) Log-out
         """)


    def precmd(self, option: str) -> int:
        """
        Handles two-word commands made with action words
        """
        admin_options = {"logout": 0, "create_volunteer": 1, "edit_volunteer": 2,
                         "deactivate_volunteer": 3, "reactivate_volunteer": 4, "delete_volunteer": 5,
                         "return": "r"}

        ### Add input error handling
        if option.isdigit():
            return list(admin_options.keys())[list(admin_options.values()).index(int(option))]
        else:
            return list(admin_options.keys())[list(admin_options.values()).index(option.lower())]


    def preloop(self) -> None:
        """
        Display manage volunteer menu.
        :return:
        """
        self.volunteer_menu()


    # ----- basic commands for volunteer account management -----
    def do_create_volunteer(self, username:str,  password: str):
        """
        Create a volunteer
        """
        print("connect to create a new volunteer...")
        username = input('Username: ')
        password = input('Password: ')
        new_volunteer = Volunteer(username=username, password=password)
        print(f"Successfully created volunteer {new_volunteer.username}")
        pass #add function and verification

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

    from cmd import Cmd

    from interfaces.cli import EmsShell
    from data.users import users_catalog
    from models.admin import Admin
    from models.user import User, require_role
    from models.volunteer import Volunteer

    class AdminShell(EmsShell):
        """
        AdminShell is the command line interface for admin role.
        """

        def __init__(self):
            """
            Initialise the admin user menu.
            """
            super(AdminShell, self).__init__()

        def admin_menu(self) -> None:
            print("""
             1) View my details 
             2) Manage emergency plan (Create/Close/View)
             3) Manage volunteer accounts and profile (Create/Edit/Deactivate/Delete)
             4) View camp details
             5) Assign volunteer to a new plan
             6) Manage refugee profile 

             0) Log-out 
             X) Exit
             """)

        def precmd(self, option: str) -> int:
            """
            Transfer option numbers to function name
            """
            admin_options = {"logout": 0, "profile": 1, "manage_plan": 2,
                             "manage_volunteer_account": 3,
                             "view_camp_details": 4,
                             "assign_volunteer": 5,
                             "manage_refugee_profile": 6, "exit": "x"}

            if option.isdigit():
                return list(admin_options.keys())[list(admin_options.values()).index(int(option))]
            elif option == 'x' or 'X':
                # ensure the input is in lower-case
                return list(admin_options.keys())[list(admin_options.values()).index(option.lower())]
            else:
                pass  # Revise error handling

        def preloop(self) -> None:
            """
            Print out admin_menu before entering the shell.
            :return:
            """
            self.admin_menu()

        # ----- basic commands for admins-----
        def do_profile(self, arg):
            """
            Print user info
            """
            print(f'username: {self.user.username}\n'
                  f'role: {self.user.__class__.__name__}')

        def do_manage_plan(self, arg):
            """
            Enter PlanMenu for further actions
            """
            PlanMenu().cmdloop()

        def do_manage_volunteer_account(self, arg):
            """
            Enter ManageVolunteerMenu for further actions
            """
            ManageVolunteerMenu().cmdloop()

        def do_manage_camp_details(self, arg):
            """
            Enter ManageCampMenu for further actions
            """
            pass

        def do_assign_volunteer(self, arg):
            """
            #5: Call assign_volunteer() function from Admin class
            """
            print("Assign a volunteer to a camp:")
            pass  # add  function

        def do_manage_refugee_profile(self, arg):
            """
            #6: Call function from Admin class
            """
            print("Edit refugee details")
            pass  # add on function


    class PlanMenu(AdminShell):
        def __init__(self):
            super(PlanMenu, self).__init__()

        def plan_menu(self) -> None:
            print("""
             Manage Emergency Plan
             --------
             1) Create a new emergency plan 
             2) View an emergency plan 
             3) Close an emergency plan

             R) Return to previous page
             """)

        def precmd(self, option: str) -> int:
            """
            Handles two-word commands made with action words
            """
            admin_options = {"logout": 0, "create_plan": 1, "view_plan": 2,
                             "close_plan": 3,
                             "return": "r"}
            if option.isdigit():
                return list(admin_options.keys())[list(admin_options.values()).index(int(option))]
            else:
                return list(admin_options.keys())[list(admin_options.values()).index(option.lower())]

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
            print("connect to create plan...")  # add function
            pass

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

        def do_return(self, arg):
            """
            Return to AdminShell
            """
            print("Return to main menu...")
            AdminShell().cmdloop()

    class ManageVolunteerMenu(AdminShell):
        """
        ManageVolunteerMenu is the sub-class of command line interface for admin role.
        It will be launched when the admin choose #3 and enter do_manage_volunteer_account().
        """

        def __init__(self):
            super(ManageVolunteerMenu, self).__init__()

        def volunteer_menu(self) -> None:
            print("""
             Manage Emergency Plan
             --------
             1) Create a new volunteer 
             2) Edit a volunteer profile 
             3) De-activate a volunteer Account
             4) Re-activate a volunteer Account
             5) Delete a volunteer Account

             R) Return to previous page
             0) Log-out
             """)

        def precmd(self, option: str) -> int:
            """
            Handles two-word commands made with action words
            """
            admin_options = {"logout": 0, "create_volunteer": 1, "edit_volunteer": 2,
                             "deactivate_volunteer": 3, "reactivate_volunteer": 4, "delete_volunteer": 5,
                             "return": "r"}

            ### Add input error handling
            if option.isdigit():
                return list(admin_options.keys())[list(admin_options.values()).index(int(option))]
            else:
                return list(admin_options.keys())[list(admin_options.values()).index(option.lower())]

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

        def do_return(self, arg):
            """
            Return to AdminShell
            """
            print("Return to main menu...")
            PlanMenu().cmdloop()




