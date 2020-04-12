All code in the Part1 folder is written by Siri Khalsa
All code in the Part2 folder is written by Anas Gauba
All Code is Written in python3

Part1 Dependencies:
	- requires the math library installed: pip or pip3 install math
	- requires numpy library: pip or pip3 install numpy
	- requires matplotlib library: pip or pip3 install matplotlib
	- requires random library: pip or pip3 install random
	- requires the copy library: pip or pip3 install copy 

To obtain the graph in figure 1. please run script Part1/Part1b.py with python3
To obtain the data from the simulated runs that determines how likely COVID is to become SARS 
please run Part1/Part1dv2.py

Part2 Dependencies:
	- requires wxpython gui library for running gui: pip or pip3 install wxpython
        - requires random library: pip or pip3 install random
        - requires numpy library: pip or pip3 install numpy
        - requires itertools and fractions library. 

Running gui: 
 - Run script Part2/CA2dDynamicsGUIWx.py with python3.
 - This will prompt you to ask the version of the CA to run.
 - To run the appropriate gui version of CA, select between 4 versions (1-4).
 NOTE: Need wxpython gui library to run the gui.

To obtain GA's solution, simply run script Part2/GA2dCA.py with python3.
 - The GA's solution will be written to script Part2/secondVariantRuleGA.py. 
 - You can rerun the gui to use GA's solution in CA's simulation by choosing option 4.

  
NOTE: You can modify Part2/CABoard.py and increase the boardSize to more than 50x50. For example:
      changing CABoard._board_col and CABoard._board_row to be 100. 

