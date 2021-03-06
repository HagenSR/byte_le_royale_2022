PGDMP     ;                     z            byte-le-royale-2022-dev_play     12.9 (Ubuntu 12.9-2.pgdg20.04+1)     14.1 (Ubuntu 14.1-2.pgdg20.04+1) W               0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false                       0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false                       0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false                       1262    25022    byte-le-royale-2022-dev_play    DATABASE     ?   CREATE DATABASE "byte-le-royale-2022-dev_play" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE = 'en_US.UTF-8' TABLESPACE = fourtb;
 .   DROP DATABASE "byte-le-royale-2022-dev_play";
                byte_api    false                        3079    25023 	   uuid-ossp 	   EXTENSION     ?   CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA public;
    DROP EXTENSION "uuid-ossp";
                   false                       0    0    EXTENSION "uuid-ossp"    COMMENT     W   COMMENT ON EXTENSION "uuid-ossp" IS 'generate universally unique identifiers (UUIDs)';
                        false    2            ?            1255    25034 2   delete_group_run_and_foriegn_keys_cascade(integer)    FUNCTION     a  CREATE FUNCTION public.delete_group_run_and_foriegn_keys_cascade(grouprunid integer) RETURNS integer
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
 T   DROP FUNCTION public.delete_group_run_and_foriegn_keys_cascade(grouprunid integer);
       public          postgres    false            ?            1255    25035    fetch_latest_clients()    FUNCTION     ?  CREATE FUNCTION public.fetch_latest_clients() RETURNS TABLE(team_id uuid, submission_id integer, file_text character varying)
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
 -   DROP FUNCTION public.fetch_latest_clients();
       public          postgres    false            
           1255    25223 (   get_errors_for_submission(integer, uuid)    FUNCTION     &  CREATE FUNCTION public.get_errors_for_submission(submissionid integer, teamid uuid) RETURNS TABLE(run_id integer, submission_id integer, error_text character varying)
    LANGUAGE plpgsql
    AS $$
BEGIN
-- Created by: Sean Hagen
-- Written on: 1/1/2021
-- returns errors for a given submission
RETURN QUERY
SELECT DISTINCT
	errors.run_id,
	errors.submission_id,
	errors.error_text
FROM
	errors JOIN submission ON errors.submission_id = submission.submission_id
WHERE
    submission.team_id = teamid AND errors.submission_id = submissionid;
end;
$$;
 S   DROP FUNCTION public.get_errors_for_submission(submissionid integer, teamid uuid);
       public          postgres    false            ?            1255    25036 '   get_file_from_submission(uuid, integer)    FUNCTION     ?  CREATE FUNCTION public.get_file_from_submission(teamid uuid, submissionid integer) RETURNS character varying
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
 R   DROP FUNCTION public.get_file_from_submission(teamid uuid, submissionid integer);
       public          postgres    false            ?            1255    25037    get_group_run_details(integer)    FUNCTION     ?  CREATE FUNCTION public.get_group_run_details(groupid integer) RETURNS TABLE(group_run_id integer, start_run timestamp without time zone, runs_per_client integer, launcher_version character varying)
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
 =   DROP FUNCTION public.get_group_run_details(groupid integer);
       public          postgres    false            ?            1255    25038    get_group_runs(uuid)    FUNCTION     ?  CREATE FUNCTION public.get_group_runs(teamid uuid) RETURNS TABLE(group_run_id integer, run_time timestamp without time zone, launcher_version character varying, runs_per_client integer)
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
 2   DROP FUNCTION public.get_group_runs(teamid uuid);
       public          postgres    false            ?            1255    25039    get_latest_group_id()    FUNCTION       CREATE FUNCTION public.get_latest_group_id() RETURNS integer
    LANGUAGE plpgsql
    AS $$
BEGIN
-- Created by: Sean Hagen
-- Written on: 12/2/2021
-- Returns the latest group run id 
RETURN group_run.group_run_id FROM group_run ORDER BY group_run_id desc LIMIT 1;
end;
$$;
 ,   DROP FUNCTION public.get_latest_group_id();
       public          postgres    false            ?            1255    25040    get_latest_submission(uuid)    FUNCTION     ?  CREATE FUNCTION public.get_latest_submission(teamid uuid) RETURNS TABLE(submission_id integer, group_run_id integer, runs_per_client integer)
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
 9   DROP FUNCTION public.get_latest_submission(teamid uuid);
       public          postgres    false            ?            1255    25041 !   get_leaderboard(boolean, integer)    FUNCTION       CREATE FUNCTION public.get_leaderboard(include_inelligible boolean, grouprun integer) RETURNS TABLE(place bigint, team_name character varying, uni_name character varying, total_wins bigint)
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
        FROM (
                SELECT MAX(submission_id) as submission_id, team_id
                FROM submission
                GROUP BY team_id
                ORDER BY submission_id, team_id
            ) as sub_ids
            LEFT JOIN (
                SELECT winner,
                    COUNT(winner) as total_wins
                FROM run
                WHERE run.group_run_id = grouprun
                    and winner is not null
                group by winner
            ) as cnts ON cnts.winner = sub_ids.submission_id
            JOIN team on sub_ids.team_id = team.team_id
            JOIN team_type on team.team_type_id = team_type.team_type_id
            JOIN university on team.uni_id = university.uni_id
        WHERE (
                team_type.eligible
                OR include_inelligible
            )
    ) as infos;
