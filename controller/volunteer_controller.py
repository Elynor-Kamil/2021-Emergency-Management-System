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


def edit_firstname(username: str, firstname: str) -> Volunteer:
    volunteer_called = find_volunteer(username)
    volunteer_called.firstname = firstname
    volunteer_called.save()
    return volunteer_called


def edit_lastname(username: str, lastname: str) -> Volunteer:
    volunteer_called = find_volunteer(username)
    volunteer_called.lastname = lastname
    volunteer_called.save()
    return volunteer_called


def edit_phone(username: str, phone: str) -> Volunteer:
    volunteer_called = find_volunteer(username)
    volunteer_called.phone = phone
    volunteer_called.save()
    return volunteer_called


def edit_camp(username: str, camp: Camp, is_admin: bool) -> Volunteer:
    if is_admin:
        volunteer_called = find_volunteer(username)
        old_camp = volunteer_called.camp
        old_camp.volunteers.remove(volunteer_called)
        old_camp.save()
        camp.volunteers.add(volunteer_called)
        camp.save()
        return volunteer_called
    else:
        volunteer_called = find_volunteer(username)
        old_camp = volunteer_called.camp
        if old_camp.plan() == camp.plan():
            old_camp.volunteers.remove(volunteer_called)
            old_camp.save()
            camp.volunteers.add(volunteer_called)
            camp.save()
            return volunteer_called
        else:
            print("You can only select a camp under the same plan.")
            return volunteer_called


def edit_availability(username: str, availability: str) -> Volunteer:
    volunteer_called = find_volunteer(username)
    volunteer_called.availability = availability
    volunteer_called.save()
    return volunteer_called


def deactivate_volunteer(username: str) -> Volunteer:
    volunteer_called = find_volunteer(username)
    volunteer_called.account_activated = False
    volunteer_called.save()
    return volunteer_called


def reactivate_volunteer(username: str) -> Volunteer:
    volunteer_called = find_volunteer(username)
    volunteer_called.account_activated = True
    volunteer_called.save()
    return volunteer_called


def delete_volunteer(username: str) -> None:
    volunteer_called = find_volunteer(username)
    volunteer_called.camp = None
    volunteer_called.delete()
