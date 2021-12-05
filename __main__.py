from interfaces.cmd.cli import EmsShell
from models.admin import Admin

if __name__ == '__main__':
    Admin.configure_initial_user()

    EmsShell().cmdloop()
