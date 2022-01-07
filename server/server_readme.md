# BYTE LE ROYALE SERVER

## General Setup and overview

This byte-le royale server consists of four parts

1. Postgres SQL database
2. Submission Runner
3. Visualizer Runner
4. Python Flask API
5. Python Client

The general process is as follows
1. Teams submit clients through the Python client
2. the Client posts the files to the API, which checks for validity and illegal keywords
3. API stores the files in the submission and code file table
4. Submission Runner, which runs every X minutes, creates a new group run
5. Submission Runner gathers the latest submissions from the submission and code tables, runs them against eachother
6. Each run is is inserted in to the run table, with the results and group run id
7. Process finishes, Teams get results through API, which calls the associated function/stored procedures
8. Visualizer runner fetches best logs from each team, and shows them. Repeats once all are finished playing and not for every group run
8. Process repeats

Please note that not all of the functionality needs to be implemented. Only what you want to!

Which will be covered in the following sections.

## Really Important things to note:
1. For the API to reflect changes made to Postgresql Functions, tables, schemas etc it needs to be restarted

## Postgres SQL Database

### Set up

#### PLEASE NOTE

The Postgres SQL database has creation scripts to facilitate the simple creation of a new database. 

1. Create a new database using PGAdmin, 
    1. Log into PG Admin on ACM left Ubuntu. Password is available in the ACM credentials file on the google drive 
    2. create a database under the byte-le-royale group.
    3. be sure to select set tablespace = fourtb. fourtb is the 4 terrabyte partition. If this isn't available, see https://stackoverflow.com/questions/9876132/postgresql-creating-database-in-a-specified-location/9876229
    4. If you've really screwed up, you can reformat the 4tb disk, set it to auto-mount in the disks application, and then recreate the DB space
2. copy, paste and run the dump.sql file in the query tool. This will create all of the tables and stored procedures
3. copy, paste and run the small_data_insert.sql file, this will insert basic data you need.
4. Modify the database schema as needed
    2. The stored procedures / functions will also need to change. Notably insert_run, get_leaderboard, get_stats_for_submission, get_team_score_over_time

#### ALSO NOTE

1. All foriegn keys in the database have a cascading delete effect. That means when you delete a row (like a group_run row) then all rows that reference it will be deleted (run) and then in turn those rows will have a cascading delete effect (logs, errors, seed). This is to help remove invalid data, as the client_runner will delete any group runs that fail to complete.
2. PGadmin is very useful, Use It!
3. Primary keys are serial and will be generated automatically. Same with timestamps

### Overview of tables

Please note that Postgres has a ERD diagram tool. Right click the database -> Generate ERD. This will be helpful!

#### University
##### uni_id int, uni_name
Just a table of university names and primary keys

#### Team_Type
##### team_type_id int, team_type_name varchar, eligible bool
Team type is given to the team table so we can determine who can win prizes. eligible is if they are eligible to win prizes.

#### team
##### team_id uuid, team_name varchar, FK uni_id int, FK team_type_id int
Team table for storing teams. Note that team_id is a UUID which corresponds to the clients VID

#### submission
##### FK team_id uuid, PK submission_id, submit_time timestamp
A submission table, inserts occur every time a team uploads a code file through the client.

