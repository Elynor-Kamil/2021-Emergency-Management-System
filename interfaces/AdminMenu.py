from interfaces.ManagePlanMenu import ManagePlanMenu
from interfaces.ManageRefugeeMenu import ManageRefugeeMenu
from interfaces.ManageVolunteerMenu import ManageVolunteerMenu
from interfaces.base_menu import BaseMenu


class AdminMenu(BaseMenu):
    welcome_message = f'\n\033[100m\033[4m\033[1mAdmin Menu\033[0m \n' \
                      f'\033[1mWelcome to EMS. Please choose an option to continue:\033[0m\n'

    @property
    def exit_message(self):
        return f'Logged out of {self.user.username}!'

    def do_profile(self):
        """View my details"""
        print("\n\033[100m\033[4m\033[1m{}\033[0m\n".format("Your details:") +
              f'Username: {self.user.username}\n'
              f'Role: {self.user.__class__.__name__}\n')

    def do_manage_plan(self):
        """Manage an emergency plan (Create/Close/View)"""
        ManagePlanMenu(self.user).run()

    def do_manage_volunteer_account(self):
        """Manage volunteer accounts and profile (Create/Edit/Deactivate/Delete)"""
        ManageVolunteerMenu(self.user).run()

    def do_manage_refugee_profile(self):
        """Manage Refugee Profile"""
        ManageRefugeeMenu(self.user).run()

    def exit_menu(self):
        """Logout"""
        return super().exit_menu()
