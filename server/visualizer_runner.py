import asyncio
import time
import json
import random
import os
import shutil
import subprocess
import platform
import zipfile
import psycopg2
from psycopg2.extras import RealDictCursor


class visualizer_runner:
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

        # Current group run ID of logs
        self.group_id = 0

        self.logs_path = 'server/vis_temp'
        try:
            while True:
                group_id = self.get_latest_group()
                if self.group_id != group_id:
                    print("getting new logs")
                    self.group_id = group_id
                    self.get_latest_log_files()
                self.visualizer_loop()
                time.sleep(15)
        except (KeyboardInterrupt, Exception) as e:
            print("Ending visualizer due to {0}".format(e))
        finally:
            self.delete_vis_temp()

    def get_latest_log_files(self):
        self.delete_vis_temp()

        print("getting latest log files")
        cur = self.conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT (get_logs_for_group_run(%s)).*", (self.group_id,))
        logs = cur.fetchall()

        for log in logs:
            # Take logs and copy into directory
            team_dir = f'{self.logs_path}/{log["team_name"]}'
            os.mkdir(team_dir)
            logs_dir = team_dir + "/logs"
            os.mkdir(logs_dir)
            files = json.loads(log['log_text'])
            for index, key in enumerate(files):
                with open(f"{logs_dir}/{key}", "w") as fl:
                    fl.write(files[key])

            shutil.copy('launcher.pyz', team_dir)

            shutil.copy('visualizer.x86_64', team_dir)

            shutil.copy('visualizer.pck', team_dir)

            shutil.copytree('visualizer/assets', team_dir + "/visualizer")

            shutil.copy('server/runners/vis_runner.sh', team_dir)

    def get_latest_group(self):
        print("Getting Latest Group Run")
        cur = self.conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT get_latest_group_id()")
        id = cur.fetchone()['get_latest_group_id']
        return id

    def delete_vis_temp(self):
        if not os.path.exists(self.logs_path):
            os.mkdir(self.logs_path)
        else:
            shutil.rmtree(self.logs_path)
            os.mkdir(self.logs_path)

    def visualizer_loop(self):

        previous_team = None
        for team_dir in os.listdir(self.logs_path):
            try:
                f = open(os.devnull, 'w')
                path = f"{self.logs_path}/{team_dir}"
                p = subprocess.Popen('bash vis_runner.sh', stdout=f, cwd=path, shell=True)
                stdout, stderr = p.communicate()

            except PermissionError:
                print("Whoops")


if __name__ == "__main__":
    visualizer_runner()
