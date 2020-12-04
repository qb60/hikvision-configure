import unittest

from Cryptodome.PublicKey import RSA

import cam_config


class TestCryptoUtils(unittest.TestCase):
    private_key_text = '''-----BEGIN RSA PRIVATE KEY-----
    MIICXAIBAAKBgQCSHixcONwzc7wXmPI79+JdmteTUW96HLADJY7YOcsw+t/HvFzB
    0RC17WxbTCD+eIpKaj5jnMpJnhUeqmijvP5+DAe1OMRjNwGmsjXZDOXs83+rM3ej
    C0+sdRLOTF2X1xpdOGAld1OBXqUJrbjb3DGY3RtJfgG2ExNZkHysVHmOtQIDAQAB
    AoGASN//o+c/+/FnCCXh+oLBRYoqpnDhNngEWS1sNu9sJfuZjJandIr+2J2Xg1lO
    w1v/LOocP7Y9NcZAJlE7ax6hlh7ow1SDIzsQhGTZ9i0j00V3rlrKS1oxWoD6zo+5
    cIbpapzMP8k823thO8SYQRdu/nYzimqOgAJUeJrfnsGJzoECQQC4WAkpWrlvJiTu
    zbA1DTXswcF/vW1FGkQQcmBuQ+pIu7dcxy0EuSsFDCFVFL5W0ry9pp8jb+PQ3+gy
    OHWQ3g+xAkEAyupJIXxOPM7uyoQAn+Dba3iJnTp/rJOTU3bQH/vh9z3x29tp2EYu
    /+oGA/3XoTiHxwgDg340j4QDHPHqyJ2URQJAc7joP2qxn+HNK5A5/oPFh1P2ma8b
    ila7xatXd8DwsSoOKJLsYtuu8uMzhYqZFj4Ct/eCTSevVu9If0ZMH14XcQJBAJLP
    H0oS3agxL6NmDe2eiiIfe7E9+dGqlBT3CW2al8qCDtK61MGdRbPyZZfNuIz0kYf2
    zFP+o5iSMo5mmS+8kuECQB+myw/w+l/fF8tUx5+cp3PX597GFIP+gX7pN3JAmyrz
    aIU6TCa1ciqpIauk7GHRMFcbjZjMDRIZ96WumlpnUrc=
    -----END RSA PRIVATE KEY-----'''

    def test_extract_random_key_from_xml(self):
        answer = '''<?xml version='1.0' encoding='UTF-8'?>
<Challenge version='2.0' xmlns='http://www.std-cgi.com/ver20/XMLSchema'>
<key>M2Y3MDU1NWZhMzg2ZjhkYzI4NDIxZjEzZWY1MTBjYzY4NDdmZTBlYjAzMDMyNzRmZGIzNWRlZmY2ZGQ1N2I3NzAyMDFmNDczMzk1NTY3MGUzZjMwZDJlMzE5MWE4NTkxMzA2YjdjNmNhYzJlYzdhYWQ5MDhjNmI5MThkYzNjMmVkMWQ4YjVlNzkyM2VjMDdlNzk1MGM0NWM3NjY5N2JmNmFlYjkwYjQ4YjQyOGFiMzg5MWI2MTNkNzUzZmU0ZGQyYjEyZThlMjhiMzJhM2VhMDI5NGVhYTA5NWVhZjVhMzRmZThlZTc1MDM2YWVmMjQwNjgzYzlkYzA2MzRkNzE0Nw==</key>
</Challenge>'''
        expected_text = 'M2Y3MDU1NWZhMzg2ZjhkYzI4NDIxZjEzZWY1MTBjYzY4NDdmZTBlYjAzMDMyNzRmZGIzNWRlZmY2ZGQ1N2I3NzAyMDFmNDczMzk1NTY3MGUzZjMwZDJlMzE5MWE4NTkxMzA2YjdjNmNhYzJlYzdhYWQ5MDhjNmI5MThkYzNjMmVkMWQ4YjVlNzkyM2VjMDdlNzk1MGM0NWM3NjY5N2JmNmFlYjkwYjQ4YjQyOGFiMzg5MWI2MTNkNzUzZmU0ZGQyYjEyZThlMjhiMzJhM2VhMDI5NGVhYTA5NWVhZjVhMzRmZThlZTc1MDM2YWVmMjQwNjgzYzlkYzA2MzRkNzE0Nw=='

        random_key_encrypted_text, answer_is_valid = cam_config.extract_random_key_encrypted(answer)

        self.assertEqual(expected_text, random_key_encrypted_text)
        self.assertTrue(answer_is_valid)

    def test_decrypt_random_key(self):
        random_key_encrypted_text = 'M2Y3MDU1NWZhMzg2ZjhkYzI4NDIxZjEzZWY1MTBjYzY4NDdmZTBlYjAzMDMyNzRmZGIzNWRlZmY2ZGQ1N2I3NzAyMDFmNDczMzk1NTY3MGUzZjMwZDJlMzE5MWE4NTkxMzA2YjdjNmNhYzJlYzdhYWQ5MDhjNmI5MThkYzNjMmVkMWQ4YjVlNzkyM2VjMDdlNzk1MGM0NWM3NjY5N2JmNmFlYjkwYjQ4YjQyOGFiMzg5MWI2MTNkNzUzZmU0ZGQyYjEyZThlMjhiMzJhM2VhMDI5NGVhYTA5NWVhZjVhMzRmZThlZTc1MDM2YWVmMjQwNjgzYzlkYzA2MzRkNzE0Nw=='
        expected_random_key = b'1ad021adbbecb495fa4794e12f0ac63c'

        private_key = RSA.importKey(self.private_key_text)
        actual_random_key = cam_config.decrypt_random_key(random_key_encrypted_text, private_key)

        self.assertEqual(expected_random_key, actual_random_key)

    def test_encrypt_password(self):
        new_password = 'qwer1234'
        random_key = b'c8059b41126bd480f684b6a46d48804c'

        expected_encrypted_password = b'NDk5M2NhMWZiNTdmNDViNzY1NDlkOTVkMTI4YjBkODhmY2U5M2QwZTcxMzdhYmJlZWM1YzU2ZmE3YTczNDQ1Nw=='

        actual_encrypted_password = cam_config.encrypt_password(random_key, new_password)

        self.assertEqual(expected_encrypted_password, actual_encrypted_password)


if __name__ == '__main__':
    unittest.main()
