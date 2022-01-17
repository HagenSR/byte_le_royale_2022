======================
Server Documentation
======================

Important Info!
================

There is a new server this year and it improves on the previous server in two major ways

1. More information is stored and kept in the database
2. You can access this information through the client

This functionality is optional, and the below section highlights the commands you need to know

Group runs
------------

Unlike previous years, clients will be run together at a distinct point in time, known as a group run. The 
benefit to group runs is that you can fetch information relating to each group run (such as launcher version!)
and view your progress (or regression) over time!

The downside is that there is no "queue" like previous years, and you have to wait for the group run to complete 
before your next client is run. 

Other cool features
---------------------

1. HTTPS!
2. Rate Limiting!
3. Seed downloading!
4. Client Downloading!
5. idk i forgor sql is kinda pog


The Important commands that you need to know!
================================================

Registering
------------

Registering is required to recieve your VID ( Don't share with anyone!) which in turn allows you to submit clients and view 
team specific information. If your teamates wish to upload to the server, you'll have to send them the vID.

.. code-block:: python

    python launcher.pyz client -register

you will then be prompted to enter information


submiting clients
--------------------

.. code-block:: python

    python launcher.pyz client -submit

Once you've registered, you can submit your client. At least one client must be submitted by midnight to be elligible to win. The server will automatically look for files in the 
root directory that contain the word 'client'. Otherwise, you can manually select the file. Once you've confirmed the file, it will be uploaded to the server and 
then run against other clients to determine placing. Feel free to submit as many times as you like, but please refrain from excessive uploads.

leaderboard
--------------

.. code-block:: python

    python launcher.pyz client leaderboard

Returns the leaderboard for elligible contestants. Alumni will want to run the command

.. code-block:: python

    python launcher.pyz client leaderboard -include_alumni

Also note you can retrieve the leaderboard for previous group runs using

.. code-block:: python

    python launcher.pyz client leaderboard -group_id <group_run_id>


view stats
------------

.. code-block:: python

    python launcher.pyz client stats

Returns stats relating to your submissions(s). All stats relate to your most recent submission. Please note that the stats will continue to change until all 
runs are completed.


Other Fun Commands!
=====================

runs for group run
-------------------

.. code-block:: python

    python launcher.pyz client stats -runs_for_group_run <group_id>

Returns all of the runs for a given group run






