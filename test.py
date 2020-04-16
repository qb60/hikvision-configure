
import unittest
import re

# -12:00
# +13:00


def timezone_has_right_format(gmt_offset):
    format_matched = re.match('[+,-]?\d{1,2}:\d{2}:\d{2}', gmt_offset)
    return format_matched is not None


def convert_gmt_offset_to_internal_timezone(gmt_offset):
    prefix = 'CST'

    sign = gmt_offset[0]
    if sign == '-':
        suffix = '+' + gmt_offset[1:]
    elif sign == '+':
        suffix = '-' + gmt_offset[1:]
    else:
        suffix = '-' + gmt_offset

    return prefix + suffix


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
        self.assertEqual(True, timezone_has_right_format('-5:30:00'))

    def test_format2(self):
        self.assertEqual(True, timezone_has_right_format('+5:30:00'))

    def test_format3(self):
        self.assertEqual(True, timezone_has_right_format('5:30:00'))

    def test_format4(self):
        self.assertEqual(False, timezone_has_right_format('d5:30:00'))

    def test_format5(self):
        self.assertEqual(False, timezone_has_right_format('5:30'))

if __name__ == '__main__':
    unittest.main()