end;
$$;
 U   DROP FUNCTION public.get_leaderboard(include_inelligible boolean, grouprun integer);
       public          postgres    false            ?            1255    25042    get_logs_for_group_run(integer)    FUNCTION     ?  CREATE FUNCTION public.get_logs_for_group_run(grouprun integer) RETURNS TABLE(run_id integer, group_run_id integer, submission_id integer, team_name character varying, log_text character varying)
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
    run.winner,
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
 ?   DROP FUNCTION public.get_logs_for_group_run(grouprun integer);
       public          postgres    false            ?            1255    25043    get_runs_for_group(integer)    FUNCTION       CREATE FUNCTION public.get_runs_for_group(groupid integer) RETURNS TABLE(group_run_id integer, run_id integer, run_time timestamp without time zone, winner character varying, player_1 character varying, player_2 character varying)
    LANGUAGE plpgsql
    AS $$
BEGIN
-- Created by: Sean Hagen
-- Written on: 12/30/2021
-- returns the runs for a given submission and group_run

RETURN QUERY

WITH team_to_submission AS (SELECT team_name, submission_id 
FROM submission 
JOIN team ON submission.team_id = team.team_id)

SELECT DISTINCT run.group_run_id, run.run_id, run.run_time, winn.team_name, player1.team_name, player2.team_name
FROM run JOIN submission 
ON run.player_1 = submission.submission_id OR run.player_2 = submission.submission_id
JOIN team_to_submission as winn on winn.submission_id = run.winner
JOIN team_to_submission as player1 on player1.submission_id = run.player_1
JOIN team_to_submission as player2 on player2.submission_id = run.player_2
WHERE run.group_run_id = groupid
ORDER BY run.run_time DESC;
end;
$$;
 :   DROP FUNCTION public.get_runs_for_group(groupid integer);
       public       
   byte_admin    false            ?            1255    25044 &   get_runs_for_submission(uuid, integer)    FUNCTION     C  CREATE FUNCTION public.get_runs_for_submission(teamid uuid, submissionid integer) RETURNS TABLE(run_id integer, group_run_id integer, run_time timestamp without time zone, winner character varying, player_1 character varying, player_2 character varying, seed_id integer, launcher_version character varying)
    LANGUAGE plpgsql
    AS $$
BEGIN
-- Created by: Sean Hagen
-- Written on: 12/30/2021
-- teamid: uuid to get runs for
-- submiddionid: submission id to get runs for
-- Returns the runs for a given team and submission
RETURN QUERY

WITH team_to_submission AS (SELECT team_name, submission_id 
FROM submission 
JOIN team ON submission.team_id = team.team_id)

SELECT DISTINCT run.run_id, run.group_run_id, run.run_time, winn.team_name, player1.team_name, player2.team_name, run.seed_id, group_run.launcher_version
FROM submission JOIN run ON submission.submission_id = run.player_1 OR submission.submission_id = run.player_2 
JOIN group_run on run.group_run_id = group_run.group_run_id
JOIN team_to_submission as winn on winn.submission_id = run.winner
JOIN team_to_submission as player1 on player1.submission_id = run.player_1
JOIN team_to_submission as player2 on player2.submission_id = run.player_2
WHERE submission.team_id = teamid AND submission.submission_id = submissionid
ORDER BY run.run_time DESC;
--SELECT * FROM team
end;
$$;
 Q   DROP FUNCTION public.get_runs_for_submission(teamid uuid, submissionid integer);
       public          postgres    false            ?            1255    25045 3   get_runs_for_submission_and_group(integer, integer)    FUNCTION     R  CREATE FUNCTION public.get_runs_for_submission_and_group(submissionid integer, groupid integer) RETURNS TABLE(group_run_id integer, run_id integer, run_time timestamp without time zone, winner character varying, player_1 character varying, player_2 character varying)
    LANGUAGE plpgsql
    AS $$
