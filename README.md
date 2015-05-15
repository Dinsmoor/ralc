###########
RALC README
###########

Prog V: 0.6.0a
Doc  V: 0.6.0a

=====
INTRO
=====
	R.A.L.C is an acronymn for Randomized Adventure Lore Creator, it is the
	combined effort of freedom-loving DND nerds to be collectively
	lazier by means of effort.

=====
SCREENSHOTS:
=====
![](http://s3.postimg.org/7weqiw5pv/Screenshot_from_2015_05_14_12_49_26.png)

=======
PURPOSE
=======
	The aim of this project is to adhere as close to the DNDv5 book as
	possible, whilst remaining flexible, extensible, modifiable,
	configurable, portable, and modular in nature. It is, and will remain
	cross-platform free software.

=
DEPENDANCIES
=
	python2.7
	python-tk
	python-imaging
	python-imaging-tk


=============
SPECIFICATIONS
=============
SHALL:
-----
	= Project:
		- Adhere to purpose.
		- Make sense
		- Be useful
	= Code:
		- Be written neatly
		- Be planned
		- Be well-documented
		- Use Tabs
		- Be portable

SHOULD:
-----
	= Project:
		- Consult DND players for ideas
	= Code:
		- Utilize online resources
		- Be passable to other programs
		- Be used as an example for a learning aide
NEVER:
-----
	= Project:
		- Assume what the user wants
	= Code:
		- Be unnecicarially repeatative
		- Forget to use expressions



========
TIMELINE
========
'''
This is the timeline of development:
'''

DONE- First release, must ouput basic character and area information.
		Design the flow of information, and requirements.
		Planning/Framework stage.

DONE- Proper spell slot assignment, Biography/Background, Skills, and
		equipment assignment for charGen. Add no-class class. Create
		currency system, valuable items must have cost.

DONE- areaGen will be rewritten, will output useful statistics about the
		environment, for later use with townGen, but in the meantime produce
		basic descriptions of an area.

INPRO- A GUI will be written to interface with charGen and areaGen, and
		display their data as a proof-of-concept and a base for future
		development.

DONE- Write an algorithm for townGen, for creating dynamic cities.


DONE- Build program to populate buildings with characters from charGen,
		and task with jobs such as guard, city official, merchant, thug,
		inkeeper,and the like. Tag others with dynamic quests provided
		from questGen.

INDEV- Create VERY simple interface to control/display inputs/outputs.
		Use tree-like navigation to categorize each building, inhabitants,
		quests, POI, etc.
0.6.0a- Write questGen: to generate dynamic quests, based on output from
		areaGen.


0.9.0a- BugHunt!

============
BEYOND SCOPE
============
??? Create dynamic interaction with characters

INPRO- Create image map of area from output, will reflect POI, Quests, Etc.

??? Use Panda3d engine to make 3d representation of generated area; may
	use Panda3d for simplicity, cross-platform, freedom, and native Python
	wrapper support reasons. Gamemaker is for pussies.
