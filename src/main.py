#!/usr/bin/python2
import sys
import os.path
import pickle
import re
import subprocess

class Resumer():
    def __init__(self, file_to_play, options=[]):
        self.db_file = self.get_db_file()
        self.db_object = self.get_db_object()
        self.file_to_play = file_to_play
        self.amendment = -5 #-5 # time to roll back
        self.options = options

    def get_db_file(self):
        return os.path.join(os.path.expanduser("~"), ".mplayer_resume")

    def get_db_object(self):
        if not os.path.exists(self.db_file):
            return dict()
        else:
            with open(self.db_file, "rb") as f:
                db_object = pickle.load(f)
            return db_object

    def get_break_time(self):
        break_time = self.get_db_object().get(self.file_to_play, 0)
        return self.amend_break_time(break_time)

    def amend_break_time(self, break_time):
        amend_time = float(break_time) + self.amendment
        if amend_time < 0:
           amend_time = break_time
        return amend_time

    def parse_break_time(self, output):
        return output.rpartition("A:")[2].split("V:")[0].strip()

    def parse_stop_status(self, output):
        if re.search(r"Exiting.*\((.*)\)", output).group(1) == "End of file":
            return False
        return True

    def play_file(self):
        cmd = ["mplayer", "-ss", str(self.get_break_time()), self.file_to_play] + self.options
        output = subprocess.check_output(cmd)
        self.save_status(output)

    def save_status(self, output):
        if self.parse_stop_status(output):
            self.db_object.update({self.file_to_play: self.parse_break_time(output)})
        else:
            self.db_object.pop(self.file_to_play)

        with open(self.db_file, "wb") as f:
            pickle.dump(self.db_object, f, pickle.HIGHEST_PROTOCOL)

if __name__ == "__main__":

    resumer = Resumer(sys.argv[1], options=sys.argv[2:])
    resumer.play_file()


