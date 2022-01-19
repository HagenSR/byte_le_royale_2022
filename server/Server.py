from flask import Flask, abort, jsonify
from flask.wrappers import Request
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import request
from requests.models import HTTPError
import uuid
import json
from logging.config import dictConfig
from flask.logging import logging
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.exceptions import BadRequest, HTTPException
import math

# Config for loggers
dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "logs/log_file.txt",
            "maxBytes": 10000,
            "backupCount": 10,
            "delay": "True",
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi', 'file']
    }
})


MAX_FILE_CHARACTER_COUNT = 14000

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# Config for limiter
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["1 per second"]
)

MAX_TEAM_NAME_LENGTH = 15

# Read db config information from file, set up connection
db_conn = {}
with open('./conn_info.json') as fl:
    db_conn = json.load(fl)

try:
    conn = psycopg2.connect(
        host="localhost",
        database=db_conn["database"],
        user=db_conn["user"],
        password=db_conn["password"]
    )
except Exception as e:
    app.logger.error("Failed to connect to DB: %s", e)
    raise e


# Turns abortions into json string (haha)
@app.errorhandler(HTTPException)
def handle_exception(e):
    return jsonify(error=str(e)), 404


@app.route("/api/get_unis", methods=['get'])
def get_unis():
    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT (get_universities()).*")
        if cur.rowcount == 0:
            app.logger.info('Error: No data to return for get_unis')
            return abort(500, description="No universities were found")
        else:
            return jsonify(cur.fetchall())
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        app.logger.error("Exception in get_unis: %s", e)
        conn.reset()
        abort(500, description=str(e))


@app.route("/api/get_team_types", methods=['get'])
def get_team_types():
    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT (get_team_types()).*")
        return jsonify(cur.fetchall())
    except Exception as e:
        app.logger.error("Exception in get_team_types: %s", e)
        conn.reset()
        abort(500, description=str(e))


@app.route("/api/get_teams", methods=['get'])
def get_teams():
    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT (get_teams()).*")
        return jsonify(cur.fetchall())
    except Exception as e:
        app.logger.error("Exception in get_teams: %s", e)
        conn.reset()
        abort(500, description=str(e))


@app.route("/api/get_leaderboard", methods=['post'])
@limiter.limit("5/minute", override_defaults=True)
def get_leaderboard():
    try:
        ell = request.json["include_inelligible"]
        group_id = request.json["group_id"]
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT (get_group_run_details(%s)).*", (group_id,))
        results = cur.fetchall()
        if len(results) > 0:
            results = results[0]
        else:
            abort(400, description="No data to return for leaderboard yet")
        cur.execute("SELECT (get_leaderboard(%s, %s)).*", (ell, results["group_run_id"]))
        if cur.rowcount == 0:
            app.logger.error('Error: No data to return for leaderboard')
            abort(400, description="No data to return for leaderboard yet")
        else:
            return jsonify({"data": cur.fetchall(), "group_run_info": results})
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        app.logger.error("Exception in get_leaderboard: %s", e)
        conn.reset()
        abort(500, description=str(e))


@app.route("/api/register", methods=['POST'])
@limiter.limit("10/hour", override_defaults=True)
def insert_team():
    try:
        teamtype = request.form.get("type")
        name = request.form.get("name")
        uni = request.form.get("uni")
        if len(name) >= MAX_TEAM_NAME_LENGTH:
            abort(404, description="Team name cannot be longer than {0} characters".format(MAX_TEAM_NAME_LENGTH))
        cur = conn.cursor()
        cur.execute("SELECT insert_team(%s, %s, %s)", (teamtype, name, uni))
        conn.commit()
        app.logger.info('Registered team at IP %s', request.remote_addr)
        if cur.rowcount == 0:
            return abort(404, description="Failed to register")
        else:
            return cur.fetchone()[0]
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        app.logger.error("Exception in register: %s", e)
        conn.reset()
        abort(500, description=str(e))


