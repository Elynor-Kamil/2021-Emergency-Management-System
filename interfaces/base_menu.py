import sys

from models.admin import Admin
from models.user import User
from models.volunteer import Volunteer


class BaseMenu:
    menu_items = []
    welcome_message = "\033[96m{}\033[0m".format("Welcome to EMS, please enter your details.")

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        menu_items = []
        for attr_name, attr in cls.__dict__.items():
            if attr_name.startswith('do_') and callable(attr):
                menu_items.append(attr)
        cls.menu_items = menu_items

    def print_menu(self):
        """Display available actions"""
        for i, item in enumerate(self.menu_items):
            print(f'[{i}] {item.__doc__}')
        for key, value in self.named_operations().items():
            print(f'[{key}] {value.__doc__}')

    def call_menu_item(self, user_input):
        if user_input in self.named_operations():
            self.named_operations()[user_input](self)
        else:
            try:
                user_input = int(user_input)
                self.menu_items[user_input](self)
            except (IndexError, ValueError):
                print(f'Invalid input {user_input}')

    def exit_menu(self):
        """Exit the menu"""
        return True

    @classmethod
    def named_operations(cls):
        return {
            'H': cls.print_menu,
            'X': cls.exit_menu
        }

    def before_run(self):
        pass

    def run(self):
        print(self.welcome_message)
        self.before_run()
        self.print_menu()
        res = None
        while not res:
            item = input('Select an action: ')
            res = self.call_menu_item(item)
        print('Bye!')


class LoginPage:
    def __init__(self, user=None) -> object:
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
                    AdminMenu().run()
                elif isinstance(self.user, Volunteer):
                    if self.user.account_activated == True:
                        VolunteerMenu().run()
                    else:
                        print("\033[31m {}\033[00m".format("** Your account is deactivated. Please contact admin."))
                        sys.exit()
            except (KeyError, User.InvalidPassword):
                print("\033[31m {}\033[00m".format("** Invalid username or password. Please try again."))


if __name__ == '__main__':
    Admin.configure_initial_user()
    LoginPage().run()
