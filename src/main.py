#!/usr/bin/python2
import sys
import os.path
import json
import re
import subprocess


class Player:
    def __init__(self, file_to_play="", options=[]):

        self.options = options
        self.time_to_rollback = -5
        self.history = History()
        self.gen_candidate()
        self.file_to_play = file_to_play

        if file_to_play:
            match = re.search(r"^[0-9]+$", file_to_play)
            if match:
                index = int(file_to_play)
                try:
                    self.file_to_play = self.candidate_list[index]
                except IndexError:
                    print "Index out of range..."
                    self.file_to_play = ""
            else:
                self.file_to_play = self.get_file_abspath(file_to_play)

    def get_file_abspath(self, file_path):
        return unicode(os.path.abspath(file_path),"utf-8")

    def get_break_time(self):
        break_time = self.history.get_history_by_id(self.file_to_play)
        return self.amend_break_time(break_time)

    def amend_break_time(self, break_time):
        break_time = float(break_time)
        amend_time = break_time + self.time_to_rollback
        if amend_time < 0:
            amend_time = break_time
        return str(amend_time)

    def parse_break_time(self, output):
        return output.rpartition("A:")[2].split("V:")[0].strip()

    def parse_stop_status(self, output):
        if re.search(r"Exiting.*\((.*)\)", output).group(1) == "End of file":
            return False
        return True

    def print_list(self):
        for i,c in enumerate(self.candidate_list):
            print i, c.rpartition("/")[2]

    def gen_candidate(self):
        self.candidate_list = []
        for key in self.history.get_history_list():
            self.candidate_list.append(key)

    def play(self):
        if self.file_to_play:
            cmd = ["mplayer",
                "-fs",
                "-ss",
                self.get_break_time(),
                self.file_to_play] + self.options
            output = subprocess.check_output(cmd)
            self.register(output)
        else:
            self.print_list()

    def register(self, output):
        if self.parse_stop_status(output):
            self.history.save(self.file_to_play, self.parse_break_time(output))
        else:
            self.history.remove(self.file_to_play)

        self.history.commit()


class History:
    def __init__(self, path="$HOME/.cache/mplayer_history.json"):
        self.db_path = self.expand_db_path(path)
        self.db = self.connect_db()

    def expand_db_path(self, path):
        return os.path.expandvars(path)

    def connect_db(self):
        if os.path.exists(self.db_path):
            with open(self.db_path) as f:
                return json.load(f)
        else:
            return {}

    def get_history_by_id(self, ID):
        return self.db.get(ID, "0")

    def get_history_list(self):
        return self.db.keys()

    def save(self, ID, value):
        self.db[ID] = value

    def remove(self, ID):
        if self.db.has_key(ID):
            self.db.pop(ID)

    def commit(self):
        with open(self.db_path, "w") as f:
            json.dump(self.db, f)


if __name__ == "__main__":

    if len(sys.argv) > 1:
        player = Player(file_to_play=sys.argv[1], options=sys.argv[2:])
    else:
        player = Player()
    player.play()
