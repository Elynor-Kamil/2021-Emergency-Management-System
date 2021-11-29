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