#### code_file
##### FK submission_id int, file_text varchar
This is where python code files are stored. (This is a valid way to do it, as Postgres will store it as a file anyway https://newbedev.com/are-there-performance-issues-storing-files-in-postgresql)

#### group_run
##### PK group_run_id int, start_run timestamp, launcher_version varchar(10), runs_per_client int
Group run is a table that groups runs together. The launcher version is useful for determining what version of a launcher a run ran on (duh). Runs_per_client is how many time the client_runner script runs a code_file (also how many seeds are generated per group run)

#### run
##### FK submission_id int, PK run_id int, score int, FK group_run_id int, run_time timestamp, FK seed_id int
A run table, for storing each run of a game. Runs that occured together have the same group_run_id. seed_id is is FK for the seed that the run used


#### logs
##### FK run_id, log_text varchar, group_run_id FK
Table to store game logs for a given run, if you desire. group_run_id is used to ensure the cascading delete also deletes logs for a group_run.
Note that logs should be a stringified JSON dict, where each key is a file name and the value is the files contents.

#### errors
##### FK run_id int, error_text varchar
Error table for storing errors that may have occured for each run, if desired. 

#### seed
##### PK seed_id int, seed varchar, group_run_id FK
The seed that a given run used. To save space, N seeds ( as determined by group_run.runs_per_client) will be generated for each group run, with each client being run against the seed. group_run_id ensures the cascading delete will delete the seeds associated with a group run when it's deleted.

### BACK UP DATABASE SCHEMA
To back up the database schema you've altered
1. Right click database
2. Select the dump.sql file in db_dump 
3. Select Format plain
4. Go to Dump Options -> select only schema
5. Click Go


## CLIENT RUNNER

The client runner fetches programs from the database, runs them, and stores their results in the database. 

If the client runner is interupted, the results will be removed from the database by deleted the associated group run, which will delete all associated information through a cascading delete (HOW MANY TIMES DO I NEED TO TYPE CASCADING DELETE. THE DELETES CASCADE OKAY)

Note that a run will be inserted for failed runs with a score of zero.

### SET UP

set up for the client runner is pretty simple

1. Allow "executing files as a program" for all files in the runner folder
2. Change database credentials
3. Change line 121 so the game gets the correct score from the logs

run the program! fix any errors that occur

### UPDATING CLIENT RUNNER

When you make changes to the game during the course of the competition, you must update the client runner!

1. stop the client runner
2. run python3 launcher.pyz update
3. run ./build.sh or ./build.bat
4. start the client runner

That's it!

### See other options

There are other options you can change within the client runner, such as which logs are saved and if errors are saved. Also see the constants such as the time between runs.


## API

The API is a python Flask API. It uses HTTPS, rate limiting, logging, error recover, verbose responses (TLDR it's poggers)

Note that type checking isn't necessary, as SQL functions have very verbose, explicit type checking and will throw errors when they get the wrong type.

### Run Locally
To run the flask server locally for testing, First set the enviroment variable by running

Linux: export FLASK_APP=Server

Windows Powershell: $env:FLASK_APP = "Server"

Then the command flask run --cert=adhoc

### Run Production

To run for production, you first need to create SSL certificates. On Ubuntu, run the following command in the certs folder

openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 5

Then to run the server on Gunicorn, run the command

gunicorn --certfile certs/cert.pem --keyfile certs/key.pem -b 134.129.91.223:8000 Server:app -w 1 --threads 12

### Endpoints

The following endpoints exist on the API. Most are somewhat self explanitory. Note that 'get' doesn't refer to the HTTP action but the action of "getting" something.

#### /api/get_unis
#### body: none
Returns the universities a player can be from or N/A. 

#### /api/get_team_types
#### body: none
Gets the types of teams a player can be.

#### /api/get_teams
#### body: none
Get all of the teams registered

#### /api/register
#### body: type int, name string, uni int
Registers a team for playing. type and uni are the PK ids for the respective tables. returns a VID for the player to save.

#### /api/submit
#### body: file int, vid string
Submits a file into the submission and file tables. note that it checks for illegal words and undue file sizes.

#### /api/get_leaderboard
#### body: include_inelligible bool, group_id int
Returns the leaderboard. if include_inelligible is true, alumni and other will be included. If group_id isn't =1, the leaderboard for the given group_id will be returned.

#### /api/get_submission_stats
#### body: vid string
Returns stats for the latest group_run, including the total number of runs and details of runs that have already gone.

#### /api/get_team_score_over_time
#### body: vid string
Returns the score that the team had in each group_run

#### /api/get_submissions_for_team
#### body: vid string
Returns all of the submissions a team has participated in.

#### /api/get_group_runs
#### body: vid string
Returns all of the group runs a team has participated in

#### /api/get_team_runs_for_group_run
#### body: vid string, groupid int
Returns all of runs for a team in a group run

#### /api/get_runs_for_submission
#### body: vid string, submissionid int
Returns all of the runs that a team's submission had.

#### /api/get_file_from_submission
#### body: vid string, submissionid int
Returns the asscosiated code file from a submission

#### /api/get_seed_from_run
#### body: vid string, runid int
Returns the seed that a run was ran with