BEGIN
-- Created by: Sean Hagen
-- Written on: 12/30/2021
-- returns the runs for a given submission and group_run

RETURN QUERY

WITH team_to_submission AS (SELECT team_name, submission_id 
FROM submission 
JOIN team ON submission.team_id = team.team_id)

SELECT DISTINCT run.group_run_id, run.run_id, run.run_time, winn.team_name, player1.team_name, player2.team_name
FROM run JOIN submission 
ON run.player_1 = submission.submission_id OR run.player_2 = submission.submission_id
JOIN team_to_submission as winn on winn.submission_id = run.winner
JOIN team_to_submission as player1 on player1.submission_id = run.player_1
JOIN team_to_submission as player2 on player2.submission_id = run.player_2
WHERE (run.player_1 = submissionid or run.player_2 = submissionid) AND run.group_run_id = groupid;
end;
$$;
 _   DROP FUNCTION public.get_runs_for_submission_and_group(submissionid integer, groupid integer);
       public          postgres    false            ?            1255    25046    get_seed_for_run(uuid, integer)    FUNCTION       CREATE FUNCTION public.get_seed_for_run(teamid uuid, runid integer) RETURNS character varying
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
 C   DROP FUNCTION public.get_seed_for_run(teamid uuid, runid integer);
       public          postgres    false            ?            1255    25047    get_submissions_for_team(uuid)    FUNCTION     ?  CREATE FUNCTION public.get_submissions_for_team(teamid uuid) RETURNS TABLE(submission_id integer, submit_time timestamp without time zone)
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
 <   DROP FUNCTION public.get_submissions_for_team(teamid uuid);
       public          postgres    false            ?            1255    25048 *   get_team_runs_for_group_run(uuid, integer)    FUNCTION     ?  CREATE FUNCTION public.get_team_runs_for_group_run(teamid uuid, grouprunid integer) RETURNS TABLE(run_id integer, submission_run_id integer, winner character varying, player_1 character varying, player_2 character varying, run_time timestamp without time zone, seed_id integer, launcher_version character varying)
    LANGUAGE plpgsql
    AS $$
BEGIN
-- Created by: Sean Hagen
-- Written on: 12/30/2021
-- gets the runs for a given group run and team
RETURN QUERY

WITH team_to_submission AS (SELECT team_name, submission_id 
FROM submission 
JOIN team ON submission.team_id = team.team_id)

SELECT DISTINCT run.run_id, submission.submission_id, winn.team_name, player1.team_name, player2.team_name, 
run.run_time, run.seed_id, group_run.launcher_version
FROM submission 
JOIN run ON submission.submission_id = run.player_1 OR submission.submission_id = run.player_2  
JOIN group_run ON group_run.group_run_id = run.group_run_id
JOIN team_to_submission as winn on winn.submission_id = run.winner
JOIN team_to_submission as player1 on player1.submission_id = run.player_1
JOIN team_to_submission as player2 on player2.submission_id = run.player_2
WHERE submission.team_id = teamid AND run.group_run_id = grouprunid
ORDER BY run.run_time DESC;
end;
$$;
 S   DROP FUNCTION public.get_team_runs_for_group_run(teamid uuid, grouprunid integer);
       public          postgres    false                        1255    25049    get_team_score_over_time(uuid)    FUNCTION     ?  CREATE FUNCTION public.get_team_score_over_time(teamid uuid) RETURNS TABLE(group_run_id integer, place bigint, team_name character varying, start_run timestamp without time zone, total_wins bigint, launcher_version character varying)
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
 <   DROP FUNCTION public.get_team_score_over_time(teamid uuid);
       public          postgres    false                       1255    25050    get_team_types()    FUNCTION     C  CREATE FUNCTION public.get_team_types() RETURNS TABLE(team_type_id integer, team_type_name character varying)
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
 '   DROP FUNCTION public.get_team_types();
       public          postgres    false                       1255    25051    get_teams()    FUNCTION     ?  CREATE FUNCTION public.get_teams() RETURNS TABLE(team_name character varying, uni_name character varying, team_type_name character varying)
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
 "   DROP FUNCTION public.get_teams();
       public          postgres    false                       1255    25052    get_universities()    FUNCTION     ?   CREATE FUNCTION public.get_universities() RETURNS TABLE(uni_id integer, uni_name character varying)
    LANGUAGE plpgsql
    AS $$
