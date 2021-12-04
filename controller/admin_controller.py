from models.user import User

###---- Admin Menu ----
def view_admin_profile(user: User) -> str:
    """
    Print information about the user.
    """
    return str(user)
