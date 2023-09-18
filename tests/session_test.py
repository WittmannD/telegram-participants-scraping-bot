import unittest

from src.session.sqlite_custom_session import SQLiteCustomSession

session = SQLiteCustomSession('test')


class SessionTest(unittest.TestCase):
    def test_session_table(self):
        row = session._execute('select name from sqlite_master where type="table" and name=(?)', 'navigation_stack')
        self.assertIsNotNone(row, "Table should exists")
        self.assertEqual(len(row), 1, "Table should be one")

    def test_session_stack_methods(self):
        dummy_user_id = 12345
        dummy_stack = ['command1', 'command2', 'command3']
        session.set_navigation_stack(dummy_user_id, dummy_stack)
        stack = session.get_navigation_stack(dummy_user_id)

        self.assertEqual(dummy_stack, stack)

        stack2 = session.get_navigation_stack(54321)

        self.assertEqual(stack2, [])


if __name__ == '__main__':
    unittest.main()
