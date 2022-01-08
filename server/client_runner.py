from collections import deque
import itertools
import os
import shutil
from typing import Deque, NewType
import psycopg2
import subprocess
import json
import platform
import zipfile
from psycopg2.extras import RealDictCursor
from joblib import Parallel, delayed, logger
import asyncio
import logging
import sys

from tqdm import std
import time

# Config for loggers
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class client_runner:

    def __init__(self):

        db_conn = {}
        with open('./server/conn_info.json') as fl:
            db_conn = json.load(fl)

        self.conn = psycopg2.connect(
            host="localhost",
            database=db_conn["database"],
            user=db_conn["user"],
            password=db_conn["password"]
        )
        self.loop = asyncio.get_event_loop()

        # The group run ID. will be set by insert_new_group_run
        self.group_id = 0

        self.NUMBER_OF_GAMES_AGAINST_SAME_TEAM = 3

        # IE how many combinations of clients can you make
        self.number_of_unique_games = -1

        self.SLEEP_TIME_SECONDS_BETWEEN_RUNS = 150

        # Maps a seed_index to a database seed_id
        self.index_to_seed_id = {}

        self.version = self.get_version_number()

        self.best_run_for_client = {}

        self.runner_temp_dir = 'server/runner_temp'
        self.seed_path = f"{self.runner_temp_dir}/seeds"

        # self.loop.run_in_executor(None, self.await_input)
        # self.loop.call_later(5, self.external_runner())
        try:
            while True:
                self.best_run_for_client = {}
                self.external_runner()
                self.read_best_logs_and_insert()
                self.delete_runner_temp()
                logging.warning(
                    f"Sleeping for {self.SLEEP_TIME_SECONDS_BETWEEN_RUNS} seconds")
                self.group_id = -1
                time.sleep(150)
        except (KeyboardInterrupt, Exception) as e:
            logging.warning("Ending runner due to {0}".format(e))
        finally:
            self.close_server()

    def external_runner(self):
        clients = self.fetch_clients()
        self.group_id = self.insert_new_group_run()

        if not os.path.exists(self.runner_temp_dir):
            os.mkdir(self.runner_temp_dir)

        if not os.path.exists(self.seed_path):
            os.mkdir(self.seed_path)

        for index in range(self.NUMBER_OF_GAMES_AGAINST_SAME_TEAM):
            path = f'{self.seed_path }/{index}'
            os.mkdir(path)
            shutil.copy('launcher.pyz', path)
            self.run_runner(path, "server/runners/generator")
            fldict = ""
            with open(f'{path}/logs/game_map.json') as fl:
                fldict = "".join(fl.readlines())
            self.index_to_seed_id[index] = self.insert_seed_file(fldict)

        # get the games as a list of client tuples
        #submission_id_list = list(map(lambda x: x["submission_id"], clients))
        games = self.return_team_parings(clients)

        # then run them in paralell using their index as a unique identifier
        res = Parallel(n_jobs=1, backend="threading")(
            map(delayed(self.internal_runner), games, [i for i in range(len(games))]))

    def internal_runner(self, row_tuple, index):
        winner = -1
        error = ""
        results = dict()
        try:
            # Run game
            # Create a folder for this client and seed
            end_path = f'{self.runner_temp_dir}/{index}'
            if not os.path.exists(end_path):
                os.mkdir(end_path)

            shutil.copy('launcher.pyz', end_path)

            # Write the clients into the folder
            for row in row_tuple:
                # runner will run -fn argument, which makes the team name the file name
                # So we can grab the submission_id out of the results later
                with open(f"{end_path}/client_{row['submission_id']}.py", 'w') as f:
                    f.write(row['file_text'])

            # Determine what seed this run needs based on it's serial index
            seed_index = int(index / self.number_of_unique_games)
            logging.warning("running run {0} for game ({1}, {2}) using seed index {3}".format(
                index, row_tuple[0]["submission_id"], row_tuple[1]["submission_id"], seed_index))

            # Copy the seed into the run folder
            if os.path.exists(f"{self.seed_path}/{seed_index}/logs/game_map.json"):
                os.mkdir(f"{end_path}/logs")
                shutil.copyfile(
                    f"{self.seed_path}/{seed_index}/logs/game_map.json", f"{end_path}/logs/game_map.json")

            res = self.run_runner(end_path, "server/runners/runner")

            if os.path.exists(end_path + '/logs/results.json'):
                with open(end_path + '/logs/results.json', 'r') as f:
                    results = json.load(f)

            # CHANGE THIS LINE TO GET CORRECT SCORE FOR GAME
            winner = -1
            if len(results['players_alive']) == 1:
                # Submission ID of player who won, otherwise it was a tie
                winner = results['players_alive'][0].split("_")[1]

            # for result in results['players']:
            #     if 'error' in result and result['error'] is not None:
            #         logging.warning("Run had error")
            #         error[client] = result['error']
        finally:
            player_sub_ids = [x["team_name"].split("_")[1] for x in results["players"]]
            run_id = self.insert_run(winner, player_sub_ids[0], player_sub_ids[1], self.group_id, error, self.index_to_seed_id[seed_index])
            # Update information in best run dict
            if winner != -1:
                if winner not in self.best_run_for_client:
                    self.best_run_for_client[row["submission_id"]] = {}
                    self.best_run_for_client[row["submission_id"]]["log_path"] = end_path + "/logs"
                    self.best_run_for_client[row["submission_id"]]["run_id"] = run_id

    def fetch_clients(self):
        '''
        Returns the latest clients for every team
        '''
        cur = self.conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT * FROM fetch_latest_clients()")
        return cur.fetchall()

    def run_runner(self, end_path, runner):
        '''
        runs a script in the runner folder. 
        end path is where the runner is located
        runner is the name of the script (no extension) 
        '''
        f = open(os.devnull, 'w')
        if platform.system() == 'Linux':
            shutil.copy(runner + '.sh', f"{end_path}/runner.sh")
            p = subprocess.Popen('bash runner.sh', stdout=f,
                                 cwd=end_path, shell=True)
            stdout, stderr = p.communicate()
            return stdout
        else:
            # server/runner.bat
            shutil.copy(runner + '.bat', f"{end_path}/runner.bat")
            p = subprocess.Popen('runner.bat', stdout=f,
                                 cwd=end_path, shell=True)
            stdout, stderr = p.communicate()
            return stdout

    def get_version_number(self):
        '''
        runs a script in the runner folder. 
        end path is where the runner is located
        runner is the name of the script (no extension) 
        '''

        stdout = ""
        if platform.system() == 'Linux':
            p = subprocess.Popen('server/runners/version.sh',
                                 stdout=subprocess.PIPE, shell=True)
            stdout, stderr = p.communicate()
        else:
            p = subprocess.Popen(
                'runner.bat', stdout=subprocess.PIPE, shell=True)
            stdout, stderr = p.communicate()
        return stdout.decode("utf-8")

    def insert_new_group_run(self):
        '''
        Inserts a new group run. Relates all the runs in this process together
        '''
        cur = self.conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT insert_group_run(%s, %s)",
                    (self.version, self.NUMBER_OF_GAMES_AGAINST_SAME_TEAM))
        self.conn.commit()
        return cur.fetchall()[0]["insert_group_run"]

    def insert_seed_file(self, seed):
        '''
        inserts the seed file into the database. 
        Returns it's seed_id
        '''
        cur = self.conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT insert_seed(%s, %s)", (seed, self.group_id))
        self.conn.commit()
        return cur.fetchall()[0]["insert_seed"]

    def insert_run(self, winner, player_1, player_2,  groupid, error, seed_id):
        '''
        Inserts a run into the DB
        '''
        cur = self.conn.cursor()
        cur.execute("SELECT insert_run(%s, %s, %s, %s, %s, %s)",
                    (winner, player_1, player_2, groupid, error, seed_id))
        run_id = cur.fetchone()[0]
        self.conn.commit()
        return run_id

    def delete_group_run_cascade(self, groupid):
        '''
        Inserts a run into the DB
        '''
        cur = self.conn.cursor()
        logging.warning(f"DELETING GROUP RUN {groupid}")
        cur.execute(
            "SELECT delete_group_run_and_foriegn_keys_cascade(%s)", (groupid,))
        self.conn.commit()

    def read_best_logs_and_insert(self):
        for submission_id in self.best_run_for_client:
            path = self.best_run_for_client[submission_id]["log_path"]
            dict_logs = {}
            for file in os.listdir(path):
                with open(f"{path}/{file}") as fl:
                    # It would probably be better to store each file in it's own row
                    # But I'm lazy and I'm just going to denote the split with the delimiter below
                    dict_logs[file] = fl.read()

            self.insert_log(json.dumps(dict_logs),
                            self.best_run_for_client[submission_id]["run_id"])

    def insert_log(self, log, run_id):
        '''
        inserts the seed file into the database. 
        Returns it's seed_id
        '''
        cur = self.conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT insert_log(%s, %s, %s)",
                    (str(log), run_id, self.group_id))
        self.conn.commit()

    def close_server(self):
        self.loop_continue = False
        self.conn.reset()
        if self.group_id != -1:
            self.delete_group_run_cascade(self.group_id)
        else:
            logging.warning("Not deleting any group runs")
        self.delete_runner_temp()

        os._exit(0)

    def delete_runner_temp(self):
        while True:
            try:
                if os.path.exists(self.runner_temp_dir):
                    shutil.rmtree(self.runner_temp_dir)
                break
            except PermissionError:
                continue

    def return_team_parings(self, submissions):
        fixtures = list(itertools.combinations(submissions, 2))
        self.number_of_unique_games = len(fixtures)
        repeated = fixtures * self.NUMBER_OF_GAMES_AGAINST_SAME_TEAM
        return repeated


if __name__ == "__main__":
    client_runner().external_runner()
