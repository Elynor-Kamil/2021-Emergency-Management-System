import sys

from models.admin import Admin
from models.user import User
from models.volunteer import Volunteer


class LoginPage:
    def __init__(self, user=None):
        self.user = user

    def run(self):
        from interfaces.AdminMenu import AdminMenu
        from interfaces.VolunteerMenu import VolunteerMenu
        # login
        while self.user is None:
            username = input('Username: ')
            password = input('Password: ')
            try:
                user = User.find(username)
                if not user:
                    print("\033[31m {}\033[00m".format('** Account not found.'))
                    continue
                self.user = user.login(password)
                self.prompt = f'{self.user.username}> '
                print(f'\033[1mWelcome {self.user.username}. Your role is {self.user.__class__.__name__}.\033[0m\n')
                if isinstance(self.user, Admin):
                    AdminMenu(self.user).run()
                elif isinstance(self.user, Volunteer):
                    if not self.user.account_activated:
                        print("\033[31m {}\033[00m".format("** Your account is deactivated. Please contact admin."))
                        sys.exit()
                    VolunteerMenu(self.user).run()
                else:
                    print(f'Unsupported role: {self.user.__class__.__name__}')
                    continue
                # logout after user exit from inner menus
                self.user = None
                continue
            except (KeyError, User.InvalidPassword):
                print("\033[31m {}\033[00m".format("** Invalid username or password. Please try again."))


if __name__ == '__main__':
    Admin.configure_initial_user()
    LoginPage().run()
