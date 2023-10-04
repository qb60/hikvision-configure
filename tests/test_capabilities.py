import unittest
from parameterized import parameterized
from cam_config import check_users_info, UserPermissions, user_level_for_permission, WDRCapabilities


class TestWDRCapabilities(unittest.TestCase):
    wdr_modes = ['open', 'close']
    wdr_level_range = (10, 20)

    @parameterized.expand([
        ('open', 15, True),
        ('close', 15, True),
        ('open', 10, True),
        ('open', 20, True),

        ('oops', 15, False),
        ('open', 9, False),
        ('open', 21, False),
    ])
    def test_mode_supported(self, mode, level, valid):
        capabilities = WDRCapabilities(self.wdr_modes, self.wdr_level_range)

        self.assertEqual(valid, capabilities.is_mode_supported(mode, level))
