
###---- Manage Volunteer Menu ----
def create_volunteer():
    """
    Yunsy, Yingbo
    """
    pass


def view_volunteer_profile():
    """
    Yunsy, Yingbo
    """
    pass


def edit_volunteer_profile():
    """
    Yunsy, Yingbo
    A function used by admin and volunteer
    Should include re-assign volunteer to a camp
    """
    pass


def deactivate_volunteer():
    """
    Yunsy, Yingbo
    """
    pass


def reactivate_volunteer():
    """
    Yunsy, Yingbo
    """
    pass


def delete_volunteer():
    """
    Yunsy, Yingbo
    """
    pass




# font_end.py

def view_plan():
    plan_name = input('Please input plan name:')
    try:
        plan = find_plan(plan_name)
        print(plan_details(plan))
    except PlanNotFound:
        print(f'No plan named {plan_name}')

# controller.py

def find_plan(plan_name: str) -> Plan:
    pass

def plan_details(plan: Plan) -> str:
    pass
