import unittest

from mojang import Client

from config import (
    BEARER_TOKEN,
    NOTCH_USERNAME,
    AVAILABLE_USERNAME,
    NOTCH_SKIN_URL,
)


class TestClient(unittest.TestCase):
    """Tests all of the functions in the Client API"""

    def setUp(self):
        self.client = Client(bearer_token=BEARER_TOKEN)

    def test_is_username_available(self):
        available = self.client.is_username_available(NOTCH_USERNAME)
        self.assertFalse(available)

        available = self.client.is_username_available(AVAILABLE_USERNAME)
        self.assertTrue(available)

    def get_billing_info(self):
        data = self.client.get_billing_info()
        expected_keys = ["id", "userId", "billingAddress", "createdAt"]

        keys = data.keys()

        for expected_key in expected_keys:
            self.assertIn(expected_key, keys)

    def test_is_username_blocked(self):
        blocked = self.client.is_username_blocked(NOTCH_USERNAME)
        self.assertFalse(blocked)

    def test_change_username(self):
        success = self.client.change_username(NOTCH_USERNAME)["success"]
        self.assertFalse(success)
        data = self.client.change_username(NOTCH_USERNAME)
        self.assertIn("error", data.keys())

    def test_get_profile(self):
        self.client.get_profile()

    def test_change_skin(self):
        self.client.change_skin(url=NOTCH_SKIN_URL)

    def test_copy_skin(self):
        self.client.copy_skin(NOTCH_USERNAME)

    def test_change_skin_variant(self):
        self.client.change_skin_variant("classic")
        self.client.change_skin_variant("slim")

    def test_reset_skin(self):
        self.client.reset_skin()

    def test_disable_cape(self):
        self.client.disable_cape()


if __name__ == "__main__":
    # https://github.com/psf/requests/issues/3912
    unittest.main(warnings="ignore")
