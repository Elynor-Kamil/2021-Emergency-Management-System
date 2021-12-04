from unittest import TestCase

from models.user import User, require_role


class UserTest(TestCase):

    def setUp(self) -> None:
        User.delete_all()

    def test_create_user(self):
        user = User(username='test_username', password='test_password')
        self.assertEqual(user.username, 'test_username')

    def test_login_success(self):
        user = User(username='test_username', password='test_password')
        self.assertEqual(user.login('test_password').username, 'test_username')

    def test_login_fail(self):
        user = User(username='test_username', password='test_password')
        with self.assertRaises(User.InvalidPassword):
            user.login('invalid_password')

    def test_update_password(self):
        user = User(username='test_username', password='test_password')
        user.update_password('new_password')
        self.assertEqual(user.login('new_password').username, 'test_username')
        with self.assertRaises(User.InvalidPassword):
            user.login('test_password')

    class MockSession:
        def __init__(self, user):
            self.user = user

    class MockRoleA:
        pass

    class MockRoleB:
        pass

    def test_require_role(self):
        @require_role(self.MockRoleA)
        def test_admin(session):
            return True

        session = self.MockSession(self.MockRoleA())
        self.assertTrue(test_admin(session))
        session.user = self.MockRoleB()
        self.assertIsNone(test_admin(session))

    def tearDown(self) -> None:
        User.delete_all()
