import unittest
import controller.volunteer_controller as vc
from models.camp import Camp
from models.plan import Plan


class TestVolunteerController(unittest.TestCase):

    def test_edit_firstname(self):
        volunteer = vc.create_volunteer(username='yunsy', password='root', firstname='Yunsy', lastname='Yin',
                                        phone='+447519953189', camp=Camp(name='UCL'))
        volunteer = vc.edit_firstname(volunteer, 'Yun-Tzu')
        self.assertEqual(volunteer.firstname, 'Yun-Tzu')

    def test_edit_firstname_invalid_input(self):
        with self.assertRaises(vc.ControllerError):
            volunteer = vc.create_volunteer(username='yunsy', password='root', firstname='Yunsy', lastname='Yin',
                                            phone='+447519953189', camp=Camp(name='UCL'))
            vc.edit_firstname(volunteer=volunteer, firstname='Y')

    def test_edit_lastname(self):
        volunteer = vc.create_volunteer(username='yunsy', password='root', firstname='Yunsy', lastname='Yin',
                                        phone='+447519953189', camp=Camp(name='UCL'))
        volunteer = vc.edit_lastname(volunteer=volunteer, lastname='Yinnn')
        self.assertEqual(volunteer.lastname, 'Yinnn')

    def test_edit_lastname_invalid_input(self):
        with self.assertRaises(vc.ControllerError):
            volunteer = vc.create_volunteer(username='yunsy', password='root', firstname='Yunsy', lastname='Yin',
                                            phone='+447519953189', camp=Camp(name='UCL'))
            vc.edit_lastname(volunteer=volunteer, lastname='Y')

    def test_edit_phone(self):
        volunteer = vc.create_volunteer(username='yunsy', password='root', firstname='Yunsy', lastname='Yin',
                                        phone='+447519953189', camp=Camp(name='UCL'))
        volunteer = vc.edit_phone(volunteer=volunteer, phone='+441111111111')
        self.assertEqual(volunteer.phone, '+441111111111')

    def test_edit_phone_without_international_code(self):
        with self.assertRaises(vc.ControllerError):
            volunteer = vc.create_volunteer(username='yunsy', password='root', firstname='Yunsy', lastname='Yin',
                                            phone='+447519953189', camp=Camp(name='UCL'))
            vc.edit_phone(volunteer=volunteer, phone='441111111111')

    def test_edit_phone_too_short(self):
        with self.assertRaises(vc.ControllerError):
            volunteer = vc.create_volunteer(username='yunsy', password='root', firstname='Yunsy', lastname='Yin',
                                            phone='+447519953189', camp=Camp(name='UCL'))
            vc.edit_phone(volunteer=volunteer, phone='+44123')

    def test_edit_camp_by_admin(self):
        volunteer = vc.create_volunteer(username='yunsy', password='root', firstname='Yunsy', lastname='Yin',
                                        phone='+447519953189', camp=Camp(name='UCL'))
        volunteer = vc.edit_camp(volunteer=volunteer, camp=Camp(name='Euston'), is_admin=True)
        self.assertEqual(str(volunteer.camp), 'Euston')

    def test_edit_camp_under_same_plan_by_volunteer(self):
        camp_1 = Camp(name='Camp 1')
        camp_2 = Camp(name='Camp 2')
        Plan(name='Plan A',
             emergency_type=Plan.EmergencyType.EARTHQUAKE,
             description='Test',
             geographical_area='',
             camps=[camp_1, camp_2])
        volunteer = vc.create_volunteer(username='yunsy', password='root', firstname='Yunsy', lastname='Yin',
                                        phone='+447519953189', camp=camp_1)
        volunteer = vc.edit_camp(volunteer=volunteer, camp=camp_2, is_admin=False)
        self.assertEqual(str(volunteer.camp), 'Camp 2')

    def test_edit_camp_under_different_plan_by_volunteer(self):
        with self.assertRaises(vc.ControllerError):
            camp_1 = Camp(name='Camp 1')
            camp_2 = Camp(name='Camp 2')
            Plan(name='Plan A',
                 emergency_type=Plan.EmergencyType.EARTHQUAKE,
                 description='Test',
                 geographical_area='',
                 camps=[camp_1])
            Plan(name='Plan B',
                 emergency_type=Plan.EmergencyType.EARTHQUAKE,
                 description='Test',
                 geographical_area='',
                 camps=[camp_2])
            volunteer = vc.create_volunteer(username='yunsy', password='root', firstname='Yunsy', lastname='Yin',
                                            phone='+447519953189', camp=camp_1)
            vc.edit_camp(volunteer=volunteer, camp=camp_2, is_admin=False)

    def test_edit_availability_false(self):
        volunteer = vc.create_volunteer(username='yunsy', password='root', firstname='Yunsy', lastname='Yin',
                                        phone='+447519953189', camp=Camp(name='UCL'))
        volunteer = vc.edit_availability(volunteer=volunteer, availability='False')
        self.assertFalse(volunteer.availability)

    def test_edit_availability_true(self):
        volunteer = vc.create_volunteer(username='yunsy', password='root', firstname='Yunsy', lastname='Yin',
                                        phone='+447519953189', camp=Camp(name='UCL'))
        volunteer = vc.edit_availability(volunteer=volunteer, availability='True')
        self.assertTrue(volunteer.availability)

    def test_edit_availability_invalid_input(self):
        with self.assertRaises(vc.ControllerError):
            volunteer = vc.create_volunteer(username='yunsy', password='root', firstname='Yunsy', lastname='Yin',
                                            phone='+447519953189', camp=Camp(name='UCL'))
            volunteer = vc.edit_availability(volunteer=volunteer, availability=False)
            self.assertFalse(volunteer.availability)


if __name__ == '__main__':
    unittest.main()
