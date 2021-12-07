from controller import plan_controller, volunteer_controller
from controller.controller_error import ControllerError
from interfaces.base_menu import BaseMenu
from interfaces.edit_volunteer import EditVolunteerMenu
from models.admin import Admin


class ManageVolunteerMenu(BaseMenu):
    title = f'\n\033[100m\033[4m\033[1mManage Volunteer Menu\033[0m \n'
    def do_create_volunteer(self):
        """Create a volunteer"""
        print("\033[100m\033[4m\033[1m{}\033[0m ".format("Create a new volunteer account"))
        # STEP 1: validate if plan exists
        while True:
            plan = input("Enter the plan that the new volunteer belongs to (or press # to exit): ")
            if plan == '#':
                return
            try:
                find_plan = plan_controller.find_plan(plan)
                plan = find_plan
                break
            except ControllerError:
                print(f"\033[31m * Plan {plan} not found. Please re-enter plan name. \033[00m")
                continue

        # STEP 2: validate if camp exists
        while True:
            camp = input("Enter the camp that the new volunteer belongs to (or press # to exit): ")
            if camp == '#':
                return
            try:
                find_camp = plan_controller.find_camp(plan=plan, camp_name=camp)
                camp = find_camp
                break
            except ControllerError:
                print(f"\033[31m * Camp {camp} not found. Please re-enter camp name. \033[00m")
                continue

        # STEP 3: other user inputs
        while True:
            username = input("Enter volunteer's username: ")
            password = input("Enter volunteer's password: ")
            firstname = input("Enter volunteer's first name: ")
            lastname = input("Enter volunteer's last name: ")
            phone = input("Enter volunteer's phone (start from + sign and national code): ")

            try:
                volunteer_controller.create_volunteer(username=username,
                                                      password=password,
                                                      firstname=firstname,
                                                      lastname=lastname,
                                                      phone=phone, camp=camp)
                print(f"\x1b[6;30;42m success! \x1b[0m Volunteer {username} created.\n")
                return
            except ControllerError as e:
                print(f'\033[31mFailed to create volunteer \033[00m{username} due to the following reasons:')
                print(f'\033[31m* {e.message} \033[00m')
                return

    def do_view_volunteer(self):
        """View a volunteer's details"""
        while True:
            username = input("Enter the volunteer's username to view (Press # to leave this page): ")
            if username == '#':
                return
            try:
                find_volunteer = volunteer_controller.find_volunteer(username)
                print(volunteer_controller.view_volunteer_profile(find_volunteer))
                return
            except ControllerError:
                print(f"\033[31m* Volunteer {username} not found. Please check and re-enter.\033[00m")
                continue

    def do_edit_volunteer(self):
        """Edit a volunteer's details"""
        EditVolunteerMenu(self.user).run()

    def do_deactivate_volunteer(self):
        """Deactivate a volunteer account"""
        while True:
            username = input("Enter the volunteer's username to deactivate (Press # to leave this page): ")
            if username == '#':
                return
            try:
                find_volunteer = volunteer_controller.find_volunteer(username)
                volunteer_controller.deactivate_volunteer(find_volunteer)
                print(f"\x1b[6;30;42m success! \x1b[0m Volunteer {username} deactivated.\n")
                return
            except ControllerError:
                print(f"\033[31m* Volunteer {username} not found. Please check and re-enter.\033[00m")
                continue

    def do_reactivate_volunteer(self):
        """Reactivate a volunteer account"""
        while True:
            username = input("Enter the volunteer's username to reactivate (Press # to leave this page): ")
            if username == '#':
                return
            try:
                find_volunteer = volunteer_controller.find_volunteer(username)
                volunteer_controller.reactivate_volunteer(find_volunteer)
                print(f"\x1b[6;30;42m success! \x1b[0mVolunteer {username} reactivated.\n")
                return
            except ControllerError:
                print(f"\033[31m* Volunteer {username} not found. Please check and re-enter.\033[00m")
                continue

    def do_delete_volunteer(self):
        """Delete a volunteer"""
        while True:
            username = input("Enter the volunteer's username to delete (Press # to leave this page): ")
            if username == '#':
                return
            try:
                find_volunteer = volunteer_controller.find_volunteer(username)
                volunteer_controller.delete_volunteer(find_volunteer)
                print("\x1b[6;30;42m success! \x1b[0m")
                print(f"Volunteer {username} deleted.")
                return
            except ControllerError:
                print(f"\033[31m* Volunteer {username} not found. Please check and re-enter.\033[00m")
                continue
