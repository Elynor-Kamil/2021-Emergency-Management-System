from interfaces.login import LoginPage
from models.admin import Admin

if __name__ == '__main__':
    Admin.configure_initial_user()

    LoginPage().run()
