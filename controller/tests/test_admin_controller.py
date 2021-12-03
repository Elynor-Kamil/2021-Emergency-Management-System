import unittest

from controller.admin_controller import view_admin_profile
from models.admin import Admin


class AdminControllerTest(unittest.TestCase):

    def setUp(self) -> None:
        Admin.delete_all()

    def test_profile(self):
        user = Admin('test_user', 'test_password')
        self.assertEqual(str(user), view_admin_profile(user))

    def tearDown(self) -> None:
        Admin.delete_all()


if __name__ == '__main__':
    unittest.main()
