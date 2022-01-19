--
-- PostgreSQL database dump
--

-- Dumped from database version 12.9 (Ubuntu 12.9-2.pgdg20.04+1)
-- Dumped by pg_dump version 14.1 (Ubuntu 14.1-2.pgdg20.04+1)

-- Started on 2022-01-18 19:16:01 CST

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 2 (class 3079 OID 16419)
-- Name: uuid-ossp; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA public;


--
-- TOC entry 3092 (class 0 OID 0)
-- Dependencies: 2
-- Name: EXTENSION "uuid-ossp"; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION "uuid-ossp" IS 'generate universally unique identifiers (UUIDs)';


--
-- TOC entry 245 (class 1255 OID 16430)
-- Name: delete_group_run_and_foriegn_keys_cascade(integer); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.delete_group_run_and_foriegn_keys_cascade(grouprunid integer) RETURNS integer
    LANGUAGE plpgsql
    AS $$
DECLARE rtnid integer;
BEGIN
-- Created by: Sean Hagen
-- Written on: 12/15/2021
-- Deletes a group run, and FKs delete in the cascade
	DELETE FROM group_run WHERE group_run.group_run_id = grouprunid;
	return 1;
end;
$$;


ALTER FUNCTION public.delete_group_run_and_foriegn_keys_cascade(grouprunid integer) OWNER TO postgres;

