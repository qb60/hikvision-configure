import unittest
import re

# -12:00
# +13:00
from parameterized import parameterized

from cam_config import convert_gmt_offset_to_internal_timezone, timezone_has_right_format, make_dst_string, DstParam, dst_offset_has_right_format, dst_param_has_right_format


class TestTimeZoneConvert(unittest.TestCase):
    def test_simple(self):
        self.assertEqual('CST-5:00:00', convert_gmt_offset_to_internal_timezone('5:00:00'))

    def test_simple1(self):
        self.assertEqual('CST-5:30:00', convert_gmt_offset_to_internal_timezone('5:30:00'))

    def test_plus(self):
        self.assertEqual('CST-5:30:00', convert_gmt_offset_to_internal_timezone('+5:30:00'))

    def test_minus(self):
        self.assertEqual('CST+5:30:00', convert_gmt_offset_to_internal_timezone('-5:30:00'))

    def test_format1(self):
        self.assertTrue(True, timezone_has_right_format('-5:30:00'))

    def test_format2(self):
        self.assertTrue(True, timezone_has_right_format('+5:30:00'))

    def test_format3(self):
        self.assertTrue(True, timezone_has_right_format('5:30:00'))

    def test_format4(self):
        self.assertEqual(False, timezone_has_right_format('d5:30:00'))

    def test_format5(self):
        self.assertEqual(False, timezone_has_right_format('5:30'))


class TestTimeZoneDST(unittest.TestCase):
    def test_make_dst_string(self):
        expected_dst = 'DST01:30:00,M1.2.3/01:00:00,M4.5.6/14:00:00'

        dst_offset = "01:30"
        start_dst = DstParam(month=1, day=3, day_order_number=2, hour=1)
        end_dst = DstParam(month=4, day=6, day_order_number=5, hour=14)

        actual_dst = make_dst_string(dst_offset, start_dst, end_dst)
        self.assertEqual(expected_dst, actual_dst)

    @parameterized.expand([
        (DstParam(month=1, day=0, day_order_number=1, hour=0), True),
        (DstParam(month=12, day=6, day_order_number=5, hour=23), True),
        (DstParam(month=0, day=0, day_order_number=1, hour=0), False),
        (DstParam(month=13, day=0, day_order_number=1, hour=0), False),
        (DstParam(month=1, day=7, day_order_number=1, hour=0), False),
        (DstParam(month=1, day=0, day_order_number=6, hour=0), False),
        (DstParam(month=1, day=0, day_order_number=1, hour=24), False)
    ])
    def test_check_dst_param_valid(self, dst_param, is_valid):
        self.assertEqual(is_valid, dst_param_has_right_format(dst_param))

    @parameterized.expand([
        ("00:30", True),
        ("01:00", True),
        ("01:30", True),
        ("02:00", True),
        ("00:10", False),
        ("02:30", False),
        ("10:00", False),
        ("0a:00", False),
        ("02:01", False),
        ("01:40", False),
    ])
    def test_check_dst_offset_format(self, offset, is_valid):
        self.assertEqual(is_valid, dst_offset_has_right_format(offset))


if __name__ == '__main__':
    unittest.main()
