import unittest
import tkfinder


class MyTestCase(unittest.TestCase):
    def test_get_commands(self):

        result = tkfinder.get_commands_character("hwoarang")
        self.assertIn("1, 1, 3, 3", result)

    def test_get_close_moves(self):
        close_moves = tkfinder.get_similar_moves("d/f+1, 2", "hwoarang")
        self.assertIn("d/f+1, 3", close_moves)

if __name__ == '__main__':
    unittest.main()
