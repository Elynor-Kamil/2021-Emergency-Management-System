import unittest
import controller.volunteer_controller as vc
from models.volunteer import Volunteer
from models.camp import Camp


class TestVolunteerController(unittest.TestCase):

    def test_create_volunteer(self):
        volunteer_called = vc.create_volunteer(username='yunsy', password='root', firstname='Yunsy', lastname='Yin',
                                               phone='+447519953189', camp=Camp(name='UCL'))
        self.assertEqual(type(volunteer_called), Volunteer)

    def test_create_volunteer_invalid_username(self):
        with self.assertRaises(vc.ControllerError):
            vc.create_volunteer(username='yun', password='root', firstname='Yunsy', lastname='Yin',
                                phone='+447519953189', camp=Camp(name='UCL'))

    def test_create_volunteer_invalid_password(self):
        with self.assertRaises(vc.ControllerError):
            vc.create_volunteer(username='yunsy', password='roo', firstname='Yunsy', lastname='Yin',
                                phone='+447519953189', camp=Camp(name='UCL'))

    def test_create_volunteer_invalid_firstname(self):
        with self.assertRaises(vc.ControllerError):
            vc.create_volunteer(username='yunsy', password='roo', firstname='Y', lastname='Yin',
                                phone='+447519953189', camp=Camp(name='UCL'))

    def test_create_volunteer_invalid_lastname(self):
        with self.assertRaises(vc.ControllerError):
            vc.create_volunteer(username='yunsy', password='roo', firstname='Yunsy', lastname='Y',
                                phone='+447519953189', camp=Camp(name='UCL'))

    def test_create_volunteer_invalid_phone_without_international_code(self):
        with self.assertRaises(vc.ControllerError):
            vc.create_volunteer(username='yunsy', password='roo', firstname='Yunsy', lastname='Yin',
                                phone='07519953189', camp=Camp(name='UCL'))

    def test_create_volunteer_invalid_phone_too_short(self):
        with self.assertRaises(vc.ControllerError):
            vc.create_volunteer(username='yunsy', password='roo', firstname='Yunsy', lastname='Yin',
                                phone='+44751', camp=Camp(name='UCL'))

    def test_find_volunteer(self):
        vc.create_volunteer(username='yunsy', password='root', firstname='Yunsy', lastname='Yin', phone='+447519953189',
                            camp=Camp(name='UCL'))
        volunteer_called = vc.find_volunteer('yunsy')
        self.assertEqual(type(volunteer_called), Volunteer)

    def test_find_volunteer_invalid_input(self):
        with self.assertRaises(vc.ControllerError):
            vc.find_volunteer('Yunsy')

    def test_view_volunteer_profile(self):
        volunteer_called = vc.create_volunteer(username='yunsy', password='root', firstname='Yunsy', lastname='Yin',
                                               phone='+447519953189',
                                               camp=Camp(name='UCL'))
        volunteer_called_profile = vc.view_volunteer_profile(volunteer_called)
        self.assertEqual(type(volunteer_called_profile), str)

    def test_deactivate_volunteer(self):
        volunteer_called = vc.create_volunteer(username='yunsy', password='root', firstname='Yunsy', lastname='Yin',
                                               phone='+447519953189',
                                               camp=Camp(name='UCL'))
        volunteer_deactivated = vc.deactivate_volunteer(volunteer_called)
        self.assertFalse(volunteer_deactivated.account_activated)

    def test_reactivate_volunteer(self):
        volunteer_called = vc.create_volunteer(username='yunsy', password='root', firstname='Yunsy', lastname='Yin',
                                               phone='+447519953189',
                                               camp=Camp(name='UCL'))
        volunteer_reactivated = vc.reactivate_volunteer(volunteer_called)
        self.assertTrue(volunteer_reactivated.account_activated)

    def test_delete_volunteer(self):
        volunteer_called = vc.create_volunteer(username='yunsy', password='root', firstname='Yunsy', lastname='Yin',
                                               phone='+447519953189',
                                               camp=Camp(name='UCL'))
        self.assertIsNone(vc.delete_volunteer(volunteer_called))


if __name__ == '__main__':
    unittest.main()
