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
