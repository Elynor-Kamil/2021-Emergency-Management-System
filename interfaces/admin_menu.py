from interfaces.manage_plan import ManagePlanMenu
from interfaces.manage_refugee import ManageRefugeeMenu
from interfaces.manage_volunteer import ManageVolunteerMenu
from interfaces.base_menu import BaseMenu


class AdminMenu(BaseMenu):
    welcome_message = f'\033[1mWelcome to EMS. Please choose an option to continue:\033[0m'
    title = f'\n\033[100m\033[4m\033[1mAdmin Menu\033[0m'

    @property
    def exit_message(self):
        return f'\033[94mLogged out of {self.user.username}!\033[0m'

    def do_profile(self):
        """View my details"""
        print("\n\033[4m\033[1m{}\033[0m\n".format("Your details:") +
              f'{self.user}\n')
        return

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
