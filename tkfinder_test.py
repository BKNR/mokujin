import unittest
import tkfinder


class MyTestCase(unittest.TestCase):
    def test_get_commands(self):
        result = tkfinder.get_commands_from("hwoarang")
        self.assertIn("1, 1, 3, 3", result)

    def test_get_close_moves(self):
        close_moves = tkfinder.get_similar_moves("d/f+1, 2", "hwoarang")
        self.assertIn("d/f+1, 3", close_moves)

    def test_is_command_in_alias(self):
        item = {'Alias': "hs, hellsweep, Giant swing, u/f3"}
        result = tkfinder.is_command_in_alias("hellsweep", item)
        self.assertTrue(result)

        result = tkfinder.is_command_in_alias("he", item)
        self.assertFalse(result)

        result = tkfinder.is_command_in_alias("uf3", item)
        self.assertTrue(result)

    def test_get_cha_name(self):
        result = tkfinder.correct_character_name("hwoarang")
        self.assertEqual("hwoarang", result)

        result = tkfinder.correct_character_name("hwo")
        self.assertEqual("hwoarang", result)

        result = tkfinder.correct_character_name("kazu")
        self.assertEqual("kazu", result)


if __name__ == '__main__':
    unittest.main()
