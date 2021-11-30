from models.volunteer import Volunteer
from models.camp import Camp
from controller.controller_error import ControllerError

    def do_return(self):
        ManageVolunteerMenu().cmdloop()


###---- Manage Volunteer Menu ----
def create_volunteer(username: str,
                     password: str,
                     firstname: str,
                     lastname: str,
                     phone: str,
                     camp: Camp) -> Volunteer:
    if isinstance(camp, Camp):
        try:
            volunteer_called = Volunteer(username=username, password=password, firstname=firstname, lastname=lastname,
                                         phone=phone)
            camp.volunteers.add(volunteer_called)
            return volunteer_called
        except Volunteer.InvalidUsernameException:
            raise ControllerError(f"Invalid username: {username}. Username should be at least 4 characters.")
        except Volunteer.InvalidPasswordException:
            raise ControllerError(f"Invalid password: {password}. Password should be at least 4 characters.")
        except Volunteer.InvalidFirstnameException:
            raise ControllerError(f"Invalid name: {firstname}. First name should be more than 1 character.")
        except Volunteer.InvalidLastnameException:
            raise ControllerError(f"Invalid name: {lastname}. Last name should be more than 1 character.")
        except Volunteer.InvalidPhoneException:
            raise ControllerError(
                f"Invalid phone number: {phone}. Phone number should start with a plus sign and international code")
    else:
        raise ControllerError(f"Camp {camp} does not exist.")


def find_volunteer(username: str) -> Volunteer:
    volunteer_called = Volunteer.find(username)
    if isinstance(volunteer_called, Volunteer):
        return volunteer_called
    else:
        raise ControllerError(f"Invalid username: {username}. Please try again.")


def view_volunteer_profile(volunteer: Volunteer) -> str:
    if isinstance(volunteer, Volunteer):
        return str(volunteer)
    else:
        raise ControllerError(f"Invalid input: {volunteer}. Please try again.")


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
    if isinstance(volunteer, Volunteer):
        volunteer_called = volunteer
        volunteer_called.account_activated = False
        volunteer_called.save()
        return volunteer_called
    else:
        raise ControllerError(f"Invalid input: {volunteer}. Please try again.")


def reactivate_volunteer(volunteer: Volunteer) -> Volunteer:
    if isinstance(volunteer, Volunteer):
        volunteer_called = volunteer
        volunteer_called.account_activated = True
        volunteer_called.save()
        return volunteer_called
    else:
        raise ControllerError(f"Invalid input: {volunteer}. Please try again.")


def delete_volunteer(volunteer: Volunteer) -> None:
    if isinstance(volunteer, Volunteer):
        volunteer.delete()
    else:
        raise ControllerError(f"Invalid input: {volunteer}. Please try again.")
