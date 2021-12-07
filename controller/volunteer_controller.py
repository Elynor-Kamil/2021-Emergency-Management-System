from models.base.document import Document
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
    if camp.plan.is_closed:
        raise ControllerError(f"Plan {camp.plan.name} is closed. Please choose another plan.")
    try:
        volunteer = Volunteer(username=username, password=password, firstname=firstname, lastname=lastname,
                              phone=phone)
        camp.volunteers.add(volunteer)
        return volunteer
    except (Volunteer.InvalidUsernameException,
            Volunteer.InvalidPasswordException,
            Volunteer.InvalidFirstnameException,
            Volunteer.InvalidLastnameException,
            Volunteer.InvalidPhoneException) as e:
        raise ControllerError(str(e))
    except Document.DuplicateKeyError as e:
        raise ControllerError(f"User {username} already exists. Please try again.")


def find_volunteer(username: str) -> Volunteer:
    volunteer = Volunteer.find(username)
    if isinstance(volunteer, Volunteer):
        return volunteer
    else:
        raise ControllerError(f"User {username} not found. Please try again.")


def view_volunteer_profile(volunteer: Volunteer) -> str:
    return str(volunteer)


def edit_firstname(volunteer: Volunteer, firstname: str) -> Volunteer:
    try:
        Volunteer.check_volunteer_firstname(firstname)
        volunteer.firstname = firstname
        volunteer.save()
        return volunteer
    except Volunteer.InvalidFirstnameException as e:
        raise ControllerError(str(e))


def edit_lastname(volunteer: Volunteer, lastname: str) -> Volunteer:
    try:
        Volunteer.check_volunteer_lastname(lastname)
        volunteer.lastname = lastname
        volunteer.save()
        return volunteer
    except Volunteer.InvalidLastnameException as e:
        raise ControllerError(str(e))


def edit_phone(volunteer: Volunteer, phone: str) -> Volunteer:
    try:
        Volunteer.check_volunteer_phone(phone)
        volunteer.phone = phone
        volunteer.save()
        return volunteer
    except Volunteer.InvalidPhoneException as e:
        raise ControllerError(str(e))


def edit_camp(volunteer: Volunteer, camp: Camp, is_admin: bool) -> Volunteer:
    old_camp = volunteer.camp
    if camp.plan.is_closed:
        raise ControllerError(f"Plan {camp.plan.name} is closed. Please choose another plan.")
    if is_admin:
        old_camp.volunteers.remove(volunteer)
        old_camp.save()
        camp.volunteers.add(volunteer)
        camp.save()
        return volunteer
    else:
        if old_camp.plan == camp.plan:
            old_camp.volunteers.remove(volunteer)
            old_camp.save()
            camp.volunteers.add(volunteer)
            camp.save()
            return volunteer
        else:
            raise ControllerError(f"Invalid camp: {camp}. You can only select a camp under the same plan.")


def edit_availability(volunteer: Volunteer, availability: bool) -> Volunteer:
    volunteer.availability = availability
    volunteer.save()
    return volunteer


def deactivate_volunteer(volunteer: Volunteer) -> Volunteer:
    if volunteer.account_activated == False:
        raise ControllerError(f"Volunteer {volunteer.username} is already deactivated.")
    volunteer.account_activated = False
    volunteer.save()
    return volunteer


def reactivate_volunteer(volunteer: Volunteer) -> Volunteer:
    if volunteer.account_activated == True:
        raise ControllerError(f"Volunteer {volunteer.username} is already active.")
    volunteer.account_activated = True
    volunteer.save()
    return volunteer


def delete_volunteer(volunteer: Volunteer) -> None:
    volunteer.delete()
