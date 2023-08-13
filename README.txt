Backing Track Maker
Author: Hayden Dustin

This program takes a .wav file containing a simple melody
and creates a lead sheet to back that melody.

Commands to Run:
 - python -W ignore run.py Sample_Gmin.wav <Debug Mode: True|False> <Detailed Debug Mode: True|False> <Graph Debug Mode: True|False>
 or
 - python3 -W ignore run.py Sample_Gmin.wav <Debug Mode: True|False> <Detailed Debug Mode: True|False> <Graph Debug Mode: True|False>


CURRENT OUTPUTS:
Debug Mode:
 - A list of each note in the .wav file
 - An analysis of the key and tempo
 - A debug version of the lead sheet

Detailed Debug Mode:
 - Everything in Debug Mode
 - A list of the weights of each key for the file
 - Displays a calculation of where the first note in the first measure is
 - Displays the note at the start of each measure

Graph Debug Mode:
 - Everything in Detailed Debug Mode
 - Provides a graph for the location of each note in the .wav file
 - Provides a frequency graph for each note


Python Version: 3.10.6

Requirements:
 - scipy
 - numpy
 - matplotlib
 - os
 - pydub
