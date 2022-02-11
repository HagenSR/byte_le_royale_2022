import asyncio
import datetime
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

        today930pm = datetime.datetime.now().replace(hour=21, minute=30, second=0, microsecond=0)
        try:
            while datetime.datetime.now() < today930pm or True:
                group_id = self.get_latest_group()
                if self.group_id != group_id:
                    print("getting new logs")
                    self.get_latest_log_files(group_id)
                    self.group_id = group_id
                self.visualizer_loop()
                time.sleep(30)
        except (KeyboardInterrupt, Exception) as e:
            print("Ending visualizer due to {0}".format(e))
        finally:
            self.delete_vis_temp()

    def get_latest_log_files(self, group_id):
        self.delete_vis_temp()

        print("getting latest log files")
        cur = self.conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT (get_logs_for_group_run(%s)).*", (group_id,))
        logs = cur.fetchall()

        for log in logs:
            # Take logs and copy into directory
            team_dir = f'{self.logs_path}/{log["team_name"]}'
            if not os.path.isdir(team_dir):
                os.mkdir(team_dir)
            id_dir = f'{team_dir}/{log["run_id"]}'
            os.mkdir(id_dir)
            logs_dir = id_dir + "/logs"
            os.mkdir(logs_dir)
            files = json.loads(log['log_text'])
            for index, key in enumerate(files):
                with open(f"{logs_dir}/{key}", "w") as fl:
                    fl.write(files[key])

            shutil.copy('launcher.pyz', id_dir)

            shutil.copy('visualizer.x86_64', id_dir)

            shutil.copy('visualizer.pck', id_dir)

            shutil.copytree('Visualizer/Assets', id_dir + "/visualizer")

            shutil.copy('server/runners/vis_runner.sh', id_dir)

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
                for id in os.listdir(path):
                    idpath = f"{path}/{id}"
                    p = subprocess.Popen('bash vis_runner.sh', stdout=f, cwd=idpath, shell=True)
                    stdout, stderr = p.communicate()

            except PermissionError:
                print("Whoops")


if __name__ == "__main__":
    visualizer_runner()