@app.route("/api/submit", methods=['POST'])
@limiter.limit("1/minute", override_defaults=True)
def submit_file():
    try:
        file = request.json["file"]
        vid = request.json["vid"]
        bad_words = check_illegal_keywords(file)
        if len(file) > MAX_FILE_CHARACTER_COUNT:
            abort(
                404,
                description="Files can be a maximum of {} characters and this file is {} characters long".format(
                    MAX_FILE_CHARACTER_COUNT,
                    len(file)))
        if bad_words:
            abort(404, description="Contained illegal keywords {0}".format(bad_words))
        cur = conn.cursor()
        cur.execute("CALL submit_code_file(%s, %s)", (file, vid))
        conn.commit()
        app.logger.info('Recieved submission from %s at IP %s', vid, request.remote_addr)
        return "True"
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        app.logger.error("Exception in submit: %s", e)
        conn.reset()
        abort(500, description=str(e))


def check_illegal_keywords(file):
    '''This should be expanded on, made better'''
    bad_words_list = ['open', 'os', 'import']
    rtn_bad_words = []
    for bad_word in rtn_bad_words:
        if bad_word in file:
            rtn_bad_words.append(bad_word)


@app.route("/api/get_submission_stats", methods=['post'])
@limiter.limit("5/minute", override_defaults=True)
def get_stats():
    try:
        vid = request.json["vid"]
        cur = conn.cursor()
        cur.execute("SELECT (get_latest_submission(%s)).*", (vid,))
        res = cur.fetchone()
        if res is None:
            app.logger.error(
                'Error: no submission made for VID %s yet', vid)
            abort(404, description="No submissions for this Vid were found")
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT (get_runs_for_submission_and_group(%s, %s)).*", res[:2])
        if cur.rowcount == 0:
            app.logger.error(
                'Error: No data to return submissions_stats for %s', vid)
            abort(404, description="No submissions for this Vid were found")
        else:
            runs = cur.fetchall()
            return jsonify({"data": runs, "sub_id": res[0], "run_group_id": res[1], "runs_per_client": res[2]})
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        app.logger.error("Exception in get_submission_stats: %s", e)
        conn.reset()
        abort(500, description=str(e))


@app.route("/api/get_team_score_over_time", methods=['post'])
@limiter.limit("5/minute", override_defaults=True)
def get_team_score_over_time():
    try:
        vid = request.json["vid"]
        cur = conn.cursor()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT (get_team_score_over_time(%s)).*", (vid,))
        app.logger.info(
            'Returning get_team_score_over_time for %s at IP %s', vid, request.remote_addr)
        if cur.rowcount == 0:
            app.logger.error(
                'Error: No data to return team_score_over_time for %s', vid)
            return abort(404, description="No data to return team_score_over_time for this Vid")
        else:
            return jsonify(cur.fetchall())
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        app.logger.error("Exception in get_leaderboard: %s", e)
        conn.reset()
        abort(500, description=str(e))


@app.route("/api/get_submissions_for_team", methods=['post'])
@limiter.limit("5/minute", override_defaults=True)
def get_submissions_for_team():
    try:
        vid = request.json["vid"]
        cur = conn.cursor()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT (get_submissions_for_team(%s)).*", (vid,))
        if cur.rowcount == 0:
            app.logger.error(
                'Error: No data to return for get_submissions_for_team for %s', vid)
            abort(404, description="No data to return for get_submissions_for_team for this Vid")
        else:
            return jsonify(cur.fetchall())
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        app.logger.error("Exception in get_submissions_for_team: %s", e)
        conn.reset()
        abort(500, description=str(e))


@app.route("/api/get_group_runs", methods=['post'])
@limiter.limit("5/minute", override_defaults=True)
def get_group_runs():
    try:
        vid = request.json["vid"]
        cur = conn.cursor()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT (get_group_runs(%s)).*", (vid,))
        if cur.rowcount == 0:
            return abort(404, description="No group runs were found")
        else:
            return jsonify(cur.fetchall())
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        app.logger.error("Exception in get_group_runs: %s", e)
        conn.reset()
        abort(500, description=str(e))