BEGIN
-- Selects all universities
RETURN QUERY
SELECT university.uni_id, university.uni_name FROM university;
end;
$$;
 )   DROP FUNCTION public.get_universities();
       public          postgres    false                       1255    25224 1   insert_error(integer, integer, character varying)    FUNCTION     ?  CREATE FUNCTION public.insert_error(subid integer, runid integer, err character varying) RETURNS void
    LANGUAGE plpgsql
    AS $$
BEGIN
-- Created by: Sean Hagen
-- Written on: 12/15/2021
-- Inserts a error into the error table. Note the cascading delete effect that group run and run have on this table!
    INSERT INTO errors (submission_id, run_id, error_text) VALUES (subid, runid, err);
end;
$$;
 X   DROP FUNCTION public.insert_error(subid integer, runid integer, err character varying);
       public          postgres    false                       1255    25053 ,   insert_group_run(character varying, integer)    FUNCTION        CREATE FUNCTION public.insert_group_run(launcherversion character varying, runsperclient integer) RETURNS integer
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
 a   DROP FUNCTION public.insert_group_run(launcherversion character varying, runsperclient integer);
       public          byte_api    false                       1255    25054 /   insert_log(character varying, integer, integer)    FUNCTION     ?  CREATE FUNCTION public.insert_log(logfl character varying, runid integer, grouprunid integer) RETURNS void
    LANGUAGE plpgsql
    AS $$
BEGIN
-- Created by: Sean Hagen
-- Written on: 12/15/2021
-- Inserts a log into the log table. Note the cascading delete effect that group run and run have on this table!
    INSERT INTO logs (log_text, run_id, group_run_id) VALUES (logfl, runid, groupRunId);
end;
$$;
 ]   DROP FUNCTION public.insert_log(logfl character varying, runid integer, grouprunid integer);
       public          postgres    false                       1255    25225 .   insert_run(integer, integer, integer, integer)    FUNCTION     t  CREATE FUNCTION public.insert_run(sub_id integer, score integer, group_run_id integer, seedid integer) RETURNS integer
    LANGUAGE plpgsql
    AS $$
DECLARE runid int;
begin
    -- insert run into run table
	INSERT INTO run(submission_id, score, group_run_id, seed_id) 
	VALUES (sub_id, score, group_run_id, seedid) RETURNING run_id INTO runid;
	
	return runid;
end;
$$;
 f   DROP FUNCTION public.insert_run(sub_id integer, score integer, group_run_id integer, seedid integer);
       public       
   byte_admin    false                       1255    25226 7   insert_run(integer, integer, integer, integer, integer)    FUNCTION     ?  CREATE FUNCTION public.insert_run(winn integer, player1 integer, player2 integer, grouprunid integer, seedid integer) RETURNS integer
    LANGUAGE plpgsql
    AS $$
DECLARE runid int;
begin
    -- insert run into run table
	INSERT INTO run(winner, player_1, player_2, group_run_id, seed_id)
	VALUES (nullif(winn, -1), player1, player2, grouprunid, seedid) RETURNING run_id INTO runid;
	
	return runid;
