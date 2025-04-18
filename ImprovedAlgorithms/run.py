####################### IMPORTS ########################
### SCIPY ###
from scipy.fft import fft
from scipy.io import wavfile
from scipy.signal import find_peaks

### NUMPY ###
import numpy as np
from numpy import arange

### MATPLOT ###
import matplotlib.pyplot as plt

### OS ###
import os

### PYDUB ###
from pydub import AudioSegment

### SYSTEM ###
import sys

### LOCAL FILE METHODS ###
from create_arrays import get_piano_notes, get_key_signatures, get_key_weights, create_measures, get_chord_weights
from find_frequency import get_frequency
from find_key import find_key
from find_tempo import get_tempo
from create_measures import create_measures
from find_chord import find_chord
from wav_file_disection import find_note_locations



######################## FIELDS ########################
file = "testAudio\\" + sys.argv[1]
key_signature_file = "data\\key_signatures.txt"
note_weight_file = "data\\note_weights.txt"
chord_weight_file = "data\\chord_weights.txt"
all_notes, one_octave = get_piano_notes()
key_signatures = get_key_signatures(one_octave, key_signature_file)

DEBUG = sys.argv[2] == "True"
DETAILED_DEBUG = sys.argv[3] == "True"
GRAPH_DEBUG = sys.argv[4] == "True"



######################### MAIN #########################
# Fetches the file and reads the data from the .wav file
here_path = os.path.dirname(os.path.realpath(__file__))
wav_file_name = file
wave_file_path = os.path.join(here_path, wav_file_name)
sr, raw_data = wavfile.read(wave_file_path)

# Extracts only the first channel from the 2-D .wav file
data = raw_data[:, 0]
time = np.arange(len(data)) / float(sr)

if(DETAILED_DEBUG):
    print("############## GENERATING GRAPHS ##############")
# Finds the locations of all notes in the .wav file
note_locations = find_note_locations(wave_file_path, 3, DEBUG = DETAILED_DEBUG)

if(GRAPH_DEBUG):
    print("##### ALL NOTE GRAPH GENERATES SEPARATELY #####\n")
if(DEBUG):
    print("#################### NOTES ####################")
note_values = []
# Stores each note contained in the .wav file in note_values
for n in range(len(note_locations)):
    if(n < len(note_locations) - 1):
        start = note_locations[n] * sr
        end = note_locations[n + 1] * sr

        note_values.append(get_frequency(data[round(start):round(end)], sr, all_notes, DEBUG = GRAPH_DEBUG))
        if(DEBUG):
            print(n, ": ", note_values[n], " @ ", note_locations[n], sep="", end="\t")
            if(n % 3 == 2):
                print("\n")

# Finds the actual key of the piece
key_weights = get_key_weights(one_octave, note_weight_file)
TRUE_KEY, IS_MAJOR = find_key(one_octave, note_values, key_signatures, key_weights, DEBUG = DETAILED_DEBUG)
if IS_MAJOR:
    TRUE_KEY_WEIGHT = key_weights[one_octave.index(TRUE_KEY[0])]
else:
    TRUE_KEY_WEIGHT = key_weights[one_octave.index(TRUE_KEY[0]) + 1]

TEMPO, TIME_SIGNATURE = get_tempo(note_locations, note_values, TRUE_KEY, DEBUG=DEBUG)

if(True):
    print("\n\n\n################ FILE ANALYSIS ################")
    print("Overall Key: ", end="")
    if(IS_MAJOR):   print(TRUE_KEY[0] + " Major", end="\n")
    else:           print(TRUE_KEY[0] + " Minor", end="\n")
    print("Tempo: ", int(60 / TEMPO))
    print("Time Signature Grouping: ", TIME_SIGNATURE)
    print()

# Remove the end of the piece as a note location
note_locations = note_locations[:len(note_locations) - 1]

GROUPING, MEASURES = create_measures(TEMPO, TIME_SIGNATURE, note_values, note_locations, TRUE_KEY, TRUE_KEY_WEIGHT, one_octave)

if(True):
    print("############ TIME SIGNATURE ############")
    print(GROUPING)
    print(" /")
    print("  " + str(TIME_SIGNATURE))

# measure_locations = create_measures(note_locations, TEMPO, TIME_SIGNATURE)

# if(DETAILED_DEBUG):
#     print("############### MEASURE DETAILS ###############")
#     print("Measure Note Locations: ", end="")
#     for i in range(len(measure_locations) - 1):
#         print(measure_locations[i], end=", ")
#     print(measure_locations[len(measure_locations) - 1], "\n\n\n\n\n")

# lead_sheet_keys = []
# chord_weights = get_chord_weights(one_octave, TRUE_KEY, chord_weight_file, IS_MAJOR)
# for i in range(len(measure_locations) - 1):
#     key = find_chord(one_octave, note_values[measure_locations[i]:measure_locations[i + 1]], chord_weights, TRUE_KEY, IS_MAJOR, DEBUG=True)
#     lead_sheet_keys.append(key)


# if(IS_MAJOR):
#     toAdd = str(TRUE_KEY[0]) + " Maj"
#     lead_sheet_keys.append(toAdd)
# else:
#     toAdd = str(TRUE_KEY[0]) + " Min"
#     lead_sheet_keys.append(toAdd)

# if(DEBUG):
#     print("######################### LEAD SHEET #########################")
#     print("Msr #:", end="\t")
#     for i in range(len(lead_sheet_keys)):
#         print(i, end="\t")
#     print("\nChord:", end="\t")
#     for i in range(len(lead_sheet_keys)):
#         print(lead_sheet_keys[i], sep="", end="\t")