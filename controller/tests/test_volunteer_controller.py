import unittest
import controller.volunteer_controller as vc
from models.camp import Camp
from models.plan import Plan


class TestVolunteerController(unittest.TestCase):

    def test_edit_firstname(self):
        volunteer_called = vc.create_volunteer(username='yunsy', password='root', firstname='Yunsy', lastname='Yin',
                                               phone='+447519953189', camp=Camp(name='UCL'))
        volunteer_edited = vc.edit_firstname(volunteer=volunteer_called, firstname='Yun-Tzu')
        self.assertEqual(volunteer_edited.firstname, 'Yun-Tzu')

    def test_edit_firstname_invalid_input(self):
        with self.assertRaises(vc.ControllerError):
            volunteer_called = vc.create_volunteer(username='yunsy', password='root', firstname='Yunsy', lastname='Yin',
                                                   phone='+447519953189', camp=Camp(name='UCL'))
            vc.edit_firstname(volunteer=volunteer_called, firstname='Y')

    def test_edit_lastname(self):
        volunteer_called = vc.create_volunteer(username='yunsy', password='root', firstname='Yunsy', lastname='Yin',
                                               phone='+447519953189', camp=Camp(name='UCL'))
        volunteer_edited = vc.edit_lastname(volunteer=volunteer_called, lastname='Yinnn')
        self.assertEqual(volunteer_edited.lastname, 'Yinnn')

    def test_edit_lastname_invalid_input(self):
        with self.assertRaises(vc.ControllerError):
            volunteer_called = vc.create_volunteer(username='yunsy', password='root', firstname='Yunsy', lastname='Yin',
                                                   phone='+447519953189', camp=Camp(name='UCL'))
            vc.edit_lastname(volunteer=volunteer_called, lastname='Y')

    def test_edit_phone(self):
        volunteer_called = vc.create_volunteer(username='yunsy', password='root', firstname='Yunsy', lastname='Yin',
                                               phone='+447519953189', camp=Camp(name='UCL'))
        volunteer_edited = vc.edit_phone(volunteer=volunteer_called, phone='+441111111111')
        self.assertEqual(volunteer_edited.phone, '+441111111111')

    def test_edit_phone_without_international_code(self):
        with self.assertRaises(vc.ControllerError):
            volunteer_called = vc.create_volunteer(username='yunsy', password='root', firstname='Yunsy', lastname='Yin',
                                                   phone='+447519953189', camp=Camp(name='UCL'))
            vc.edit_phone(volunteer=volunteer_called, phone='441111111111')

    def test_edit_phone_too_short(self):
        with self.assertRaises(vc.ControllerError):
            volunteer_called = vc.create_volunteer(username='yunsy', password='root', firstname='Yunsy', lastname='Yin',
                                                   phone='+447519953189', camp=Camp(name='UCL'))
            vc.edit_phone(volunteer=volunteer_called, phone='+44123')

    def test_edit_camp_by_admin(self):
        volunteer_called = vc.create_volunteer(username='yunsy', password='root', firstname='Yunsy', lastname='Yin',
                                               phone='+447519953189', camp=Camp(name='UCL'))
        volunteer_edited = vc.edit_camp(volunteer=volunteer_called, camp=Camp(name='Euston'), is_admin=True)
        self.assertEqual(str(volunteer_edited.camp), 'Euston')

    def test_edit_camp_under_same_plan_by_volunteer(self):
        camp_1 = Camp(name='Camp 1')
        camp_2 = Camp(name='Camp 2')
        Plan(name='Plan A',
             emergency_type=Plan.EmergencyType.EARTHQUAKE,
             description='Test',
             geographical_area='',
             camps=[camp_1, camp_2])
        volunteer_called = vc.create_volunteer(username='yunsy', password='root', firstname='Yunsy', lastname='Yin',
                                               phone='+447519953189', camp=camp_1)
        volunteer_edited = vc.edit_camp(volunteer=volunteer_called, camp=camp_2, is_admin=False)
        self.assertEqual(str(volunteer_edited.camp), 'Camp 2')

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
            volunteer_called = vc.create_volunteer(username='yunsy', password='root', firstname='Yunsy', lastname='Yin',
                                                   phone='+447519953189', camp=camp_1)
            vc.edit_camp(volunteer=volunteer_called, camp=camp_2, is_admin=False)

    def test_edit_availability_false(self):
        volunteer_called = vc.create_volunteer(username='yunsy', password='root', firstname='Yunsy', lastname='Yin',
                                               phone='+447519953189', camp=Camp(name='UCL'))
        volunteer_edited = vc.edit_availability(volunteer=volunteer_called, availability='False')
        self.assertFalse(volunteer_edited.availability)

    def test_edit_availability_True(self):
        volunteer_called = vc.create_volunteer(username='yunsy', password='root', firstname='Yunsy', lastname='Yin',
                                               phone='+447519953189', camp=Camp(name='UCL'))
        volunteer_edited = vc.edit_availability(volunteer=volunteer_called, availability='True')
        self.assertTrue(volunteer_edited.availability)

    def test_edit_availability_invalid_input(self):
        with self.assertRaises(vc.ControllerError):
            volunteer_called = vc.create_volunteer(username='yunsy', password='root', firstname='Yunsy', lastname='Yin',
                                                   phone='+447519953189', camp=Camp(name='UCL'))
            volunteer_edited = vc.edit_availability(volunteer=volunteer_called, availability=False)
            self.assertFalse(volunteer_edited.availability)


if __name__ == '__main__':
    unittest.main()
