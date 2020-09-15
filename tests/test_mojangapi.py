import unittest

from mojang import MojangAPI


class TestMojangAPI(unittest.TestCase):
    """Tests all of the functions in MojangAPI

    Currently does not unit test:
    - refresh_access_token
    """

    # Notch is used as a base player
    # Assumes Notch's UUID and username will never change
    NOTCH_UUID = "069a79f444e94726a5befca90e38aaf5"
    NOTCH_USERNAME = "Notch"

    INVALID_USERNAME = "username_that_does_not_exist"
    INVALID_UUID = "uuid_that_does_not_exist"

    def test_get_uuid(self):
        uuid = MojangAPI.get_uuid(self.INVALID_USERNAME)
        self.assertEqual(uuid, None)
        
        uuid = MojangAPI.get_uuid(self.NOTCH_USERNAME)
        self.assertEqual(uuid, self.NOTCH_UUID)
        
    def test_get_uuids(self):
        usernames = [self.NOTCH_USERNAME, "Herobrine", "Test", "Minecraft"]
        profiles = MojangAPI.get_uuids(usernames)
        self.assertEqual(len(profiles), len(usernames))
        self.assertEqual(profiles[self.NOTCH_USERNAME], self.NOTCH_UUID)

        # The username passed should be invalid rather than not taken
        # Invalid usernames cause a Mojang server error
        self.assertRaises(ValueError, MojangAPI.get_uuids, [self.INVALID_USERNAME])

    def test_get_username(self):
        username = MojangAPI.get_username(self.NOTCH_UUID)
        self.assertEqual(username, self.NOTCH_USERNAME)
    
        username = MojangAPI.get_username(self.INVALID_UUID)
        self.assertEqual(username, None)
    
    def test_get_drop_timestamp(self):
        self.assertRaises(ValueError, MojangAPI.get_drop_timestamp, self.INVALID_USERNAME)
        self.assertEqual(None, MojangAPI.get_drop_timestamp(self.NOTCH_USERNAME))

    def test_get_profile(self):
        profile = MojangAPI.get_profile(self.NOTCH_UUID)
        self.assertEqual(profile.id, self.NOTCH_UUID)
        self.assertEqual(profile.name, self.NOTCH_USERNAME)
        self.assertIsInstance(profile.timestamp, int)
        profile = MojangAPI.get_profile(self.INVALID_UUID)
        self.assertEqual(profile, None)

    def test_get_api_status(self):
        statuses = MojangAPI.get_api_status()
        self.assertEqual(bool(statuses.get("minecraft.net")), True)

    def test_get_name_history(self):
        names = MojangAPI.get_name_history(self.NOTCH_UUID)[0]
        self.assertEqual(names["changed_to_at"], 0)

    def test_get_blocked_servers(self):
        servers = MojangAPI.get_blocked_servers()
        # Assumes that there are always at least 100 blocked servers by Mojang.
        self.assertGreater(len(servers), 100)

    def test_get_sale_statistics(self):
        kwargs = dict(item_sold_minecraft=True,
                      prepaid_card_redeemed_minecraft=True,
                      item_sold_cobalt=False,
                      item_sold_scrolls=False,
                      prepaid_card_redeemed_cobalt=False,
                      item_sold_dungeons=False
                      )

        metrics = MojangAPI.get_sale_statistics(**kwargs)
        self.assertIsNotNone(metrics.get("total"))
        self.assertIsNotNone(metrics.get("last24h"))
        self.assertIsNotNone(metrics.get("sale_velocity_per_seconds"))
        

if __name__ == "__main__":
    unittest.main()
