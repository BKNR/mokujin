import unittest, json
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
        self.assertEqual("f, f, f+3 or WR+3", tkfinder.get_move(character, "wr3")["Command"])
        self.assertEqual("1, 1, 2", tkfinder.get_move(character, "112")["Command"])
        self.assertEqual("f, n, d, d/f+4, 1", tkfinder.get_move(character, "hs")["Command"])
        self.assertEqual("f, n, d, d/f+4, 1", tkfinder.get_move(character, "cd41")["Command"])
        self.assertEqual("f, n, d/f+2", tkfinder.get_move(character, "ewgf")["Command"])
        self.assertEqual("WS+1, 2", tkfinder.get_move(character, "ws12")["Command"])
        self.assertEqual("b+2,1", tkfinder.get_move(character, "b21")["Command"])
        marduk = {
            "name": "marduk",
            "proper_name": "Marduk",
            "local_json": "marduk.json",
            "online_webpage": "http://rbnorway.org/marduk-t7-frames",
            "portrait": "https://i.imgur.com/2OtX6nd.png"
        }
        self.assertEqual("d/f+3, d/f+1, 2", tkfinder.get_move(marduk, "df3df12")["Command"])
        self.assertEqual("d/f+3, 1, d+2", tkfinder.get_move(marduk, "df31,d+2")["Command"])
        self.assertEqual("d/f+3, 1, d+2", tkfinder.get_move(marduk, "df3,1d+2")["Command"])
        self.assertEqual("d/f+3, 1, d+2", tkfinder.get_move(marduk, "df+3,1d2")["Command"])

        leo = {
            "name": "leo",
            "proper_name": "Leo",
            "local_json": "leo.json",
            "online_webpage": "http://rbnorway.org/leo-t7-frames",
            "portrait": "https://i.imgur.com/i1CO8SB.jpg"
        }
        self.assertEqual("WS+4, 1+2", tkfinder.get_move(leo, "ws41+2")["Command"])
        self.assertEqual("b+1, 4", tkfinder.get_move(leo, "b14")["Command"])
        self.assertEqual("KNK 3, 4", tkfinder.get_move(leo, "knk 34")["Command"])
        self.assertEqual("KNK 1+2", tkfinder.get_move(leo, "knk 1+2")["Command"])

        kazumi = {
            "name": "kazumi",
            "proper_name": "Kazumi",
            "local_json": "kazumi.json",
            "online_webpage": "http://rbnorway.org/kazumi-t7-frames",
            "portrait": "https://i.imgur.com/ZNiaFwL.jpg"
        }
        self.assertEqual("b, f+2, 1, 1+2", tkfinder.get_move(kazumi, "bf211+2")["Command"])
        self.assertEqual("u/f+4", tkfinder.get_move(kazumi, "uf4")["Command"])

    def test_move_simplifier(self):
        move = "df+3, df+1, 1+2"
        self.assertEqual("df3df11+2", tkfinder.move_simplifier(move))

    def test_none(self):
        entry1 = json.loads("[{\"Gif\": \"\"}]")
        entry2 = json.loads("[{\"Gif\": \"something\"}]")
        entry3 = json.loads("[{\"Gif\": null}]")
        entry4 = json.loads("[{\"Test\": \"test\"}]")

        self.assertTrue(not entry1[0]["Gif"])
        self.assertTrue(entry2[0]["Gif"])
        self.assertTrue(not entry3[0]["Gif"])
        self.assertTrue(not 'Gif' in entry4)

        self.assertTrue("ws12" == "ws12")


if __name__ == '__main__':
    unittest.main()