end;
$$;
 u   DROP FUNCTION public.insert_run(winn integer, player1 integer, player2 integer, grouprunid integer, seedid integer);
       public       
   byte_admin    false                       1255    25056 J   insert_run(integer, integer, integer, integer, character varying, integer)    FUNCTION     ?  CREATE FUNCTION public.insert_run(winn integer, player1 integer, player2 integer, grouprunid integer, err character varying, seedid integer) RETURNS integer
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
 ?   DROP FUNCTION public.insert_run(winn integer, player1 integer, player2 integer, grouprunid integer, err character varying, seedid integer);
       public          byte_api    false                       1255    25057 '   insert_seed(character varying, integer)    FUNCTION     ?  CREATE FUNCTION public.insert_seed(seedfl character varying, grouprunid integer) RETURNS integer
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
 P   DROP FUNCTION public.insert_seed(seedfl character varying, grouprunid integer);
       public          postgres    false                       1255    25058 0   insert_team(integer, character varying, integer)    FUNCTION     ?  CREATE FUNCTION public.insert_team(team_type integer, team character varying, uni integer) RETURNS uuid
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
 Z   DROP FUNCTION public.insert_team(team_type integer, team character varying, uni integer);
       public          postgres    false            	           1255    25059 )   submit_code_file(character varying, uuid) 	   PROCEDURE     ?  CREATE PROCEDURE public.submit_code_file(file character varying, vid uuid)
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
 J   DROP PROCEDURE public.submit_code_file(file character varying, vid uuid);
       public          postgres    false            ?            1259    25060 	   code_file    TABLE     ^   CREATE TABLE public.code_file (
    submission_id integer,
    file_text character varying
);
    DROP TABLE public.code_file;
       public         heap    postgres    false            ?            1259    25066    errors    TABLE     p   CREATE TABLE public.errors (
    run_id integer,
    error_text character varying,
    submission_id integer
);
    DROP TABLE public.errors;
       public         heap    postgres    false            ?            1259    25072 	   group_run    TABLE     ?   CREATE TABLE public.group_run (
    group_run_id integer NOT NULL,
    start_run timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    launcher_version character varying(10) NOT NULL,
    runs_per_client integer
);
    DROP TABLE public.group_run;
       public         heap    postgres    false            ?            1259    25076    group_run_group_run_id_seq    SEQUENCE     ?   CREATE SEQUENCE public.group_run_group_run_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 1   DROP SEQUENCE public.group_run_group_run_id_seq;
       public          postgres    false    205                       0    0    group_run_group_run_id_seq    SEQUENCE OWNED BY     Y   ALTER SEQUENCE public.group_run_group_run_id_seq OWNED BY public.group_run.group_run_id;
          public          postgres    false    206            ?            1259    25078    logs    TABLE     k   CREATE TABLE public.logs (
    run_id integer,
    log_text character varying,
    group_run_id integer
);
    DROP TABLE public.logs;
       public         heap    postgres    false            ?            1259    25084    run    TABLE     ?   CREATE TABLE public.run (
    run_id integer NOT NULL,
    group_run_id integer,
    run_time timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    seed_id integer,
    winner integer,
    player_1 integer,
    player_2 integer
);
    DROP TABLE public.run;
       public         heap    postgres    false            ?            1259    25088    run_runid_seq    SEQUENCE     ?   CREATE SEQUENCE public.run_runid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 $   DROP SEQUENCE public.run_runid_seq;
       public          postgres    false    208                       0    0    run_runid_seq    SEQUENCE OWNED BY     @   ALTER SEQUENCE public.run_runid_seq OWNED BY public.run.run_id;
          public          postgres    false    209            ?            1259    25090    seed    TABLE     q   CREATE TABLE public.seed (
    seed_id integer NOT NULL,
    seed character varying,
    group_run_id integer
);
    DROP TABLE public.seed;
       public         heap    postgres    false            ?            1259    25096    seed_seed_id_seq    SEQUENCE     ?   CREATE SEQUENCE public.seed_seed_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 '   DROP SEQUENCE public.seed_seed_id_seq;
       public          postgres    false    210                       0    0    seed_seed_id_seq    SEQUENCE OWNED BY     E   ALTER SEQUENCE public.seed_seed_id_seq OWNED BY public.seed.seed_id;
          public          postgres    false    211            ?            1259    25098 
   submission    TABLE     ?   CREATE TABLE public.submission (
    team_id uuid,
    submission_id integer NOT NULL,
    submit_time timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);
    DROP TABLE public.submission;
       public         heap    postgres    false            ?            1259    25102    submission_submissionid_seq    SEQUENCE     ?   CREATE SEQUENCE public.submission_submissionid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 2   DROP SEQUENCE public.submission_submissionid_seq;
       public          postgres    false    212                       0    0    submission_submissionid_seq    SEQUENCE OWNED BY     \   ALTER SEQUENCE public.submission_submissionid_seq OWNED BY public.submission.submission_id;
          public          postgres    false    213            ?            1259    25104    team    TABLE       CREATE TABLE public.team (
    team_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    uni_id integer,
    team_type_id integer,
    team_name character varying(100) NOT NULL,
    CONSTRAINT team_teamname_check CHECK (((team_name)::text <> ''::text))
);
    DROP TABLE public.team;
       public         heap    postgres    false    2            ?            1259    25109 	   team_type    TABLE     ?   CREATE TABLE public.team_type (
    team_type_id integer NOT NULL,
    team_type_name character varying(100) NOT NULL,
    eligible boolean,
    CONSTRAINT teamtype_teamname_check CHECK (((team_type_name)::text <> ''::text))
);
    DROP TABLE public.team_type;
       public         heap    postgres    false            ?            1259    25113    teamtype_teamtypeid_seq    SEQUENCE     ?   CREATE SEQUENCE public.teamtype_teamtypeid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 .   DROP SEQUENCE public.teamtype_teamtypeid_seq;
       public          postgres    false    215                       0    0    teamtype_teamtypeid_seq    SEQUENCE OWNED BY     V   ALTER SEQUENCE public.teamtype_teamtypeid_seq OWNED BY public.team_type.team_type_id;
          public          postgres    false    216            ?            1259    25115 
   university    TABLE     ?   CREATE TABLE public.university (
    uni_id integer NOT NULL,
    uni_name character varying(100) NOT NULL,
    CONSTRAINT university_uniname_check CHECK (((uni_name)::text <> ''::text))
);
    DROP TABLE public.university;
       public         heap    postgres    false            ?            1259    25119    university_uniid_seq    SEQUENCE     ?   CREATE SEQUENCE public.university_uniid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 +   DROP SEQUENCE public.university_uniid_seq;
       public          postgres    false    217                       0    0    university_uniid_seq    SEQUENCE OWNED BY     N   ALTER SEQUENCE public.university_uniid_seq OWNED BY public.university.uni_id;
          public          postgres    false    218            i           2604    25121    group_run group_run_id    DEFAULT     ?   ALTER TABLE ONLY public.group_run ALTER COLUMN group_run_id SET DEFAULT nextval('public.group_run_group_run_id_seq'::regclass);
 E   ALTER TABLE public.group_run ALTER COLUMN group_run_id DROP DEFAULT;
       public          postgres    false    206    205            k           2604    25122 
   run run_id    DEFAULT     g   ALTER TABLE ONLY public.run ALTER COLUMN run_id SET DEFAULT nextval('public.run_runid_seq'::regclass);
 9   ALTER TABLE public.run ALTER COLUMN run_id DROP DEFAULT;
       public          postgres    false    209    208            l           2604    25123    seed seed_id    DEFAULT     l   ALTER TABLE ONLY public.seed ALTER COLUMN seed_id SET DEFAULT nextval('public.seed_seed_id_seq'::regclass);
 ;   ALTER TABLE public.seed ALTER COLUMN seed_id DROP DEFAULT;
       public          postgres    false    211    210            n           2604    25124    submission submission_id    DEFAULT     ?   ALTER TABLE ONLY public.submission ALTER COLUMN submission_id SET DEFAULT nextval('public.submission_submissionid_seq'::regclass);
 G   ALTER TABLE public.submission ALTER COLUMN submission_id DROP DEFAULT;
       public          postgres    false    213    212            q           2604    25125    team_type team_type_id    DEFAULT     }   ALTER TABLE ONLY public.team_type ALTER COLUMN team_type_id SET DEFAULT nextval('public.teamtype_teamtypeid_seq'::regclass);
 E   ALTER TABLE public.team_type ALTER COLUMN team_type_id DROP DEFAULT;
       public          postgres    false    216    215            s           2604    25126    university uni_id    DEFAULT     u   ALTER TABLE ONLY public.university ALTER COLUMN uni_id SET DEFAULT nextval('public.university_uniid_seq'::regclass);
 @   ALTER TABLE public.university ALTER COLUMN uni_id DROP DEFAULT;
       public          postgres    false    218    217            v           2606    25128    group_run group_run_pkey 
   CONSTRAINT     `   ALTER TABLE ONLY public.group_run
    ADD CONSTRAINT group_run_pkey PRIMARY KEY (group_run_id);
 B   ALTER TABLE ONLY public.group_run DROP CONSTRAINT group_run_pkey;
       public            postgres    false    205            y           2606    25130    run run_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.run
    ADD CONSTRAINT run_pkey PRIMARY KEY (run_id);
 6   ALTER TABLE ONLY public.run DROP CONSTRAINT run_pkey;
       public            postgres    false    208            |           2606    25132    seed seed_pkey 
   CONSTRAINT     Q   ALTER TABLE ONLY public.seed
    ADD CONSTRAINT seed_pkey PRIMARY KEY (seed_id);
 8   ALTER TABLE ONLY public.seed DROP CONSTRAINT seed_pkey;
       public            postgres    false    210            ~           2606    25134    submission submission_pkey 
   CONSTRAINT     c   ALTER TABLE ONLY public.submission
    ADD CONSTRAINT submission_pkey PRIMARY KEY (submission_id);
 D   ALTER TABLE ONLY public.submission DROP CONSTRAINT submission_pkey;
       public            postgres    false    212            ?           2606    25136    team team_pkey 
   CONSTRAINT     Q   ALTER TABLE ONLY public.team
    ADD CONSTRAINT team_pkey PRIMARY KEY (team_id);
 8   ALTER TABLE ONLY public.team DROP CONSTRAINT team_pkey;
       public            postgres    false    214            ?           2606    25138    team team_teamname_key 
   CONSTRAINT     V   ALTER TABLE ONLY public.team
    ADD CONSTRAINT team_teamname_key UNIQUE (team_name);
 @   ALTER TABLE ONLY public.team DROP CONSTRAINT team_teamname_key;
       public            postgres    false    214            ?           2606    25140    team_type teamtype_pkey 
   CONSTRAINT     _   ALTER TABLE ONLY public.team_type
    ADD CONSTRAINT teamtype_pkey PRIMARY KEY (team_type_id);
 A   ALTER TABLE ONLY public.team_type DROP CONSTRAINT teamtype_pkey;
       public            postgres    false    215            ?           2606    25142    university university_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.university
    ADD CONSTRAINT university_pkey PRIMARY KEY (uni_id);
 D   ALTER TABLE ONLY public.university DROP CONSTRAINT university_pkey;
       public            postgres    false    217            w           1259    25143    fki_fk_run_id    INDEX     @   CREATE INDEX fki_fk_run_id ON public.logs USING btree (run_id);
 !   DROP INDEX public.fki_fk_run_id;
       public            postgres    false    207            z           1259    25144    fki_group_run_id_fk    INDEX     L   CREATE INDEX fki_group_run_id_fk ON public.seed USING btree (group_run_id);
 '   DROP INDEX public.fki_group_run_id_fk;
       public            postgres    false    210            ?           2606    25145 $   code_file codefile_submissionid_fkey    FK CONSTRAINT     ?   ALTER TABLE ONLY public.code_file
    ADD CONSTRAINT codefile_submissionid_fkey FOREIGN KEY (submission_id) REFERENCES public.submission(submission_id) ON DELETE CASCADE;
 N   ALTER TABLE ONLY public.code_file DROP CONSTRAINT codefile_submissionid_fkey;
       public          postgres    false    212    203    2942            ?           2606    25150    errors errors_run_id_fkey    FK CONSTRAINT     ?   ALTER TABLE ONLY public.errors
    ADD CONSTRAINT errors_run_id_fkey FOREIGN KEY (run_id) REFERENCES public.run(run_id) ON DELETE CASCADE;
 C   ALTER TABLE ONLY public.errors DROP CONSTRAINT errors_run_id_fkey;
       public          postgres    false    208    204    2937            ?           2606    25155    logs fk_group_run_id    FK CONSTRAINT     ?   ALTER TABLE ONLY public.logs
    ADD CONSTRAINT fk_group_run_id FOREIGN KEY (group_run_id) REFERENCES public.group_run(group_run_id) ON DELETE CASCADE;
 >   ALTER TABLE ONLY public.logs DROP CONSTRAINT fk_group_run_id;
       public          postgres    false    207    2934    205            ?           2606    25160    logs fk_run_id    FK CONSTRAINT     ?   ALTER TABLE ONLY public.logs
    ADD CONSTRAINT fk_run_id FOREIGN KEY (run_id) REFERENCES public.run(run_id) ON DELETE CASCADE;
 8   ALTER TABLE ONLY public.logs DROP CONSTRAINT fk_run_id;
       public          postgres    false    208    2937    207            ?           2606    25165    seed group_run_id_fk    FK CONSTRAINT     ?   ALTER TABLE ONLY public.seed
    ADD CONSTRAINT group_run_id_fk FOREIGN KEY (group_run_id) REFERENCES public.group_run(group_run_id) ON DELETE CASCADE;
 >   ALTER TABLE ONLY public.seed DROP CONSTRAINT group_run_id_fk;
       public          postgres    false    205    210    2934            ?           2606    25170    run player_1_fk    FK CONSTRAINT     ?   ALTER TABLE ONLY public.run
    ADD CONSTRAINT player_1_fk FOREIGN KEY (player_1) REFERENCES public.submission(submission_id) ON DELETE CASCADE;
 9   ALTER TABLE ONLY public.run DROP CONSTRAINT player_1_fk;
       public          postgres    false    2942    208    212            ?           2606    25175    run player_2_fk    FK CONSTRAINT     ?   ALTER TABLE ONLY public.run
    ADD CONSTRAINT player_2_fk FOREIGN KEY (player_2) REFERENCES public.submission(submission_id) ON DELETE CASCADE;
 9   ALTER TABLE ONLY public.run DROP CONSTRAINT player_2_fk;
       public          postgres    false    212    208    2942            ?           2606    25180    run run_group_run_id_fkey    FK CONSTRAINT     ?   ALTER TABLE ONLY public.run
    ADD CONSTRAINT run_group_run_id_fkey FOREIGN KEY (group_run_id) REFERENCES public.group_run(group_run_id) ON DELETE CASCADE;
 C   ALTER TABLE ONLY public.run DROP CONSTRAINT run_group_run_id_fkey;
       public          postgres    false    2934    208    205            ?           2606    25185    run seed_fk    FK CONSTRAINT     ?   ALTER TABLE ONLY public.run
    ADD CONSTRAINT seed_fk FOREIGN KEY (seed_id) REFERENCES public.seed(seed_id) ON DELETE CASCADE;
 5   ALTER TABLE ONLY public.run DROP CONSTRAINT seed_fk;
       public          postgres    false    2940    208    210            ?           2606    25190    errors subidfk    FK CONSTRAINT     ?   ALTER TABLE ONLY public.errors
    ADD CONSTRAINT subidfk FOREIGN KEY (submission_id) REFERENCES public.submission(submission_id) ON DELETE CASCADE;
 8   ALTER TABLE ONLY public.errors DROP CONSTRAINT subidfk;
       public          postgres    false    212    204    2942            ?           2606    25195 !   submission submission_teamid_fkey    FK CONSTRAINT     ?   ALTER TABLE ONLY public.submission
    ADD CONSTRAINT submission_teamid_fkey FOREIGN KEY (team_id) REFERENCES public.team(team_id) ON DELETE CASCADE;
 K   ALTER TABLE ONLY public.submission DROP CONSTRAINT submission_teamid_fkey;
       public          postgres    false    2944    212    214            ?           2606    25200    team team_teamtypeid_fkey    FK CONSTRAINT     ?   ALTER TABLE ONLY public.team
    ADD CONSTRAINT team_teamtypeid_fkey FOREIGN KEY (team_type_id) REFERENCES public.team_type(team_type_id) ON DELETE CASCADE;
 C   ALTER TABLE ONLY public.team DROP CONSTRAINT team_teamtypeid_fkey;
       public          postgres    false    214    215    2948            ?           2606    25205    team team_uniid_fkey    FK CONSTRAINT     ?   ALTER TABLE ONLY public.team
    ADD CONSTRAINT team_uniid_fkey FOREIGN KEY (uni_id) REFERENCES public.university(uni_id) ON DELETE CASCADE;
 >   ALTER TABLE ONLY public.team DROP CONSTRAINT team_uniid_fkey;
       public          postgres    false    2950    214    217            ?           2606    25210    run winner_fk    FK CONSTRAINT     ?   ALTER TABLE ONLY public.run
    ADD CONSTRAINT winner_fk FOREIGN KEY (winner) REFERENCES public.submission(submission_id) ON DELETE CASCADE;
 7   ALTER TABLE ONLY public.run DROP CONSTRAINT winner_fk;
       public          postgres    false    208    2942    212           