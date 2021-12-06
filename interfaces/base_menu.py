from interfaces.login import LoginPage
from models.admin import Admin


class BaseMenu:
    menu_items = []
    welcome_message = "\033[96m{}\033[0m".format("Welcome to EMS, please enter your details.")
    exit_message = None

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        menu_items = []
        for attr_name, attr in cls.__dict__.items():
            if attr_name.startswith('do_') and callable(attr):
                menu_items.append(attr)
        cls.menu_items = menu_items

    def __init__(self, user):
        self.user = user

    def print_menu(self):
        """Display available actions"""
        for i, item in enumerate(self.menu_items):
            print(f'[{i}] {item.__doc__}')
        for key, value in self.named_operations().items():
            print(f'[{key}] {value.__doc__}')

    def call_menu_item(self, user_input):
        if user_input in self.named_operations():
            return self.named_operations()[user_input](self)
        else:
            try:
                user_input = int(user_input)
                return self.menu_items[user_input](self)
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
            item = input(f'[{self.user.username}] Select an action: ')
            res = self.call_menu_item(item)
        if self.exit_message:
            print(self.exit_message)


class DemoMenu(BaseMenu):
    user = None

    def do_demo(self):
        """Prints 'Hello World'"""
        print('Hello World')

    def do_greeting(self):
        """Personalised greeting"""
        if self.user:
            print(f'Hello {self.user}')
        else:
            print('Please login first')

    def do_login(self):
        """Login"""
        user = input('Enter your name: ')
        self.user = user
        print('Logged in')

    def do_mange_plans(self):
        """Manage plans"""
        print('You are back to demo menu')
        self.print_menu()

    def logout(self):
        """Logout"""
        print('Logged out')

    @classmethod
    def named_operations(cls):
        return super().named_operations() | {
            'O': cls.logout
        }
