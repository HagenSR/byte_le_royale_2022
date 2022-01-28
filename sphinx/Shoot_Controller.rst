====================
Shoot Controller
====================


Lore
-----

The Armed Forces of the United States of Planetary Monetization was once a thriving
society. Protected by their superior military prowess, they survived for millenia.
Then the SIG's attacked. They were vicious and sudden, there was no safety,
nor remorse. College students of the United States of Planetary Monetization were
given the harshest punishments of them all.
Tasked with developing a system of highly technical weaponry to fully surpass that
of the United States of Planetary Monetization they were building the very weapons
that would keep themselves, their children, and kin subjugated for eternity.
Doomed to a life in debt to SIG'S.
The technology developed by these college students are now to be utilized by YOU
in the fight against the SIG's and it is your task to participate.

Basic Info
----------

The shoot controller handles how the player shoots, in other words, ray logic. When a player shoots it instantaneously sends a ray (or rays in the case of a gun shooting multiple times in a single shot) damaging whatever the rays come into contact with.
**If a player has a shield, it absorbs the damage of a single bullet.**
A gun has three types of shooting types. Single shot, where the user fires a single ray. Multi-shot where the user fires a quick succession of rays. The final type is spread, which acts like a shotgun.

Code
----

.. code-block:: python

    actions.set_shoot(heading = int(90))

Will shoot southwards