--
-- TOC entry 246 (class 1255 OID 16431)
-- Name: fetch_latest_clients(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.fetch_latest_clients() RETURNS TABLE(team_id uuid, submission_id integer, file_text character varying)
    LANGUAGE plpgsql
    AS $$
BEGIN
-- Select latest code files. Because of the serial nature of submissionID, we can use max(subid) to 
-- find the latest submission.
RETURN QUERY
SELECT
    sub.team_id,
    sub.submission_id,
    code_file.file_text
from
    code_file
    JOIN (
        SELECT
            submission.team_id,
            MAX(submission.submission_id) as submission_id
        FROM
            submission
        GROUP BY
            submission.team_id
    ) as sub ON sub.submission_id = code_file.submission_id;
end;
$$;


ALTER FUNCTION public.fetch_latest_clients() OWNER TO postgres;

--
-- TOC entry 247 (class 1255 OID 16432)
-- Name: get_file_from_submission(uuid, integer); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.get_file_from_submission(teamid uuid, submissionid integer) RETURNS character varying
    LANGUAGE plpgsql
    AS $$
BEGIN
-- Created by: Sean Hagen
-- Written on: 11/1/2021
-- Returns the code file for a given submission
RETURN file_text FROM code_file JOIN submission ON code_file.submission_id = submission.submission_id
WHERE team_id = teamid AND submission.submission_id = submissionid;
--SELECT * FROM team
end;
$$;


ALTER FUNCTION public.get_file_from_submission(teamid uuid, submissionid integer) OWNER TO postgres;

--
-- TOC entry 260 (class 1255 OID 16596)
-- Name: get_group_run_details(integer); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.get_group_run_details(groupid integer) RETURNS TABLE(group_run_id integer, start_run timestamp without time zone, runs_per_client integer, launcher_version character varying)
    LANGUAGE plpgsql
    AS $$
DECLARE grpId int := groupid;
BEGIN
-- Created by: Sean Hagen
-- Written on: 11/1/2021
-- Select the latest submission_id, group_run_id for a team as well as the runs_per_team for that group run

IF grpId = -1 THEN
	SELECT group_run.group_run_id INTO grpId FROM group_run ORDER BY group_run.group_run_id DESC LIMIT 1;
END IF;

RETURN QUERY
SELECT
	group_run.group_run_id,
	group_run.start_run,
	group_run.runs_per_client,
	group_run.launcher_version
FROM
    group_run
WHERE group_run.group_run_id = grpId;
end;
$$;


ALTER FUNCTION public.get_group_run_details(groupid integer) OWNER TO postgres;

--
-- TOC entry 249 (class 1255 OID 16433)
-- Name: get_group_runs(uuid); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.get_group_runs(teamid uuid) RETURNS TABLE(group_run_id integer, run_time timestamp without time zone, launcher_version character varying, runs_per_client integer)
    LANGUAGE plpgsql
    AS $$
BEGIN
-- Created by: Sean Hagen
-- Written on: 12/30/2021
-- teamid: uuid to get runs for
-- Returns the group runs this team has been in
RETURN QUERY
SELECT DISTINCT group_run.group_run_id, group_run.start_run, group_run.launcher_version, group_run.runs_per_client FROM group_run 
JOIN run ON run.group_run_id = group_run.group_run_id 
JOIN submission ON run.player_1 = submission.submission_id OR run.player_2 = submission.submission_id 
WHERE submission.team_id = teamid
ORDER BY group_run.start_run DESC;

end;
$$;


ALTER FUNCTION public.get_group_runs(teamid uuid) OWNER TO postgres;

--
-- TOC entry 248 (class 1255 OID 16434)
-- Name: get_latest_group_id(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.get_latest_group_id() RETURNS integer
    LANGUAGE plpgsql
    AS $$
BEGIN
-- Created by: Sean Hagen
-- Written on: 12/2/2021
-- Returns the latest group run id 
RETURN group_run.group_run_id FROM group_run ORDER BY group_run_id desc LIMIT 1;
end;
$$;


ALTER FUNCTION public.get_latest_group_id() OWNER TO postgres;

--
-- TOC entry 250 (class 1255 OID 16435)
-- Name: get_latest_submission(uuid); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.get_latest_submission(teamid uuid) RETURNS TABLE(submission_id integer, group_run_id integer, runs_per_client integer)
    LANGUAGE plpgsql
    AS $$
BEGIN
-- Created by: Sean Hagen
-- Written on: 11/1/2021
-- Select the latest submission_id, group_run_id for a team as well as the runs_per_team for that group run
RETURN QUERY
SELECT DISTINCT
    latest_submission.subid,
    latest_submission.group_run_id,
	group_run.runs_per_client
FROM
    group_run
    JOIN (
        SELECT
            MAX(submission.submission_id) as subid,
            MAX(run.group_run_id) as group_run_id
        FROM
            run
            JOIN submission ON run.player_1 = submission.submission_id OR run.player_2 = submission.submission_id
        WHERE
            submission.team_id = teamid

) as latest_submission ON group_run.group_run_id = latest_submission.group_run_id;
end;
$$;


ALTER FUNCTION public.get_latest_submission(teamid uuid) OWNER TO postgres;

--
-- TOC entry 261 (class 1255 OID 16687)
-- Name: get_leaderboard(boolean, integer); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.get_leaderboard(include_inelligible boolean, grouprun integer) RETURNS TABLE(place bigint, team_name character varying, uni_name character varying, total_wins bigint)
    LANGUAGE plpgsql
    AS $$
BEGIN
-- Created by: Sean Hagen
-- Written on: 11/1/2021
-- include_inelligible: if true, return inelligible teams in the results
-- group_run: if -1 then return most recent group_run, else return results for the specified group run
RETURN QUERY
SELECT dense_rank() OVER (
        ORDER BY infos.total_wins DESC
    ) as place,
    infos.*
FROM (
        SELECT team.team_name,
            university.uni_name,
            COALESCE(cnts.total_wins, 0) as total_wins
        FROM submission
            LEFT JOIN (
                SELECT winner,
                    COUNT(winner) as total_wins
                FROM run
                WHERE run.group_run_id = grouprun
                group by winner
            ) as cnts ON cnts.winner = submission.submission_id
            JOIN team on submission.team_id = team.team_id
            JOIN team_type on team.team_type_id = team_type.team_type_id
            JOIN university on team.uni_id = university.uni_id
        WHERE (
                team_type.eligible
                OR include_inelligible
            )
    ) as infos;
end;
$$;


ALTER FUNCTION public.get_leaderboard(include_inelligible boolean, grouprun integer) OWNER TO postgres;

--
-- TOC entry 251 (class 1255 OID 16437)
-- Name: get_logs_for_group_run(integer); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.get_logs_for_group_run(grouprun integer) RETURNS TABLE(run_id integer, group_run_id integer, submission_id integer, team_name character varying, log_text character varying)
    LANGUAGE plpgsql
    AS $$
BEGIN--SELECT * FROM team
-- Created by: Sean Hagen
-- Written on: 1/1/2021
-- returns the logs for a given group run
RETURN QUERY
SELECT DISTINCT
    run.run_id,
    run.group_run_id,
    run.submission_id,
    team.team_name,
	logs.log_text
FROM
	logs JOIN run ON logs.run_id = run.run_id
    JOIN submission ON run.player_1 = submission.submission_id OR run.player_2 = submission.submission_id
    JOIN team ON submission.team_id = team.team_id
WHERE
    run.group_run_id = grouprun;
end;
$$;


ALTER FUNCTION public.get_logs_for_group_run(grouprun integer) OWNER TO postgres;

--
-- TOC entry 263 (class 1255 OID 16698)
-- Name: get_runs_for_submission(uuid, integer); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.get_runs_for_submission(teamid uuid, submissionid integer) RETURNS TABLE(run_id integer, group_run_id integer, run_time timestamp without time zone, winner integer, player_1 integer, player_2 integer, seed_id integer, launcher_version character varying)
    LANGUAGE plpgsql
    AS $$
BEGIN
-- Created by: Sean Hagen
-- Written on: 12/30/2021
-- teamid: uuid to get runs for
-- submiddionid: submission id to get runs for
-- Returns the runs for a given team and submission
RETURN QUERY
SELECT DISTINCT run.run_id, run.group_run_id, run.run_time, run.winner, run.player_1, run.player_2, run.seed_id, group_run.launcher_version
FROM submission JOIN run ON submission.submission_id = run.player_1 OR submission.submission_id = run.player_2 JOIN group_run on run.group_run_id = group_run.group_run_id
WHERE submission.team_id = teamid AND submission.submission_id = submissionid
ORDER BY run.run_time DESC;
--SELECT * FROM team
end;
$$;


ALTER FUNCTION public.get_runs_for_submission(teamid uuid, submissionid integer) OWNER TO postgres;

--
-- TOC entry 265 (class 1255 OID 16701)
-- Name: get_runs_for_submission_and_group(integer, integer); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.get_runs_for_submission_and_group(submissionid integer, groupid integer) RETURNS TABLE(group_run_id integer, run_id integer, run_time timestamp without time zone, winner integer, player_1 integer, player_2 integer)
    LANGUAGE plpgsql
    AS $$
BEGIN
-- Created by: Sean Hagen
-- Written on: 12/30/2021
-- returns the runs for a given submission and group_run
RETURN QUERY
SELECT DISTINCT run.group_run_id, run.run_id, run.run_time, run.winner, run.player_1, run.player_2 FROM run JOIN submission 
ON run.player_1 = submission.submission_id OR run.player_2 = submission.submission_id
WHERE (run.player_1 = submissionid or run.player_2 = submissionid) AND run.group_run_id = groupid;
end;
$$;


ALTER FUNCTION public.get_runs_for_submission_and_group(submissionid integer, groupid integer) OWNER TO postgres;

--
-- TOC entry 253 (class 1255 OID 16440)
-- Name: get_seed_for_run(uuid, integer); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.get_seed_for_run(teamid uuid, runid integer) RETURNS character varying
    LANGUAGE plpgsql
    AS $$
BEGIN
-- Created by: Sean Hagen
-- Written on: 12/15/2021
-- teamid : uuid to get seed for
-- runid: run id to get seed for
-- returns the seed for a given team and run
RETURN seed
FROM
    run
    JOIN seed ON run.seed_id = seed.seed_id
    JOIN submission ON run.player_1 = submission.submission_id OR run.player_2 = submission.submission_id
WHERE
    team_id = teamid
    AND run_id = runid;
end;
$$;


ALTER FUNCTION public.get_seed_for_run(teamid uuid, runid integer) OWNER TO postgres;

--
-- TOC entry 252 (class 1255 OID 16441)
-- Name: get_submissions_for_team(uuid); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.get_submissions_for_team(teamid uuid) RETURNS TABLE(submission_id integer, submit_time timestamp without time zone)
    LANGUAGE plpgsql
    AS $$
BEGIN--SELECT * FROM team
-- Created by: Sean Hagen
-- Written on: 12/15/2021
-- returns all submission ids a team has
RETURN QUERY
SELECT submission.submission_id, submission.submit_time FROM SUBMISSION 
WHERE team_id = teamid
ORDER BY submit_time DESC;
end;
$$;


ALTER FUNCTION public.get_submissions_for_team(teamid uuid) OWNER TO postgres;

--
-- TOC entry 264 (class 1255 OID 16700)
-- Name: get_team_runs_for_group_run(uuid, integer); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.get_team_runs_for_group_run(teamid uuid, grouprunid integer) RETURNS TABLE(run_id integer, submission_run_id integer, winner integer, player_1 integer, player_2 integer, run_time timestamp without time zone, seed_id integer, launcher_version character varying)
    LANGUAGE plpgsql
    AS $$
BEGIN
-- Created by: Sean Hagen
-- Written on: 12/30/2021
-- gets the runs for a given group run and team
RETURN QUERY
SELECT DISTINCT run.run_id, submission.submission_id, run.winner, run.player_1, run.player_2, run.run_time, run.seed_id, group_run.launcher_version
FROM submission JOIN run ON submission.submission_id = run.player_1 OR submission.submission_id = run.player_2  JOIN group_run ON group_run.group_run_id = run.group_run_id
WHERE submission.team_id = teamid AND run.group_run_id = grouprunid
ORDER BY run.run_time DESC;
end;
$$;


ALTER FUNCTION public.get_team_runs_for_group_run(teamid uuid, grouprunid integer) OWNER TO postgres;

--
-- TOC entry 262 (class 1255 OID 16697)
-- Name: get_team_score_over_time(uuid); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.get_team_score_over_time(teamid uuid) RETURNS TABLE(group_run_id integer, place bigint, team_name character varying, start_run timestamp without time zone, total_wins bigint, launcher_version character varying)
    LANGUAGE plpgsql
    AS $$
BEGIN
-- Created by: Sean Hagen
-- Written on: 11/1/2021
-- gets a teams average score for each group run they were in
RETURN QUERY
SELECT results.group_run_id,
	results.place,
    results.team_name,
    results.start_run,
    results.total_wins,
    results.launcher_version
FROM (
        SELECT group_run.group_run_id, group_run.start_run, group_run.launcher_version,
		(get_leaderboard(true, group_run.group_run_id)).*
		as leaderboard
        FROM group_run
    ) as results 
WHERE results.team_name = (
        Select team.team_name
        FROM team
        WHERE team.team_id = teamid
 )
ORDER BY results.group_run_id DESC;
end;
$$;


ALTER FUNCTION public.get_team_score_over_time(teamid uuid) OWNER TO postgres;

--
-- TOC entry 254 (class 1255 OID 16444)
-- Name: get_team_types(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.get_team_types() RETURNS TABLE(team_type_id integer, team_type_name character varying)
    LANGUAGE plpgsql
    AS $$
BEGIN
-- Created by: Sean Hagen
-- Written on: 11/1/2021
-- returns the team type table
RETURN QUERY
SELECT team_type.team_type_id, team_type.team_type_name FROM team_type;
end;
$$;


ALTER FUNCTION public.get_team_types() OWNER TO postgres;

--
-- TOC entry 255 (class 1255 OID 16445)
-- Name: get_teams(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.get_teams() RETURNS TABLE(team_name character varying, uni_name character varying, team_type_name character varying)
    LANGUAGE plpgsql
    AS $$
BEGIN
-- Created by: Sean Hagen
-- Written on: 12/15/2021
-- returns all of the teams that registered
RETURN QUERY
SELECT team.team_name, university.uni_name, team_type.team_type_name FROM team 
JOIN university ON team.uni_id = university.uni_id 
JOIN team_type ON team.team_type_id = team_type.team_type_id;
end;
$$;


ALTER FUNCTION public.get_teams() OWNER TO postgres;

--
-- TOC entry 256 (class 1255 OID 16446)
-- Name: get_universities(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.get_universities() RETURNS TABLE(uni_id integer, uni_name character varying)
    LANGUAGE plpgsql
    AS $$
BEGIN
-- Selects all universities
RETURN QUERY
SELECT university.uni_id, university.uni_name FROM university;
end;
$$;


ALTER FUNCTION public.get_universities() OWNER TO postgres;

--
-- TOC entry 257 (class 1255 OID 16447)
-- Name: insert_group_run(character varying, integer); Type: FUNCTION; Schema: public; Owner: byte_api
--

CREATE FUNCTION public.insert_group_run(launcherversion character varying, runsperclient integer) RETURNS integer
    LANGUAGE plpgsql
    AS $$
DECLARE rtnid integer;
BEGIN
-- Created by: Sean Hagen
-- Written on: 12/15/2021
-- Insert into group run. both id and timestamp are default, so only LauncherVersion and number of runs per client are needed
    INSERT INTO group_run(launcher_version, runs_per_client) VALUES (LauncherVersion, runsperclient) RETURNING group_run_id INTO rtnid;
	return rtnid;
end;
$$;


ALTER FUNCTION public.insert_group_run(launcherversion character varying, runsperclient integer) OWNER TO byte_api;

--
-- TOC entry 258 (class 1255 OID 16448)
-- Name: insert_log(character varying, integer, integer); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.insert_log(logfl character varying, runid integer, grouprunid integer) RETURNS void
    LANGUAGE plpgsql
    AS $$
BEGIN
-- Created by: Sean Hagen
-- Written on: 12/15/2021
-- Inserts a log into the log table. Note the cascading delete effect that group run and run have on this table!
    INSERT INTO logs (log_text, run_id, group_run_id) VALUES (logfl, runid, groupRunId);
end;
$$;


ALTER FUNCTION public.insert_log(logfl character varying, runid integer, grouprunid integer) OWNER TO postgres;

--
-- TOC entry 231 (class 1255 OID 16449)
-- Name: insert_run(integer, integer, integer, character varying, integer); Type: FUNCTION; Schema: public; Owner: byte_api
--

CREATE FUNCTION public.insert_run(sub_id integer, score integer, group_run_id integer, err character varying, seedid integer) RETURNS integer
    LANGUAGE plpgsql
    AS $$
DECLARE runid int;
begin
    -- insert run into run table
	INSERT INTO run(submission_id, score, group_run_id, seed_id) 
	VALUES (sub_id, score, group_run_id, seedid) RETURNING run_id INTO runid;
	
	if err <> '' then
		INSERT INTO errors VALUES (runid, err);
	end if;
	return runid;
end;
$$;


ALTER FUNCTION public.insert_run(sub_id integer, score integer, group_run_id integer, err character varying, seedid integer) OWNER TO byte_api;

--
-- TOC entry 259 (class 1255 OID 16663)
-- Name: insert_run(integer, integer, integer, integer, character varying, integer); Type: FUNCTION; Schema: public; Owner: byte_api
--

CREATE FUNCTION public.insert_run(winn integer, player1 integer, player2 integer, grouprunid integer, err character varying, seedid integer) RETURNS integer
    LANGUAGE plpgsql
    AS $$
DECLARE runid int;
begin
    -- insert run into run table
	INSERT INTO run(winner, player_1, player_2, group_run_id, seed_id)
	VALUES (nullif(winn, -1), player1, player2, grouprunid, seedid) RETURNING run_id INTO runid;
	
	if err <> '' then
		INSERT INTO errors VALUES (runid, err);
	end if;
	return runid;
end;
$$;


ALTER FUNCTION public.insert_run(winn integer, player1 integer, player2 integer, grouprunid integer, err character varying, seedid integer) OWNER TO byte_api;

--
-- TOC entry 232 (class 1255 OID 16450)
-- Name: insert_seed(character varying, integer); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.insert_seed(seedfl character varying, grouprunid integer) RETURNS integer
    LANGUAGE plpgsql
    AS $$
DECLARE rtnid integer;
BEGIN
-- Created by: Sean Hagen
-- Written on: 12/15/2021
-- Inserts a seed into the seed table. Note that seeds are re-used by each team and delete when there group run is deleted
    INSERT INTO seed (seed, group_run_id) VALUES (seedfl, groupRunId) RETURNING seed_id INTO rtnid;
	return rtnid;
end;
$$;


ALTER FUNCTION public.insert_seed(seedfl character varying, grouprunid integer) OWNER TO postgres;

--
-- TOC entry 233 (class 1255 OID 16451)
-- Name: insert_team(integer, character varying, integer); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.insert_team(team_type integer, team character varying, uni integer) RETURNS uuid
    LANGUAGE plpgsql
    AS $$
DECLARE tmid uuid;
BEGIN
-- Created by: Sean Hagen
-- Inserts a new team into the team table
-- Returns team id
    INSERT INTO team (team_type_id, team_name, uni_id) VALUES (team_type, team, uni)  RETURNING team_id INTO tmid;
	return tmid;
end;
$$;


ALTER FUNCTION public.insert_team(team_type integer, team character varying, uni integer) OWNER TO postgres;

--
-- TOC entry 234 (class 1255 OID 16452)
-- Name: submit_code_file(character varying, uuid); Type: PROCEDURE; Schema: public; Owner: postgres
--

CREATE PROCEDURE public.submit_code_file(file character varying, vid uuid)
    LANGUAGE plpgsql
    AS $$
DECLARE sub_ID int = 0;
begin
    -- insert submission into submission table
	INSERT INTO SUBMISSION (team_id) VALUES (vid) RETURNING submission_id INTO sub_ID;
	
    -- insert file into file table
	INSERT INTO code_file(submission_id, file_text) VALUES (sub_id, file);
end;
$$;


ALTER PROCEDURE public.submit_code_file(file character varying, vid uuid) OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 203 (class 1259 OID 16453)
-- Name: code_file; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.code_file (
    submission_id integer,
    file_text character varying
);


ALTER TABLE public.code_file OWNER TO postgres;

--
-- TOC entry 204 (class 1259 OID 16459)
-- Name: errors; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.errors (
    run_id integer,
    error_text character varying,
    submission_id integer
);


ALTER TABLE public.errors OWNER TO postgres;

--
-- TOC entry 205 (class 1259 OID 16465)
-- Name: group_run; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.group_run (
    group_run_id integer NOT NULL,
    start_run timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    launcher_version character varying(10) NOT NULL,
    runs_per_client integer
);


ALTER TABLE public.group_run OWNER TO postgres;

--
-- TOC entry 206 (class 1259 OID 16469)
-- Name: group_run_group_run_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.group_run_group_run_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.group_run_group_run_id_seq OWNER TO postgres;

--
-- TOC entry 3093 (class 0 OID 0)
-- Dependencies: 206
-- Name: group_run_group_run_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.group_run_group_run_id_seq OWNED BY public.group_run.group_run_id;


--
-- TOC entry 207 (class 1259 OID 16471)
-- Name: logs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.logs (
    run_id integer,
    log_text character varying,
    group_run_id integer
);


ALTER TABLE public.logs OWNER TO postgres;

--
-- TOC entry 208 (class 1259 OID 16477)
-- Name: run; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.run (
    run_id integer NOT NULL,
    group_run_id integer,
    run_time timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    seed_id integer,
    winner integer,
    player_1 integer,
    player_2 integer
);


ALTER TABLE public.run OWNER TO postgres;

--
-- TOC entry 209 (class 1259 OID 16481)
-- Name: run_runid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.run_runid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.run_runid_seq OWNER TO postgres;

--
-- TOC entry 3094 (class 0 OID 0)
-- Dependencies: 209
-- Name: run_runid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.run_runid_seq OWNED BY public.run.run_id;


--
-- TOC entry 210 (class 1259 OID 16483)
-- Name: seed; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.seed (
    seed_id integer NOT NULL,
    seed character varying,
    group_run_id integer
);


ALTER TABLE public.seed OWNER TO postgres;

--
-- TOC entry 211 (class 1259 OID 16489)
-- Name: seed_seed_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.seed_seed_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.seed_seed_id_seq OWNER TO postgres;

--
-- TOC entry 3095 (class 0 OID 0)
-- Dependencies: 211
-- Name: seed_seed_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.seed_seed_id_seq OWNED BY public.seed.seed_id;


--
-- TOC entry 212 (class 1259 OID 16491)
-- Name: submission; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.submission (
    team_id uuid,
    submission_id integer NOT NULL,
    submit_time timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.submission OWNER TO postgres;

--
-- TOC entry 213 (class 1259 OID 16496)
-- Name: submission_submissionid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.submission_submissionid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.submission_submissionid_seq OWNER TO postgres;

--
-- TOC entry 3096 (class 0 OID 0)
-- Dependencies: 213
-- Name: submission_submissionid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.submission_submissionid_seq OWNED BY public.submission.submission_id;


--
-- TOC entry 214 (class 1259 OID 16498)
-- Name: team; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.team (
    team_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    uni_id integer,
    team_type_id integer,
    team_name character varying(100) NOT NULL,
    CONSTRAINT team_teamname_check CHECK (((team_name)::text <> ''::text))
);


ALTER TABLE public.team OWNER TO postgres;

--
-- TOC entry 215 (class 1259 OID 16503)
-- Name: team_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.team_type (
    team_type_id integer NOT NULL,
    team_type_name character varying(100) NOT NULL,
    eligible boolean,
    CONSTRAINT teamtype_teamname_check CHECK (((team_type_name)::text <> ''::text))
);


ALTER TABLE public.team_type OWNER TO postgres;

--
-- TOC entry 216 (class 1259 OID 16507)
-- Name: teamtype_teamtypeid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.teamtype_teamtypeid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.teamtype_teamtypeid_seq OWNER TO postgres;

--
-- TOC entry 3097 (class 0 OID 0)
-- Dependencies: 216
-- Name: teamtype_teamtypeid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.teamtype_teamtypeid_seq OWNED BY public.team_type.team_type_id;


--
-- TOC entry 217 (class 1259 OID 16509)
-- Name: university; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.university (
    uni_id integer NOT NULL,
    uni_name character varying(100) NOT NULL,
    CONSTRAINT university_uniname_check CHECK (((uni_name)::text <> ''::text))
);


ALTER TABLE public.university OWNER TO postgres;

--
-- TOC entry 218 (class 1259 OID 16513)
-- Name: university_uniid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.university_uniid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.university_uniid_seq OWNER TO postgres;

--
-- TOC entry 3098 (class 0 OID 0)
-- Dependencies: 218
-- Name: university_uniid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.university_uniid_seq OWNED BY public.university.uni_id;


--
-- TOC entry 2917 (class 2604 OID 16515)
-- Name: group_run group_run_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.group_run ALTER COLUMN group_run_id SET DEFAULT nextval('public.group_run_group_run_id_seq'::regclass);


--
-- TOC entry 2919 (class 2604 OID 16516)
-- Name: run run_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.run ALTER COLUMN run_id SET DEFAULT nextval('public.run_runid_seq'::regclass);


--
-- TOC entry 2920 (class 2604 OID 16517)
-- Name: seed seed_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.seed ALTER COLUMN seed_id SET DEFAULT nextval('public.seed_seed_id_seq'::regclass);


--
-- TOC entry 2922 (class 2604 OID 16518)
-- Name: submission submission_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.submission ALTER COLUMN submission_id SET DEFAULT nextval('public.submission_submissionid_seq'::regclass);


--
-- TOC entry 2925 (class 2604 OID 16519)
-- Name: team_type team_type_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.team_type ALTER COLUMN team_type_id SET DEFAULT nextval('public.teamtype_teamtypeid_seq'::regclass);


--
-- TOC entry 2927 (class 2604 OID 16520)
-- Name: university uni_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.university ALTER COLUMN uni_id SET DEFAULT nextval('public.university_uniid_seq'::regclass);


--
-- TOC entry 2930 (class 2606 OID 16522)
-- Name: group_run group_run_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.group_run
    ADD CONSTRAINT group_run_pkey PRIMARY KEY (group_run_id);


--
-- TOC entry 2933 (class 2606 OID 16524)
-- Name: run run_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.run
    ADD CONSTRAINT run_pkey PRIMARY KEY (run_id);


--
-- TOC entry 2936 (class 2606 OID 16526)
-- Name: seed seed_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.seed
    ADD CONSTRAINT seed_pkey PRIMARY KEY (seed_id);


--
-- TOC entry 2938 (class 2606 OID 16528)
-- Name: submission submission_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.submission
    ADD CONSTRAINT submission_pkey PRIMARY KEY (submission_id);


--
-- TOC entry 2940 (class 2606 OID 16530)
-- Name: team team_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.team
    ADD CONSTRAINT team_pkey PRIMARY KEY (team_id);


--
-- TOC entry 2942 (class 2606 OID 16532)
-- Name: team team_teamname_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.team
    ADD CONSTRAINT team_teamname_key UNIQUE (team_name);


--
-- TOC entry 2944 (class 2606 OID 16534)
-- Name: team_type teamtype_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.team_type
    ADD CONSTRAINT teamtype_pkey PRIMARY KEY (team_type_id);


--
-- TOC entry 2946 (class 2606 OID 16536)
-- Name: university university_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.university
    ADD CONSTRAINT university_pkey PRIMARY KEY (uni_id);


--
-- TOC entry 2931 (class 1259 OID 16537)
-- Name: fki_fk_run_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX fki_fk_run_id ON public.logs USING btree (run_id);


--
-- TOC entry 2934 (class 1259 OID 16538)
-- Name: fki_group_run_id_fk; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX fki_group_run_id_fk ON public.seed USING btree (group_run_id);


--
-- TOC entry 2947 (class 2606 OID 16539)
-- Name: code_file codefile_submissionid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.code_file
    ADD CONSTRAINT codefile_submissionid_fkey FOREIGN KEY (submission_id) REFERENCES public.submission(submission_id) ON DELETE CASCADE;


--
-- TOC entry 2948 (class 2606 OID 16544)
-- Name: errors errors_run_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.errors
    ADD CONSTRAINT errors_run_id_fkey FOREIGN KEY (run_id) REFERENCES public.run(run_id) ON DELETE CASCADE;


--
-- TOC entry 2950 (class 2606 OID 16549)
-- Name: logs fk_group_run_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.logs
    ADD CONSTRAINT fk_group_run_id FOREIGN KEY (group_run_id) REFERENCES public.group_run(group_run_id) ON DELETE CASCADE;


--
-- TOC entry 2951 (class 2606 OID 16554)
-- Name: logs fk_run_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.logs
    ADD CONSTRAINT fk_run_id FOREIGN KEY (run_id) REFERENCES public.run(run_id) ON DELETE CASCADE;


--
-- TOC entry 2957 (class 2606 OID 16559)
-- Name: seed group_run_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.seed
    ADD CONSTRAINT group_run_id_fk FOREIGN KEY (group_run_id) REFERENCES public.group_run(group_run_id) ON DELETE CASCADE;


--
-- TOC entry 2955 (class 2606 OID 16649)
-- Name: run player_1_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.run
    ADD CONSTRAINT player_1_fk FOREIGN KEY (player_1) REFERENCES public.submission(submission_id) ON DELETE CASCADE;


--
-- TOC entry 2956 (class 2606 OID 16654)
-- Name: run player_2_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.run
    ADD CONSTRAINT player_2_fk FOREIGN KEY (player_2) REFERENCES public.submission(submission_id) ON DELETE CASCADE;


--
-- TOC entry 2952 (class 2606 OID 16564)
-- Name: run run_group_run_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.run
    ADD CONSTRAINT run_group_run_id_fkey FOREIGN KEY (group_run_id) REFERENCES public.group_run(group_run_id) ON DELETE CASCADE;


--
-- TOC entry 2953 (class 2606 OID 16574)
-- Name: run seed_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.run
    ADD CONSTRAINT seed_fk FOREIGN KEY (seed_id) REFERENCES public.seed(seed_id) ON DELETE CASCADE;


--
-- TOC entry 2949 (class 2606 OID 16794)
-- Name: errors subidfk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.errors
    ADD CONSTRAINT subidfk FOREIGN KEY (submission_id) REFERENCES public.submission(submission_id) ON DELETE CASCADE;


--
-- TOC entry 2958 (class 2606 OID 16579)
-- Name: submission submission_teamid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.submission
    ADD CONSTRAINT submission_teamid_fkey FOREIGN KEY (team_id) REFERENCES public.team(team_id) ON DELETE CASCADE;


--
-- TOC entry 2959 (class 2606 OID 16584)
-- Name: team team_teamtypeid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.team
    ADD CONSTRAINT team_teamtypeid_fkey FOREIGN KEY (team_type_id) REFERENCES public.team_type(team_type_id) ON DELETE CASCADE;


--
-- TOC entry 2960 (class 2606 OID 16589)
-- Name: team team_uniid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.team
    ADD CONSTRAINT team_uniid_fkey FOREIGN KEY (uni_id) REFERENCES public.university(uni_id) ON DELETE CASCADE;


--
-- TOC entry 2954 (class 2606 OID 16644)
-- Name: run winner_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.run
    ADD CONSTRAINT winner_fk FOREIGN KEY (winner) REFERENCES public.submission(submission_id) ON DELETE CASCADE;


-- Completed on 2022-01-18 19:16:01 CST

--
-- PostgreSQL database dump complete
--

