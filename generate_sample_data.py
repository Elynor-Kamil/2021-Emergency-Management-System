import glob
import os
from datetime import date

from models.admin import Admin
from models.camp import Camp
from models.plan import Plan
from models.refugee import Refugee
from models.volunteer import Volunteer

if __name__ == '__main__':

    # delete existing data

    files = glob.glob('data/*')
    for f in files:
        os.remove(f)

    Admin.configure_initial_user()

    camps1 = [
        Camp(name='camp1'),
        Camp(name='camp2'),
        Camp(name='camp3')
    ]

    camps2 = [
        Camp(name='camp4'),
        Camp(name='camp5')
    ]

    plan1 = Plan(name='plan1', emergency_type=Plan.EmergencyType.FIRE,
                 description='This is Plan 1', geographical_area='World', camps=camps1)

    plan2 = Plan(name='plan2', emergency_type=Plan.EmergencyType.FLOOD,
                 description='This is Plan 2', geographical_area='UK', camps=camps2)

    v1 = Volunteer(username='vvv1', password='11111', firstname='Volunteer', lastname='One', phone='+44123456789')
    v2 = Volunteer(username='vvv2', password='22222', firstname='Volunteer', lastname='Two', phone='+44123456789',
                   availability=False)
    v3 = Volunteer(username='vvv3', password='33333', firstname='Volunteer', lastname='Three', phone='+44123456789',
                   account_activated=False)

    camps1[0].volunteers.add(v1)
    camps1[1].volunteers.add(v2)
    camps2[0].volunteers.add(v3)

    r1 = Refugee(firstname='Refugee', lastname='One', num_of_family_member=54, starting_date=date(2021, 5, 4))
    camps1[0].refugees.add(r1)
    r2 = Refugee(firstname='Refugee', lastname='Two', num_of_family_member=203, starting_date=date(2020, 7, 16),
                 medical_condition_type=[Refugee.MedicalCondition.HIV, Refugee.MedicalCondition.DIABETES])
    camps1[1].refugees.add(r2)
    r3 = Refugee(firstname='Refugee', lastname='Three', num_of_family_member=325, starting_date=date(2020, 3, 21))
    camps2[0].refugees.add(r3)
    print(f'Refugee 1 id: {r1.user_id}')
    print(f'Refugee 2 id: {r2.user_id}')
    print(f'Refugee 3 id: {r3.user_id}')

    print('Sample data generated successfully')
