import unittest

from src.commands.base import BaseCommand


class BaseCommandTest(unittest.TestCase):
    def test_base_command_class(self):
        def should_raises():
            class TestCommand(BaseCommand):
                keyboard_markup = None
                command_pattern = None

                @staticmethod
                def handler():
                    pass

            command = TestCommand()

        self.assertRaises((NotImplementedError, TypeError), should_raises)



if __name__ == '__main__':
    unittest.main()
