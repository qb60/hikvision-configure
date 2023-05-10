import unittest

from cam_config import Enum


class UserPermissions(Enum):
    Nothing = 'n'
    Video = 'v'
    Records = 'r'
    All = 'a'


class TestEnum(unittest.TestCase):
    def test_enum_items(self):
        expected = {'Nothing': 'n', 'Video': 'v', 'Records': 'r', 'All': 'a'}
        items = UserPermissions.items()

        self.assertEqual(items, expected)

    def test_enum_values(self):
        expected = ['n', 'v', 'r', 'a']
        values = UserPermissions.values()

        self.assertEqual(values, expected)
        self.assertTrue('n' in values)


if __name__ == '__main__':
    unittest.main()
