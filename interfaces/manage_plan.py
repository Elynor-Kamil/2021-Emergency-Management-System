from controller import plan_controller
from controller.controller_error import ControllerError
from interfaces.base_menu import BaseMenu


class ManagePlanMenu(BaseMenu):
    title = f'\n\033[100m\033[4m\033[1mManage Plan Menu\033[0m'

    def do_create_plan(self):
        """Create a plan"""
        print("\n\033[100m\033[4m\033[1m{}\033[0m ".format("Create a new emergency plan"))
        e_name = input("Enter emergency plan name (or press # to exit): ")
        if e_name == '#':
            return
        # -- handle emergency type
        print("Enter a emergency type from the list")
        emergency_types = list(plan_controller.list_emergency_types())
        for i, option in enumerate(emergency_types):
            print(f'[ {i} ] {option.value}')

        while True:
            emergency_input = input("Enter a emergency type number from the list: ")
            try:
                emergency_id = int(emergency_input)
                emergency_type = emergency_types[emergency_id]
                break
            except (IndexError, ValueError):
                print(f"\033[31m* '{emergency_input}' is not on the list.\033[00m")
                continue

        e_description = input("Enter description: ")
        e_geo_area = input("Enter geographical area: ")
        while True:
            camps_input = input("Enter camp names (use comma to separate camps): ")
            camp_names = camps_input.replace(', ', ',').split(",")
            try:
                camps = [plan_controller.create_camps(name) for name in camp_names]
                break
            except ControllerError as e:
                print(f"\033[31m* Failed to create camps: {e}.\033[00m")
                continue
        try:
            plan_controller.create_plan(plan_name=e_name,
                                        emergency_type=emergency_type,
                                        description=e_description,
                                        geographical_area=e_geo_area,
                                        camps=camps)
            print(f"\x1b[6;30;42m success! \x1b[0m\t Plan '{e_name}' created.")
            return
        except ControllerError as e:
            print(f"\033[31m* Unable to create an emergency plan: {e}\033[00m")
            return

    def do_list_plans(self):
        """List out all the existing plans"""
        print("\n\033[100m\033[4m\033[1m{}\033[0m ".format("Existing Plans"))
        if not plan_controller.list_plans():
            print("\033[31m * No existing plan. \033[00m")
        for plan in plan_controller.list_plans():
            print(plan, '\n')
        return

    def do_view_plan(self):
        """View a plan"""
        while True:
            plan_name = input("Enter the plan name (or # to exit): ")
            if plan_name == '#':
                return
            try:
                find_plan = plan_controller.find_plan(plan_name)
                print("\n\033[100m\033[4m\033[1m{}\033[0m".format("View Plan statistics"))
                print(plan_controller.view_plan_statistics(find_plan))
                return
            except ControllerError:
                print(f"\033[31m * Plan '{plan_name}' not found. Please re-enter plan name. \033[00m")
                continue

    def do_close_plan(self):
        """Close a plan"""
        while True:
            plan_name = input("Enter the plan name (or # to exit): ")
            if plan_name == '#':
                return
            try:
                find_plan = plan_controller.find_plan(plan_name)
            except ControllerError:
                print(f"\033[31m * Plan '{plan_name}' not found. Please re-enter plan name. \033[00m")
                continue
            try:
                plan_controller.close_plan(find_plan)
                print("\x1b[6;30;42m success! \x1b[0m\t")
                print(f"Plan '{plan_name}' Closed.")
                return
            except ControllerError as e:
                print(f"\033[31m * Failed to close plan: {e}\033[00m")
                return