@app.route("/api/get_runs_for_group_run", methods=['post'])
@limiter.limit("5/minute", override_defaults=True)
def get_team_runs_for_group_run():
    try:
        groupid = request.json["groupid"]
        cur = conn.cursor()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT (get_runs_for_group(%s)).*", (groupid,))
        if cur.rowcount == 0:
            return abort(404, description="No group runs were found")
        else:
            return jsonify(cur.fetchall())
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        app.logger.error("Exception in get_group_runs: %s", e)
        conn.reset()
        abort(500, description=str(e))


@app.route("/api/get_runs_for_submission", methods=['post'])
@limiter.limit("5/minute", override_defaults=True)
def get_runs_for_submission():
    try:
        vid = request.json["vid"]
        subid = request.json["submissionid"]
        cur = conn.cursor()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT (get_runs_for_submission(%s, %s)).*", (vid, subid))
        if cur.rowcount == 0:
            app.logger.error(
                'Error: No data to return for get_runs_for_submission for %s', vid)
            raise abort(404, description="No submissions were found")
        else:
            return jsonify(cur.fetchall())
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        app.logger.error("Exception in get_runs_for_submission: %s", e)
        conn.reset()
        abort(500, description=str(e))


@app.route("/api/get_file_from_submission", methods=['post'])
@limiter.limit("1/minute", override_defaults=True)
def get_file_from_submission():
    try:
        vid = request.json["vid"]
        subid = request.json["submissionid"]
        cur = conn.cursor()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT get_file_from_submission(%s, %s)", (vid, subid))
        app.logger.info('Returning file for submissionid %s for team %s at IP %s', subid, vid, request.remote_addr)
        if cur.rowcount == 0:
            app.logger.error(
                'Error: No data to return for get_file_from_submission for %s', vid)
            return abort(404, description="No data to return for get_file_from_submission for this Vid")
        else:
            return jsonify(cur.fetchone()["get_file_from_submission"])
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        app.logger.error("Exception in get_file_for_submission: %s", e)
        conn.reset()
        abort(500, description=str(e))


@app.route("/api/get_seed_from_run", methods=['post'])
@limiter.limit("1/minute", override_defaults=True)
def get_seed_from_run():
    try:
        vid = request.json["vid"]
        runid = request.json["runid"]
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT get_seed_for_run(%s, %s)", (vid, runid))
        app.logger.info('Returning seed for runid %s for team %s at IP %s',
                        runid, vid, request.remote_addr)
        if cur.rowcount == 0:
            app.logger.error(
                'Error: No data to return for get_seed_from_run for %s', vid)
            return abort(404, description="No data to return for get_seed_from_run")
        else:
            res = cur.fetchone()["get_seed_for_run"]
            return res if res is not None else ""
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        app.logger.error("Exception in get_seed_from_run: %s", str(e))
        conn.reset()
        abort(500, description=str(e))


@app.route("/api/get_code_from_submission", methods=['post'])
@limiter.limit("5/minute", override_defaults=True)
def get_code_from_submission():
    try:
        vid = request.json["vid"]
        subid = request.json["subid"]
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT get_file_from_submission(%s, %s)", (vid, subid))
        app.logger.info('Returning code for subid %s for team %s at IP %s',
                        subid, vid, request.remote_addr)
        if cur.rowcount == 0:
            app.logger.error(
                'Error: No data to return for get_seed_from_run for %s', vid)
            return abort(404, description="No data to return for get_seed_from_run")
        else:
            res = cur.fetchone()["get_file_from_submission"]
            return res if res is not None else ""
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        app.logger.error("Exception in get_seed_from_run: %s", str(e))
        conn.reset()
        abort(500, description=str(e))
