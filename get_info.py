from scipy.fft import fft
from numpy import arange
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import re


def buildArray(a):
    """
    Helper method designed to convert np arrays into standard arrays.
    :param a: np.array
    :returns: array
    """
    newA = ["" for i in range(len(a))]
    for i in range(len(a)):
        newA[i] = re.sub(r'b', '', str(a[i]))
        newA[i] = re.sub(r'\'', '', str(newA[i]))
    return newA



def get_frequency(x, sf, notes_array, DEBUG = False):
    """
    Derive frequency spectrum of a signal from time domain
    :param x: signal in the time domain
    :param sf: sampling frequency
    :returns: frequencies and their content distribution
    """
    x = x - np.average(x)  # zero-centering

    n = len(x)
    k = arange(n)
    tarr = n / float(sf)
    frqarr = k / float(tarr)  # two sides frequency range

    frqarr = frqarr[range(n // 2)]  # one side frequency range

    x = fft(x) / n  # fft computing and normalization
    x = x[range(n // 2)]

    peak_indicies, props = find_peaks(x, height=0.015)
    max_mag = 0
    note_freq = 0
    for i, peak in enumerate(peak_indicies):
        freq = frqarr[peak]
        magnitude = props["peak_heights"][i]
        if(max_mag < magnitude):
            max_mag = magnitude
            note_freq = freq

    note = "None"
    for fr in notes_array:
        if(abs(note_freq - notes_array[fr]) < 5):
            note = str(fr)

    if(DEBUG):
        plt.plot(frqarr, abs(x))
        plt.xlabel('Freq (Hz)')
        plt.ylabel('|X(freq)|')
        plt.tight_layout()
        plt.title(note)
        plt.show()

    return note

def find_key(octave: str, notes: str, keys: np, weights: np, DEBUG = False):
    # Used to determine how common each note is
    note_weight = [0 for i in range(len(octave))]

    # Calculate the occurence of each note
    for n in notes:
        if(n != "None"):
            temp = octave.index(re.sub(r'[0-9]', '', n))
            note_weight[temp]+=1

    # Calculates the weight for each key, major then minor
    key_weights = [0 for i in range(len(octave) * 2)]
    for key in range(len(octave)):                                          # Loops for each key
        for maj_min in range(len(keys[0, :, 0])):                           # Checks major and minor
            sum = 0                                                         # Loop order 12 - 2 - 12
            for note in range(len(note_weight)):                            # Checks each note
                sum+=weights[(key * 2) + maj_min][note] * note_weight[note] # Multiplies each note's weight by its occurance
            key_weights[(key * 2) + maj_min] = sum                          # Stores the overall score

    # Determines if the key selected was major or minor
    maxKey = max(key_weights)
    isMajor = (0 == key_weights.index(maxKey) % 2)

    if(DEBUG):
        print("########## KEY WEIGHTS ##########")
        print("###### MAJOR ####### MINOR ######")
        for i in range(0, len(key_weights), 2):
            print(str(octave[int(i/2)]) + ":", end="\t")
            print(key_weights[i], "\t|\t", key_weights[i+1])
        print()


    # Returns the array and its mode
    # Because key_weights is a 1D array it needs to be scaled to be read
    if(isMajor):
        temp = key_weights.index(maxKey) / 2
        array = buildArray(keys[int(temp), 0, :])
        return array, isMajor

    else:
        temp = (key_weights.index(maxKey) - 1) / 2
        array = buildArray(keys[int(temp), 1, :])
        return array, isMajor
    
def find_chord(octave: list, notes: list, weights: list, key: str, isMajor: bool, DEBUG = False):
    # Used to determine how common each note is
    note_occurance = [0 for i in range(len(octave))]

    # Calculate the occurence of each note
    for n in notes:
        if(n != "None"):
            temp = octave.index(re.sub(r'[0-9]', '', n))
            note_occurance[temp]+=1

    total_weights = [0 for i in range(len(weights))]
    for weight in range(len(weights)):
        c = 0
        for w in range(len(octave)):
            c+=weights[weight][w] * note_occurance[w]
        total_weights[weight] = c
    
    maxKey = total_weights.index(max(total_weights))
    offset = octave.index(key[0])
    maxKey = octave[(maxKey + offset) % 12]
    if(isMajor and (maxKey == key[0] or maxKey == key[3] or maxKey == key[4])):
        return str(maxKey) + " Maj"
    if(not(isMajor) and (maxKey == key[2] or maxKey == key[4] or maxKey == key[5] or maxKey == key[6])):
        return str(maxKey) + " Maj"
    if(not(isMajor) and (maxKey == key[1])):
        return str(maxKey) + "°"
    return str(maxKey) + " Min"

    
def tempo_helper(loc, tempo, interval, sensitivity = 0.1):
    correct_notes = 0
    for i in range(len(loc) - 2):
        t = loc[i] + tempo
        t2 = loc[i] + (tempo / interval)
        if(t > loc[i + 1] - sensitivity and t < loc[i + 1] + sensitivity):
            correct_notes+=1
        
#        elif(t2 > loc[i + 1] - sensitivity and t2 < loc[i + 1] + sensitivity):
#            correct_notes+=1
    return correct_notes

def find(list, t, min):
    for i in range(len(list)):
        if(re.sub(r'[0-9]', '', list[i]) == t):
            if(min == 0):
                return i
            min-=1

    return -1

def get_tempo(loc, notes, key, sensitivity = 0.2, pass_threshold = 0.95, DEBUG = False):
    root_loc = []
    root = key[0]
    for n in notes:
        if(root == re.sub(r'[0-9]', '', n)):
            root_loc.append(find(notes, re.sub(r'[0-9]', '', n), len(root_loc)))

    base_distance = loc[1] - loc[0]
    for i in range(2, len(loc)):
        if(loc[i] - loc[i - 1] < base_distance):
            base_distance = loc[i] - loc[i - 1]

    current_distance = loc[root_loc[1]] - loc[root_loc[0]]
    while(current_distance > base_distance):
        correct_notes = tempo_helper(loc, current_distance, 2, sensitivity)
        if(correct_notes / (len(loc) - 1) < pass_threshold):
            current_distance/=4
        else: 
            return current_distance, 4

    current_distance = loc[root_loc[1]] - loc[root_loc[0]]
    while(current_distance > base_distance):
        correct_notes = tempo_helper(loc, current_distance, 3, sensitivity)
        if(correct_notes / (len(loc) - 1) < pass_threshold):
            current_distance/=3
        else: 
            return current_distance, 3
    if(DEBUG):
        print("Failed")
    return get_tempo(loc, notes, key, sensitivity, pass_threshold - 0.1)