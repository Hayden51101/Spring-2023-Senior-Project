####################### IMPORTS ########################
### TKINTER ###
from tkinter import Tk
from tkinter import ttk
from tkinter import *
from tkinter.filedialog import askopenfilename

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
from get_info import get_frequency, find_key, get_tempo, find_chord
from wav_file_disection import find_note_locations


######################## FIELDS ########################
key_signature_file = "data/key_signatures.txt"
note_weight_file = "data/note_weights.txt"
chord_weight_file = "data/chord_weights.txt"
all_notes, one_octave = get_piano_notes()
key_signatures = get_key_signatures(one_octave, key_signature_file)
DEBUG = False
DETAILED_DEBUG = False
GRAPH_DEBUG = False
class FileHandler():
    file = ""
    def select_file(self):
        self.file = askopenfilename()



######################### MAIN #########################
def main(frame, label, gui):
    # Fetches the file and reads the data from the .wav file
    wave_file_path = fh.file
    sr, raw_data = wavfile.read(wave_file_path)

    # Extracts only the first channel from the 2-D .wav file
    data = raw_data[:, 0]
    time = np.arange(len(data)) / float(sr)

    label.config(text="Finding Note Locations")
    progress_bar = ttk.Label(frame, text="|--------------------------------------------------|", font=("Courier", 11))
    progress_bar.grid(column=1, row=1)
    frame.update()
    # Finds the locations of all notes in the .wav file
    note_locations = find_note_locations(wave_file_path, 3)
    label.config(text="Identifying Notes")
    progress_bar.config(text="|#####---------------------------------------------|")
    frame.update()

    progress_rate = round(len(note_locations)/20)
    if(progress_rate == 0):
        progress_rate = 1
    pr = 0

    note_values = []
    # Stores each note contained in the .wav file in note_values
    for n in range(len(note_locations)):
        if(n < len(note_locations) - 1):
            start = note_locations[n] * sr
            end = note_locations[n + 1] * sr

            note_values.append(get_frequency(data[round(start):round(end)], sr, all_notes))

            if(n % progress_rate == progress_rate - 1):
                pr+=1
                temp = ""
                for i in range(20):
                    if(i <= pr):
                        temp+="#"
                    else:
                        temp+="-"
                progress_bar.config(text="|#####" + temp + "-------------------------|")
                frame.update()
    


    label.config(text="Finding the Key")
    progress_bar.config(text="|##############################--------------------|")
    frame.update()
    # Finds the actual key of the piece
    TRUE_KEY, IS_MAJOR = find_key(one_octave, note_values, key_signatures, get_key_weights(one_octave, note_weight_file))

    label.config(text="Finding the Tempo")
    progress_bar.config(text="|###################################---------------|")
    frame.update()
    TEMPO, TIME_SIGNATURE = get_tempo(note_locations, note_values, TRUE_KEY)

    label.config(text="Creating Measures")
    progress_bar.config(text="|########################################----------|")
    frame.update()
    measure_locations = create_measures(note_locations, TEMPO, TIME_SIGNATURE)

    progress_rate = round(len(measure_locations)/10)
    if(progress_rate == 0):
        progress_rate = 1
    pr = 0
    label.config(text="Creating Chords")
    progress_bar.config(text="|########################################----------|")
    frame.update()
    lead_sheet_keys = []
    chord_weights = get_chord_weights(one_octave, TRUE_KEY, chord_weight_file, IS_MAJOR)
    for i in range(len(measure_locations) - 1):
        key = find_chord(one_octave, note_values[measure_locations[i]:measure_locations[i + 1]], chord_weights, TRUE_KEY, IS_MAJOR)
        lead_sheet_keys.append(key)

        if(i % progress_rate == progress_rate - 1):
                pr+=1
                temp = ""
                for n in range(10):
                    if(n <= pr):
                        temp+="#"
                    else:
                        temp+="-"
                progress_bar.config(text="|##############################" + temp + "|")
                frame.update()


    if(IS_MAJOR):
        toAdd = str(TRUE_KEY[0]) + " Maj"
        lead_sheet_keys.append(toAdd)
    else:
        toAdd = str(TRUE_KEY[0]) + " Min"
        lead_sheet_keys.append(toAdd)

    label.config(text="Complete!")
    progress_bar.config(text="|##################################################|")
    frame.update()

    frame = ttk.Frame(gui, padding=10)
    frame.grid()
    ttk.Label(frame, text = "######################### LEAD SHEET #########################").grid(column=0, row=0)
    temp = "Msr #:\t"
    for i in range(len(lead_sheet_keys)):
       temp+=str(i) + "\t"
    m_num = ttk.Scrollbar(frame)
    m_num.grid(column=0, row=1)
    num = Text(gui, xscrollcommand=m_num.set)
    num.grid(column=0, row=1)
    num.insert(END, temp)
    num.insert(END, "\n")
    temp = "Chord:\t"
    for i in range(len(lead_sheet_keys)):
        temp+=str(lead_sheet_keys[i]) + "\t"
    num.insert(END, temp)



####################### UI SETUP #######################
ui = Tk()
ui.title("Lead Sheet Generator")
ui.geometry("600x200")
frame = ttk.Frame(ui, padding=10)
frame.grid()
text = ttk.Label(frame, text="Select a file to begin generating!", font=("Courier", 12))
text.grid(column=1, row=0)
fh = FileHandler()
ttk.Button(frame, text="Select File", command=fh.select_file).grid(column=0, row=0)
ttk.Button(frame, text="Run", command=lambda: main(frame, text, ui)).grid(column=0, row=1)
ui.mainloop()