import unittest
from parameterized import parameterized
from cam_config import check_users_info, UserPermissions, user_level_for_permission


class TestCheckUsers(unittest.TestCase):
    @parameterized.expand([
        [[]],
        [[['user', 'password', 'n']]],
        [[['user', 'password', 'v']]],
        [[['user', 'password', 'r']]],
        [[['user', 'password', 'a']]],
    ])
    def test_dont_raise_on_proper_user_info(self, users):
        check_users_info(users)

    @parameterized.expand([
        [[['admin']]],
        [[['admin', 'password']]],
        [[['user', 'password', 'd']]],
        [[['user', 'password', '']]],
        [[['', 'password', 'a']]],
        [[['user', '', 'a']]],
        [[['user', 'pass', 'a']]],
    ])
    def test_raise_on_wrong_user_info(self, users):
        with self.assertRaises(RuntimeError) as error:
            check_users_info(users)

        print(error.exception)


class TestUserLevel(unittest.TestCase):
    def test_viewer_user_level(self):
        self.assertEqual('Operator', user_level_for_permission(UserPermissions.All))
        self.assertEqual('Viewer', user_level_for_permission(UserPermissions.Nothing))
        self.assertEqual('Viewer', user_level_for_permission(UserPermissions.Video))
        self.assertEqual('Viewer', user_level_for_permission(UserPermissions.Records))


if __name__ == '__main__':
    unittest.main()
