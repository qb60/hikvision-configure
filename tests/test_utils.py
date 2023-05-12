import unittest

from cam_config import parse_command_line_arguments

DUMMY_IP = '10.10.10.10'
DUMMY_APP_NAME = 'APP_NAME'


class TestCommandLine(unittest.TestCase):
    def test_current_ip(self):
        current_ip = '10.10.10.10'
        args = [DUMMY_APP_NAME, current_ip]

        options = parse_command_line_arguments(args)
        self.assertEqual(current_ip, options.current_ip)

    def test_new_ip_default_mask(self):
        new_ip = '10.10.10.11'
        args = [DUMMY_APP_NAME, DUMMY_IP, new_ip]

        options = parse_command_line_arguments(args)

        self.assertEqual(new_ip, str(options.new_ip.ip))
        self.assertEqual('255.255.255.0', str(options.new_ip.netmask))

    def test_new_ip_custom_mask(self):
        new_ip = '10.10.10.11'
        args = [DUMMY_APP_NAME, DUMMY_IP, new_ip + '/27']

        options = parse_command_line_arguments(args)

        self.assertEqual(new_ip, str(options.new_ip.ip))
        self.assertEqual('255.255.255.224', str(options.new_ip.netmask))

    def test_no_new_ip(self):
        args = [DUMMY_APP_NAME, DUMMY_IP]

        options = parse_command_line_arguments(args)

        self.assertEqual(None, options.new_ip)

    def test_dhcp_lowercase(self):
        args = [DUMMY_APP_NAME, DUMMY_IP, 'dhcp']

        options = parse_command_line_arguments(args)

        self.assertEqual('dhcp', options.new_ip)

    def test_dhcp_uppercase(self):
        args = [DUMMY_APP_NAME, DUMMY_IP, 'DHCP']

        options = parse_command_line_arguments(args)

        self.assertEqual('dhcp', options.new_ip)


if __name__ == '__main__':
    unittest.main()
