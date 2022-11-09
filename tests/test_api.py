import unittest

from mojang import API, MojangError


from config import (
    NOTCH_USERNAME,
    NOTCH_UUID,
    INVALID_UUID,
    INVALID_USERNAME,
)


class TestAPI(unittest.TestCase):
    """Tests all of the functions in the Public API"""

    def setUp(self):
        self.api = API()

    def test_get_uuid(self):
        uuid = self.api.get_uuid(INVALID_USERNAME)
        self.assertEqual(uuid, None)

        uuid = self.api.get_uuid(NOTCH_USERNAME)
        self.assertEqual(uuid, NOTCH_UUID)

    def test_get_uuids(self):
        usernames = [NOTCH_USERNAME, "Herobrine", "Test", "Minecraft"]
        profiles = self.api.get_uuids(usernames)
        self.assertEqual(len(profiles), len(usernames))
        self.assertEqual(profiles[NOTCH_USERNAME], NOTCH_UUID)

        # The username passed should be invalid rather than not taken
        # Invalid usernames cause a Mojang server error
        self.assertRaises(MojangError, self.api.get_uuids, [INVALID_USERNAME])
        self.assertRaises(TypeError, self.api.get_uuids, "A random string")

    def test_get_username(self):
        username = self.api.get_username(NOTCH_UUID)
        self.assertEqual(username, NOTCH_USERNAME)

        username = self.api.get_username(INVALID_UUID)
        self.assertEqual(username, None)

    def test_get_profile(self):
        profile = self.api.get_profile(NOTCH_UUID)
        self.assertEqual(profile.id, NOTCH_UUID)
        self.assertEqual(profile.name, NOTCH_USERNAME)
        self.assertIsInstance(profile.timestamp, int)
        self.assertEqual(profile, profile)
        profile = self.api.get_profile(INVALID_UUID)
        self.assertEqual(profile, None)

    def test_get_blocked_servers(self):
        servers = self.api.get_blocked_servers()
        # Assumes that there is always at least 1 blocked server by Mojang.
        self.assertGreater(len(servers), 0)


if __name__ == "__main__":
    # https://github.com/psf/requests/issues/3912
    unittest.main(warnings="ignore")
