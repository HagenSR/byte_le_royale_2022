===================
Running the game
===================

Installing
==========

Make sure to uninstall the visual studio version of python if you have visual studio installed. 
You can do this by re-running the installer and unselecting the python development kit then clicking update.

We recommend running a python version between 3.8.10 and 3.9.9

You can use any text editor for this competition, but we recommend visual studio code.


Running the game
================

Building the launcher
---------------------

NOTE: There are some packages requires for running this year's game. You can run the command 

.. code-block:: console

    python -m pip install -r requirements.txt

(To view the packages to be installed, simply open the requirements.txt file)


Generating the map
------------------

You can generate a new game map by calling

.. code-block:: python

    python launcher.pyz g

within a terminal in the byte-le folder. You can keep the same game map by just not running the above command.


Running the game
-----------------

You can run the bot by calling

.. code-block:: python

    python launcher.pyz r

within the terminal. Print statements within your client will print if you wish to use them for debugging purposes. Alternatively, you can view
the turn logs that are produced within the logs folder.


Running the visualizer
----------------------

As a third option for debugging, we have built a visualizer! The visualizer visually depicts the logs that are produced, so you can more easily decipher what went wrong. 
The visualizer can be run with

.. code-block:: python

    python launcher.pyz v


Improving the bot
-----------------

All improvements should be made within the client. We provide a base client but you are welcome to rename the file or create multiple client files. 
Note that if you make multiple files, there can only be two client in the root folder. Place the other clients in the test_clients folder. Make sure to check the
documentation for hints on how to improve!


Scrimmage!
==========

The actual competition occurs on the server! View the server documentation for more info.