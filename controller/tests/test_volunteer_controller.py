import unittest
import controller.volunteer_controller as vc
from models.plan import Plan
from models.camp import Camp
from models.volunteer import Volunteer


class TestVolunteerController(unittest.TestCase):

    def setUp(self):
        Volunteer.delete_all()
        camp_1 = Camp(name='Camp-1')
        camp_2 = Camp(name='Camp-2')
        camp_3 = Camp(name='Camp-3')
        Plan(name='Plan-1',
             emergency_type=Plan.EmergencyType.EARTHQUAKE,
             description='Test',
             geographical_area='',
             camps=[camp_1, camp_2])
        Plan(name='Plan-2',
             emergency_type=Plan.EmergencyType.EARTHQUAKE,
             description='Test',
             geographical_area='',
             camps=[camp_3])
        vc.create_volunteer(username='yunsy', password='root', firstname='Yunsy', lastname='Yin',
                            phone='+447519953189', camp=camp_1)

    def test_edit_firstname(self):
        volunteer = Volunteer.find('yunsy')
        volunteer = vc.edit_firstname(volunteer, 'Yun-Tzu')
        self.assertEqual(volunteer.firstname, 'Yun-Tzu')

    def test_edit_firstname_invalid_input(self):
        volunteer = Volunteer.find('yunsy')
        with self.assertRaises(vc.ControllerError):
            vc.edit_firstname(volunteer=volunteer, firstname='Y')

    def test_edit_lastname(self):
        volunteer = Volunteer.find('yunsy')
        volunteer = vc.edit_lastname(volunteer=volunteer, lastname='Yinnn')
        self.assertEqual(volunteer.lastname, 'Yinnn')

    def test_edit_lastname_invalid_input(self):
        volunteer = Volunteer.find('yunsy')
        with self.assertRaises(vc.ControllerError):
            vc.edit_lastname(volunteer=volunteer, lastname='Y')

    def test_edit_phone(self):
        volunteer = Volunteer.find('yunsy')
        volunteer = vc.edit_phone(volunteer=volunteer, phone='+441111111111')
        self.assertEqual(volunteer.phone, '+441111111111')

    def test_edit_phone_without_international_code(self):
        volunteer = Volunteer.find('yunsy')
        with self.assertRaises(vc.ControllerError):
            vc.edit_phone(volunteer=volunteer, phone='441111111111')

    def test_edit_phone_too_short(self):
        volunteer = Volunteer.find('yunsy')
        with self.assertRaises(vc.ControllerError):
            vc.edit_phone(volunteer=volunteer, phone='+44123')

    def test_edit_camp_by_admin(self):
        volunteer = Volunteer.find('yunsy')
        camp = Plan.find(key='Plan-2').camps.get('Camp-3')
        volunteer = vc.edit_camp(volunteer=volunteer, camp=camp, is_admin=True)
        self.assertEqual(str(volunteer.camp), 'Camp-3')

    def test_edit_camp_under_same_plan_by_volunteer(self):
        volunteer = Volunteer.find('yunsy')
        camp = Plan.find(key='Plan-1').camps.get('Camp-2')
        volunteer = vc.edit_camp(volunteer=volunteer, camp=camp, is_admin=False)
        self.assertEqual(str(volunteer.camp), 'Camp-2')

    def test_edit_camp_under_different_plan_by_volunteer(self):
        volunteer = Volunteer.find('yunsy')
        camp = Plan.find(key='Plan-2').camps.get('Camp-3')
        with self.assertRaises(vc.ControllerError):
            vc.edit_camp(volunteer=volunteer, camp=camp, is_admin=False)

    def test_edit_availability_false(self):
        volunteer = Volunteer.find('yunsy')
        volunteer = vc.edit_availability(volunteer=volunteer, availability=False)
        self.assertFalse(volunteer.availability)

    def test_edit_availability_true(self):
        volunteer = Volunteer.find('yunsy')
        volunteer = vc.edit_availability(volunteer=volunteer, availability=True)
        self.assertTrue(volunteer.availability)


if __name__ == '__main__':
    unittest.main()
