from models.volunteer import Volunteer
from models.camp import Camp


###---- Manage Volunteer Menu ----
def create_volunteer(username: str,
                     password: str,
                     firstname: str,
                     lastname: str,
                     phone: str,
                     camp: Camp) -> Volunteer:
    """
    Yunsy, Yingbo
    """
    pass


def find_volunteer(username: str) -> Volunteer:
    pass


def view_volunteer_profile(volunteer: Volunteer) -> str:
    """
    Admin
    Yunsy, Yingbo
    """
    pass


def edit_volunteer_profile(volunteer: Volunteer, firstname: str, lastname: str,
                           phone: str) -> Volunteer:
    """
    Yunsy, Yingbo
    A function used by admin and volunteer
    Should include re-assign volunteer to a camp
    """
    pass


def change_volunteer_camp(volunteer: Volunteer, camp: Camp, is_admin: bool) -> Volunteer:
    """
    The admin role
    :param is_admin: if this method is called by an admin
    :param volunteer:
    :param camp: the new camp
    :return:
    """
    pass


def deactivate_volunteer(volunteer: Volunteer) -> Volunteer:
    """
    Yunsy, Yingbo
    """
    pass


def reactivate_volunteer(volunteer: Volunteer) -> Volunteer:
    """
    Yunsy, Yingbo
    """
    pass


def delete_volunteer(volunteer: Volunteer) -> None:
    """
    Yunsy, Yingbo
    """
    pass
