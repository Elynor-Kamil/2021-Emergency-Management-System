import functools
from cmd import Cmd


class EmsShell(Cmd):
    """
    EmsShell is the main class for the command line interface.
    """
    prompt = '> '
    user = None  # TODO: type hint for user

    def login(self) -> None:
        """
        Prompts the user for a username and password to login to EMS.
        Loop until the user enters a valid username and password.
        """
        while self.user is None:
            username = input('Username: ')
            password = input('Password: ')
            try:
                self.user = 'volunteer'
                # raise Exception     # TODO: implement login
            except Exception:
                print('Invalid username or password, please try again.')

    def preloop(self) -> None:
        """
        Ask the user to login before entering the shell.
        :return:
        """
        print('Welcome to EMS, please login.')
        self.login()

    def require_user_type(self, *user_types):
        def decorator_require_user_type(func):
            @functools.wraps(func)
            def wrapper_require_user_type(*args, **kwargs):
                session = args[0]
                if session.user in user_types:  # TODO: implement user type checking
                    return func(*args, **kwargs)
                else:
                    print('You do not have permission to perform this action.')

            return wrapper_require_user_type

        return decorator_require_user_type

    @require_user_type('admin', 'volunteer')
    def do_profile(self, args):
        """
        Permission control demo.
        """
        print(f'user: {self.user}')

    @require_user_type('admin')
    def do_plans(self, args):
        """
        Permission control demo.
        """
        print('Not implemented')
