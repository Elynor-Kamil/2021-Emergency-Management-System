from interfaces.base_menu import BaseMenu
from interfaces.edit_volunteer import EditVolunteerMenu
from interfaces.manage_refugee import ManageRefugeeMenu


class VolunteerMenu(BaseMenu):
    title = f'\n\033[100m\033[4m\033[1mVolunteer Menu\033[0m'
    welcome_message = f'\033[1mWelcome to EMS. Please choose an option to continue:\033[0m\n'

    @property
    def exit_message(self):
        return f'Logged out of {self.user.username}!'

    def do_edit_details(self):
        """Edit my details"""
        EditVolunteerMenu(self.user).run()

    def do_manage_refugee_profile(self):
        """Manage refugees"""
        if self.user.camp.plan.is_closed:
            print("\033[31m {}\033[00m".format("** The plan you are assigned to is closed. Please contact admin."))
            return
        ManageRefugeeMenu(self.user).run()

    def exit_menu(self):
        """Logout"""
        return super().exit_menu()
