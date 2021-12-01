import re
from models.volunteer import Volunteer
from models.camp import Camp
from controller.controller_error import ControllerError


###---- Manage Volunteer Menu ----
def create_volunteer(username: str,
                     password: str,
                     firstname: str,
                     lastname: str,
                     phone: str,
                     camp: Camp) -> Volunteer:
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


def find_volunteer(username: str) -> Volunteer:
    pass


def view_volunteer_profile(volunteer: Volunteer) -> str:
    """
    Admin
    Yunsy, Yingbo
    """
    pass


def edit_firstname(volunteer: Volunteer, firstname: str) -> Volunteer:
    if len(firstname) > 1:
        volunteer_called = volunteer
        volunteer_called.firstname = firstname
        volunteer_called.save()
        return volunteer_called
    else:
        raise ControllerError(f"Invalid name: {firstname}. First name should be more than 1 character.")


def edit_lastname(volunteer: Volunteer, lastname: str) -> Volunteer:
    if len(lastname) > 1:
        volunteer_called = volunteer
        volunteer_called.lastname = lastname
        volunteer_called.save()
        return volunteer_called
    else:
        raise ControllerError(f"Invalid name: {lastname}. Last name should be more than 1 character.")


def edit_phone(volunteer: Volunteer, phone: str) -> Volunteer:
    phone_text = r"\+(9[976]\d|8[987530]\d|6[987]\d|5[90]\d|42\d|3[875]\d|2[98654321]\d|9[8543210]|8[6421]" \
                 r"|6[6543210]|5[87654321]|4[987654310]|3[9643210]|2[70]|7|1)\d{5,14}$"
    if re.search(phone_text, phone):
        volunteer_called = volunteer
        volunteer_called.phone = phone
        volunteer_called.save()
        return volunteer_called
    else:
        raise ControllerError(
            f"Invalid phone number: {phone}. Phone number should start with a plus sign and international code")


def edit_camp(volunteer: Volunteer, camp: Camp, is_admin: bool) -> Volunteer:
    volunteer_called = volunteer
    old_camp = volunteer_called.camp
    if is_admin:
        old_camp.volunteers.remove(volunteer_called)
        old_camp.save()
        camp.volunteers.add(volunteer_called)
        camp.save()
        return volunteer_called
    else:
        if old_camp.plan == camp.plan:
            old_camp.volunteers.remove(volunteer_called)
            old_camp.save()
            camp.volunteers.add(volunteer_called)
            camp.save()
            return volunteer_called
        else:
            raise ControllerError(f"Invalid camp: {camp}. You can only select a camp under the same plan.")


def edit_availability(volunteer: Volunteer, availability: str) -> Volunteer:
    list_true = ["True", "true", "T", "1"]
    list_false = ["False", "false", "F", "0"]
    if availability in list_true:
        volunteer_called = volunteer
        volunteer_called.availability = True
        volunteer_called.save()
        return volunteer_called
    elif availability in list_false:
        volunteer_called = volunteer
        volunteer_called.availability = False
        volunteer_called.save()
        return volunteer_called
    else:
        raise ControllerError(f"Invalid input: {availability}. Only 'True' or 'False' is accepted.")


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
