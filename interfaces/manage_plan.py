from controller import plan_controller
from controller.controller_error import ControllerError
from interfaces.base_menu import BaseMenu
from models.plan import Plan


class ManagePlanMenu(BaseMenu):
    title = f'\n\033[100m\033[4m\033[1mManage Plan Menu\033[0m \n'

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
                print(f'\033[31m* Type {emergency_input} is not on the list.\033[00m')
                continue

        e_description = input("Enter description: ")
        e_geo_area = input("Enter geographical area: ")
        while True:
            camps_input = input("Enter camp names (use comma to separate camps): ")
            camp_names = camps_input.replace(', ', ',').split(",")
            if camp_names == '':
                print("\033[31m {}\033[00m".format("** Camp name cannot be empty."))
                continue
            try:
                camps = [plan_controller.create_camps(name) for name in camp_names]
                break
            except ControllerError as e:
                print("\033[31m {}\033[00m".format(f"** Failed to create camps: {e}. \nPlease check and re-enter"))
                continue
        try:
            plan_controller.create_plan(plan_name=e_name,
                                        emergency_type=emergency_type,
                                        description=e_description,
                                        geographical_area=e_geo_area,
                                        camps=camps)
            print(f"\x1b[6;30;42m success! \x1b[0m\t Plan {e_name} created.")
            return
        except ControllerError:
            print("\033[31m {}\033[00m".format("** Unable to create an emergency plan."))
            return

    def do_list_plans(self):
        """List out all the existing plans"""
        print("\n\033[100m\033[4m\033[1m{}\033[0m ".format("Existing Plans"))
        for plan in plan_controller.list_plans():
            print(plan)
        return

    def do_view_plan(self):
        """View a plan"""
        while True:
            plan_name = input("Enter the plan name (or # to exit): ")
            if plan_name == '#':
                return
            try:
                find_plan = plan_controller.find_plan(plan_name)
                print("\033[100m\033[4m\033[1m{}\033[0m\n".format("View Plan statistics"))
                print(plan_controller.view_plan_statistics(find_plan))
                return
            except ControllerError:
                print(f"\033[31m * Plan {plan_name} not found. Please re-enter plan name. \033[00m")
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
                print(f"\033[31m * Plan {plan_name} not found. Please re-enter plan name. \033[00m")
                continue
            plan_controller.close_plan(find_plan)
            print("\x1b[6;30;42m success! \x1b[0m\t")
            print(f"Plan {plan_name} Closed.")
            return
