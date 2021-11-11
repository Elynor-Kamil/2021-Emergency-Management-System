from cmd import Cmd

from data.users import users_catalog
from models.admin import Admin
from models.user import User, require_role
from models.volunteer import Volunteer


class EmsShell(Cmd):
    """
    EmsShell is the main class for the command line interface.
    """
    prompt = '> '
    user: User = None

    def login(self) -> None:
        """
        Prompts the user for a username and password to login to EMS.
        Loop until the user enters a valid username and password.
        """
        while self.user is None:
            username = input('Username: ')
            password = input('Password: ')
            try:
                self.user = users_catalog[username].login(password)
                print(f'Welcome {self.user.username}')
            except (KeyError, User.InvalidPassword):
                print('Invalid username or password. Please try again.')

    def do_logout(self, args):
        """
        Logout the current user, prompting for a new username and password.
        """
        self.user = None
        print('Logged out. Re-log in to continue')
        self.login()

    def preloop(self) -> None:
        """
        Ask the user to login before entering the shell.
        :return:
        """
        print('Welcome to EMS, please login.')
        self.login()

    @require_role(User)
    def do_profile(self, args):
        """
        Print user info
        """
        print(f'username: {self.user.username}'
              f'role: {self.user.__class__.__name__}')

    def do_create(self, args: str):
        """
        create methods
        """
        entity, *args = args.split()
        args = ' '.join(args)
        if entity == 'volunteer':
            self.do_create_volunteer(args)
        else:
            print(f'Unknown entity {entity}')

    @require_role(Admin)
    def do_create_volunteer(self, args):
        """
        Create a volunteer user
        """
        username = input('Username: ')
        password = input('Password: ')
        user = Volunteer(username, password)
        users_catalog[username] = user
