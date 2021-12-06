from interfaces.cmd.cli import EmsShell


class VolunteerShell(EmsShell):
    """
    VolunteerShell is the command line interface for volunteer role.
    """
    volunteer_options = {"logout": 0, "edit_details": 1, "manage_refugee_profile": 2,
                         "exit": "x"}

    def volunteer_menu(self) -> None:
        print("\033[100m\033[4m\033[1m{}\033[0m ".format("Volunteer Menu"))
        print("\033[1mWelcome to EMS. Please choose an option to continue:\033[0m\n"
              "[ 1 ] Edit my details\n"
              "[ 2 ] Manage Refugee Profile\n\n"
              "[ 0 ] Log-out\n"
              "[ X ] Exit\n")

    def precmd(self, option: str) -> str:
        """
        Transfer option numbers to function name for volunteer menu
        """
        if option.isdigit() and int(option) in list(self.volunteer_options.values()):
            return list(self.volunteer_options.keys())[list(self.volunteer_options.values()).index(int(option))]
        elif option.upper() == 'X' or option.upper() == 'R':
            return list(self.volunteer_options.keys())[list(self.volunteer_options.values()).index(option.lower())]
        else:
            return "invalid_input"

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
        from interfaces.cmd.edit_profile_cli import EditVolunteerMenu
        is_admin = False
        EditVolunteerMenu(self.user).cmdloop()

    def do_manage_refugee_profile(self, arg):
        """
        #2: Enter ManageRefugeeMenu for further actions
        """
        from interfaces.cmd.admin_cli import ManageRefugeeMenu
        ManageRefugeeMenu(self.user).cmdloop
