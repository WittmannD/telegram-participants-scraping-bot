import unittest


class ConfigTest(unittest.TestCase):
    def check_required_variables(self):
        try:
            from src.common.config import current_config
        except RuntimeError as err:
            self.fail(str(err))

        self.assertIsNotNone(current_config.TELEGRAM_API_ID, "Should be defined")
        self.assertIsNotNone(current_config.TELEGRAM_API_HASH, "Should be defined")
        self.assertIsNotNone(current_config.TELEGRAM_BOT_TOKEN, "Should be defined")


if __name__ == '__main__':
    unittest.main()
