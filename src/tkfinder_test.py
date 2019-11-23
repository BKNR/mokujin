import unittest
from src import tkfinder


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
        self.assertEqual(None, result)

    def test_get_cha_move(self):
        character = {
            "name": "kazuya",
            "proper_name": "Kazuya",
            "local_json": "kazuya.json",
            "online_webpage": "http://rbnorway.org/kazuya-t7-frames",
            "portrait": "https://i.imgur.com/kMvhDfU.jpg"
        }

        self.assertEqual("1, 1, 2", tkfinder.get_move(character, "1 ,1 ,2", False)["Command"])
        self.assertEqual("f, n, d, d/f+4, 1", tkfinder.get_move(character, "hs", False)["Command"])
        self.assertEqual("f, n, d/f+2", tkfinder.get_move(character, "ewgf", False)["Command"])

    def test_none(self):
        entry = {"Gif": ""}
        entry2 = {"Gif": None}
        entry3 = {"Gif": " "}
        self.assertTrue(not entry["Gif"])
        self.assertTrue(not entry2["Gif"])
        self.assertFalse(not entry3["Gif"])


if __name__ == '__main__':
    unittest.main()
