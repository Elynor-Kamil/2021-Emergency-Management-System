from controller import plan_controller, refugee_controller
from controller.controller_error import ControllerError
from interfaces.base_menu import BaseMenu
from models.admin import Admin
from datetime import datetime


class ManageRefugeeMenu(BaseMenu):
    title = f'\n\033[100m\033[4m\033[1mManage Refugee Menu\033[0m'

    @property
    def is_admin(self):
        return isinstance(self.user, Admin)

    def do_create_refugee(self):
        """Create a refugee profile"""
        print("\n\033[100m\033[4m\033[1m{}\033[0m ".format("Create a new refugee profile"))

        if self.is_admin:
            while True:
                plan_name = input("Enter the name of the plan the refugee belongs to (or press # to exit): ")
                if plan_name == '#':
                    return
                try:
                    plan = plan_controller.find_plan(plan_name)
                    break
                except ControllerError:
                    print(f"\033[31m * Plan '{plan_name}' not found. Please re-enter plan name. \033[00m")
                    continue

            while True:
                camp_name = input("Enter the name of the camp the refugee belongs to (or press # to exit): ")
                if camp_name == '#':
                    return
                try:
                    camp = plan_controller.find_camp(plan=plan, camp_name=camp_name)
                    break
                except ControllerError:
                    print(f"\033[31m * Camp {camp_name} not found. Please re-enter camp name. \033[00m")
                    continue
        else:
            camp = self.user.camp

        # STEP 3: get refugee info
        r_firstname = input("Enter refugee's first name: ")
        r_lastname = input("Enter refugee's last name: ")
        while True:
            try:
                num_of_family_member = int(input("Enter the number of family members (including the refugee):"))
                break
            except ValueError:
                print('\033[31m* Please input a valid integer\033[00m')

        # STEP 4: handle medical_condition
        print("Enter refugee's medical condition from the list")
        medical_condition_types = list(refugee_controller.list_medical_condition_types())
        for i, option in enumerate(medical_condition_types):
            print(f'[ {i} ] {option.value}')

        while True:
            medical_input = input("Enter refugee's medical condition from the list "
                                  "(leave empty for none, use comma to separate multiple inputs): ")
            if medical_input == '':
                r_conditions = []
                break
            medical_conditions = medical_input.replace(', ', ',').split(",")
            r_conditions = []
            for condition in medical_conditions:
                try:
                    r_condition = medical_condition_types[int(condition)]
                    r_conditions.append(r_condition)
                except (IndexError, ValueError):
                    print(f"\033[31m* '{condition}' is not on the list.\033[00m")
                    break
            else:
                break

        # STEP 5: Create refugee
        while True:
            try:
                refugee = refugee_controller.create_refugee(firstname=r_firstname, lastname=r_lastname, camp=camp,
                                                            num_of_family_member=num_of_family_member,
                                                            medical_condition_type=r_conditions,
                                                            starting_date=datetime.today().date())
                print(f"\x1b[6;30;42m success! \x1b[0m "
                      f"Refugee {r_firstname} {r_lastname} created.\n \033[1mRefugee ID: {refugee.user_id}\033[0m")
                print(f"\033[1m* Please note down refugee ID as it is required when viewing refugee profile.\033[0m\n")
                return
            except ControllerError as e:
                print(f'\033[31m* Failed to create refugee: {e}. '
                      f'Please check and retry.\033[00m')
                return

    def do_view_refugee(self):
        """View a refugee profile"""
        while True:
            user_input = input("Enter the refugee's ID to view (or # to exit): ")
            if user_input == "#":
                return
            try:
                refugee_id = int(user_input)
                try:
                    refugee = refugee_controller.find_refugee(refugee_id)
                    if not self.is_admin and refugee.camp != self.user.camp:
                        print(f"\033[31m* {refugee_id} not found. Please check and re-enter.\033[00m")
                        continue
                    print(f"\n\033[100m\033[4m\033[1mView refugee profile\033[0m")
                    print(refugee_controller.view_refugee(refugee))
                    return
                except ControllerError:
                    print(f"\033[31m* {refugee_id} not found. Please check and re-enter.\033[00m")
                    continue
            except ValueError:
                print(f'\033[31m* Invalid refugee ID {user_input}. Please check and re-enter.\033[00m')
