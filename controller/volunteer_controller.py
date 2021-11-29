from models.volunteer import Volunteer
from models.camp import Camp


def find_volunteer(username: str) -> Volunteer:
    volunteer_called = Volunteer.find(username)
    return volunteer_called


def create_volunteer(username: str,
                     password: str,
                     firstname: str,
                     lastname: str,
                     phone: str,
                     camp: Camp) -> Volunteer:
    volunteer_called = Volunteer(username=username, password=password, firstname=firstname, lastname=lastname,
                                 phone=phone)
    camp.volunteers.add(volunteer_called)
    return volunteer_called


def view_volunteer_profile(volunteer: Volunteer) -> str:
    return str(volunteer)


def edit_volunteer_profile(volunteer: Volunteer, firstname: str, lastname: str,
                           phone: str) -> Volunteer:
    """
    Yunsy, Yingbo
    A function used by admin and volunteer
    Should include re-assign volunteer to a camp
    """
    # A new menu class EditVolunteerMenu was built to list the items to be edited in the new branch cli-edit-volunteer
    # The function edit_volunteer_profile is divided into 5 sub-functions according to the edited item.
    pass


def change_volunteer_camp(volunteer: Volunteer, camp: Camp, is_admin: bool) -> Volunteer:
    """
    The admin role
    :param is_admin: if this method is called by an admin
    :param volunteer:
    :param camp: the new camp
    :return:
    """
    # A new menu class EditVolunteerMenu was built to list the items to be edited including camp in the new branch cli-edit-volunteer
    pass


def deactivate_volunteer(volunteer: Volunteer) -> Volunteer:
    volunteer_called = volunteer
    volunteer_called.account_activated = False
    volunteer_called.save()
    return volunteer_called


def reactivate_volunteer(volunteer: Volunteer) -> Volunteer:
    volunteer_called = volunteer
    volunteer_called.account_activated = True
    volunteer_called.save()
    return volunteer_called


def delete_volunteer(volunteer: Volunteer) -> None:
    volunteer_called = volunteer
    volunteer_called.camp = None
    volunteer_called.delete()
