from controller import volunteer_controller, plan_controller
from controller.controller_error import ControllerError
from interfaces.base_menu import BaseMenu
from models.admin import Admin
from models.volunteer import Volunteer


class EditVolunteerMenu(BaseMenu):
    title = f'\n\033[100m\033[4m\033[1mEdit Volunteer Profile\033[0m \n'
    volunteer = None

    @property
    def is_admin(self):
        return isinstance(self.user, Admin)

    def before_run(self):
        if self.is_admin:
            while True:
                username = input("Enter Volunteer's username (or enter # to leave this page): ")
                if username == "#":
                    return True
                else:
                    try:
                        find_volunteer = volunteer_controller.find_volunteer(username)
                        self.volunteer = find_volunteer
                        return
                    except ControllerError:
                        print(f"\033[31m** Volunteer {username} not found. Please check and re-enter.\033[00m")
                        continue
        elif isinstance(self.user, Volunteer):
            self.volunteer = self.user
            return
        else:
            print(f'Unsupported role: {self.user.__class__.__name__}')
            return

    def print_menu(self):
        print("\n\033[100m\033[4m\033[1m{}\033[0m".format("Edit Volunteer Profile"))
        print(
            f"You're editing {self.volunteer.username}'s profile. Select the information to edit :\n"
            f"[ 0 ] First name: {self.volunteer.firstname}\n"
            f"[ 1 ] Last name: {self.volunteer.lastname}\n"
            f"[ 2 ] Phone number: {self.volunteer.phone}\n"
            f"[ 3 ] Camp: {self.volunteer.camp}\n"
            f"[ 4 ] Availability: {self.volunteer.availability}")
        for key, value in self.named_operations().items():
            print(f'[{key}] {value.__doc__}')

    def do_edit_firstname(self):
        print(f"Original first name is {self.volunteer.firstname}.")
        while True:
            firstname = input("Please enter new first name (or press # to exit this page):")
            if firstname == '#':
                return
            try:
                volunteer_controller.edit_firstname(self.volunteer, firstname)
                print(f"\x1b[6;30;42msuccess!\x1b[0m Volunteer's first name is changed to {self.volunteer.firstname}")
                return
            except ControllerError:
                print(
                    f"\033[31m** Invalid first name {firstname}. First name should have at least 2 characters.\033[00m")
                continue

    def do_edit_lastname(self):
        print(f"Original last name is {self.volunteer.lastname}.")
        while True:
            lastname = input("Please enter new last name (or press # to exit this page):")
            if lastname == '#':
                return
            try:
                volunteer_controller.edit_lastname(self.volunteer, lastname)
                print(f"\x1b[6;30;42msuccess!\x1b[0m Volunteer's last name is changed to {self.volunteer.lastname}")
                return
            except ControllerError:
                print(f"\033[31m** Invalid last name {lastname}. Last name should have at least 2 characters.\033[00m")
                continue

    def do_edit_phone(self):
        print(f"Original phone number is {self.volunteer.phone}.")
        print("(Phone number should include country code with a + sign.")
        while True:
            phone = input("Please enter new phone number (or press # to exit this page):")
            if phone == '#':
                EditVolunteerMenu(self.user).cmdloop()
                return
            try:
                volunteer_controller.edit_phone(self.volunteer, phone)
                print(f"\x1b[6;30;42msuccess!\x1b[0m Volunteer's phone number is changed to {self.volunteer.phone}")
                return
            except ControllerError:
                print(f"\033[31m** Invalid phone number {phone}. "
                      f"Phone number should include country code with a + sign.\033[00m")
                continue

    def do_edit_camp(self):
        print(f"Original assigned camp is {self.volunteer.camp} for Plan {self.volunteer.camp.plan}.")
        if self.is_admin:
            while True:
                plan_name = input("Enter the name of the new plan (or press # to exit): ")
                if plan_name == '#':
                    return
                try:
                    plan = plan_controller.find_plan(plan_name)
                    break
                except ControllerError:
                    print(f"\033[31m * Plan {plan_name} not found. Please re-enter plan name. \033[00m")
                    continue
        else:
            plan = self.volunteer.camp.plan

        # STEP 2: validate if camp exists
        while True:
            camp_name = input("Enter the name of the new camp (or press # to exit): ")
            if camp_name == '#':
                return
            try:
                camp = plan_controller.find_camp(plan=plan, camp_name=camp_name)
                break
            except ControllerError:
                print(f"\033[31m * Camp {camp_name} not found. Please re-enter camp name. \033[00m")
                continue

        try:
            volunteer_controller.edit_camp(self.volunteer, camp, self.is_admin)
            print(f"\x1b[6;30;42m success! \x1b[0m New assigned camp is {self.volunteer.camp}.")
        except ControllerError as e:
            print(f'Cannot change camp: {str(e)}')

    def do_edit_availability(self):
        print(f"Original availability is {self.volunteer.availability}.")
        while True:
            print('[1] - Available\n'
                  '[0] - Unavailable')
            availability = input("Please select new availability:")
            if availability == '1':
                availability = True
            elif availability == '0':
                availability = False
            else:
                print(f"\033[31m** Invalid option {availability}.\033[00m")
                continue
            break
        volunteer = volunteer_controller.edit_availability(self.volunteer, availability)
        status = 'available' if volunteer.availability else 'unavailable'
        print(f"\x1b[6;30;42m success! \x1b[0m Volunteer {volunteer.firstname} is now {status}.")
        return