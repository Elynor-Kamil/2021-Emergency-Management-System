import glob
import os
from datetime import date

from models.admin import Admin

# delete existing data
from models.camp import Camp
from models.plan import Plan
from models.refugee import Refugee
from models.volunteer import Volunteer

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
               account_activated=True)
v3 = Volunteer(username='vvv3', password='33333', firstname='Volunteer', lastname='Three', phone='+44123456789',
               account_activated=False)

camps1[0].volunteers.add(v1)
camps1[1].volunteers.add(v2)
camps2[0].volunteers.add(v3)

r = Refugee(firstname='Refugee', lastname='One', num_of_family_member=4, starting_date=date(2021, 5, 4))
camps1[0].refugees.add(r)
