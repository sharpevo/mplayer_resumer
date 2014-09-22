#-*-coding:utf-8-*-
import unittest
import os
from mplayer_resumer import History

class MainTest(unittest.TestCase):
    def setUp(self):
        self.history = History(path="test/mplayer_history.json")
        self.init_db = self.history.db

    def test_get_history_by_id(self):
        self.assertEqual(
            self.history.get_history_by_id("/home/ryan/downloads/test.f4v"),
            "15.4")
        self.assertEqual(
            self.history.get_history_by_id("blahblah.avi"),
            "0")
        uni_str = unicode("/media/ftp/海阔天空专区/霍比特人1_The.Hobbit.An.Unexpected.Journey.2012.720p.BluRay.x264-SPARKS/the.hobbit.an.unexpected.journey.2012\.720p.bluray.x264-sparks.mkv", "utf-8")
        self.assertEqual(
            self.history.get_history_by_id(uni_str),
            "2582.7")

    def test_save(self):
        self.assertEqual(self.history.get_history_by_id("another.avi"), "0")
        self.history.save("another.avi", "22.2")
        self.assertEqual(self.history.get_history_by_id("another.avi"), "22.2")

    def test_remove(self):
        self.history.remove("test")  # remove movies new
        self.assertEqual(self.history.get_history_by_id("/home/ryan/downloads/test.f4v"), "15.4")
        self.history.remove("/home/ryan/downloads/test.f4v")
        self.assertEqual(self.history.get_history_by_id("/home/ryan/downloads/test.f4v"), "0")

    #def test_commit(self):
        #old_db = self.history.db
        #self.history.commit()
        #self.history.connect_db()
        #self.assertEqual(self.history.db, old_db)
        #self.assertNotEqual(self.history.db, self.init_db)

if __name__ == "__main__":
    unittest.main()
