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


def find_volunteer(username: str) -> Volunteer:
    volunteer = Volunteer.find(username)
    if isinstance(volunteer, Volunteer):
        return volunteer
    else:
        raise ControllerError(f"User {username} not found. Please try again.")


def view_volunteer_profile(volunteer: Volunteer) -> str:
    return str(volunteer)


def edit_firstname(volunteer: Volunteer, firstname: str) -> Volunteer:
    volunteer_called = volunteer
    volunteer_called.firstname = firstname
    volunteer_called.save()
    return volunteer_called


def edit_lastname(volunteer: Volunteer, lastname: str) -> Volunteer:
    volunteer_called = volunteer
    volunteer_called.lastname = lastname
    volunteer_called.save()
    return volunteer_called


def edit_phone(volunteer: Volunteer, phone: str) -> Volunteer:
    volunteer_called = volunteer
    volunteer_called.phone = phone
    volunteer_called.save()
    return volunteer_called


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
        if old_camp.plan() == camp.plan():
            old_camp.volunteers.remove(volunteer_called)
            old_camp.save()
            camp.volunteers.add(volunteer_called)
            camp.save()
            return volunteer_called
        else:
            print("You can only select a camp under the same plan.")
            return volunteer_called


def edit_availability(volunteer: Volunteer, availability: str) -> Volunteer:
    volunteer_called = volunteer
    volunteer_called.availability = availability
    volunteer_called.save()
    return volunteer_called


def deactivate_volunteer(volunteer: Volunteer) -> Volunteer:
    volunteer.account_activated = False
    volunteer.save()
    return volunteer


def reactivate_volunteer(volunteer: Volunteer) -> Volunteer:
    volunteer.account_activated = True
    volunteer.save()
    return volunteer


def delete_volunteer(volunteer: Volunteer) -> None:
    volunteer.delete()
