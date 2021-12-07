from interfaces.login import LoginPage
from models.admin import Admin


class BaseMenu:
    menu_items = []
    welcome_message = None
    title = None
    exit_message = None

    class InvalidAction(Exception):
        pass

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
            print(f'[ {i} ] {item.__doc__}')
        for key, value in self.named_operations().items():
            print(f'[ {key} ] {value.__doc__}')

    def call_menu_item(self, user_input):
        user_input = user_input.upper()  # make it case insensitive
        if user_input in self.named_operations():
            return self.named_operations()[user_input](self)
        else:
            try:
                user_input = int(user_input)
                if user_input < 0:
                    raise self.InvalidAction
                return self.menu_items[user_input](self)
            except (IndexError, ValueError):
                raise self.InvalidAction

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
        if self.before_run():  # return True in before_run to exit menu
            return
        res = None
        while not res:
            if self.title:
                print(self.title)
            if self.welcome_message:
                print(self.welcome_message)
            self.print_menu()
            while True:
                item = input(f'({self.user.username}) Select an action: ')
                try:
                    res = self.call_menu_item(item)  # return True in function to exit menu
                    break
                except self.InvalidAction:
                    print(f'\033[31m* Invalid input {item}. Please enter an option from the menu.\033[00m')
        if self.exit_message:
            print(self.exit_message)
            return
