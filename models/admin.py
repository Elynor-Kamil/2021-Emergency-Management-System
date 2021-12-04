from models.user import User


class Admin(User):
    """
    Class for admin user
    """

    @classmethod
    def configure_initial_user(cls):
        """
        Configure initial admin user if no admin exists
        """
        if len(cls.all()) == 0:
            cls('root', 'root')
