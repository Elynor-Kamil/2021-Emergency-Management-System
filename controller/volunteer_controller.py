from models.volunteer import Volunteer
from models.camp import Camp


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
