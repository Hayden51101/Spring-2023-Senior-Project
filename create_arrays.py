import numpy as np

def get_piano_notes():   
    # White keys are in Uppercase and black keys (sharps) are in lowercase
    octave = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'] 

    base_freq = 440 #Frequency of A4

    # Goes through each letter in octave and assigns a number, then increments the number and repeats
    # Ex. a2, B2, C3, c3, etc.
    keys = np.array([x+str(y) for y in range(0,9) for x in octave])

    # Trim to standard 88 keys
    start = np.where(keys == 'A0')[0][0]
    end = np.where(keys == 'C8')[0][0]
    keys = keys[start:end+1]
    
    # The equation for determining specific pitches is complicated. This is as condensed as it can get.
    note_freqs = dict(zip(keys, [2**((n+1-49)/12)*base_freq for n in range(len(keys))]))
    note_freqs[''] = 0.0 # stop
    return note_freqs, octave


def get_key_signatures(full_octave, path):
    key_signatures = np.chararray((12, 2, 7), itemsize=2)
    with open(path, "r") as ks:
        i = 0
        for note in full_octave:
            major = ks.readline().split(", ")
            minor = ks.readline().split(", ")
            ks.readline()
            key_signatures[i, 0, :] = major
            key_signatures[i, 1, :] = minor
            i+=1
    
    return key_signatures

def get_key_weights(full_octave, path):
    key_weights = []
    with open(path, "r") as ks:
        for note in full_octave:
            major = ks.readline().split(", ")
            minor = ks.readline().split(", ")
            ks.readline()

            major = [eval(n) for n in major]
            minor = [eval(n) for n in minor]

            key_weights.append(major)
            key_weights.append(minor)
    
    return key_weights

def key_offset(a, offset):
    return a[offset:] + a[:offset]

def get_chord_weights(full_octave, key, path, is_major):
    chord_weights = []
    with open(path, "r") as ks:
        empty = ks.readline().split(", ")
        ks.readline()
        empty = [eval(n) for n in empty]
        for note in full_octave:
            flag = True
            for n in key:
                if(n == note):
                    if(is_major):
                        temp = ks.readline().split(", ")
                        ks.readline()
                        ks.readline()
                    else:
                        ks.readline()
                        temp = ks.readline().split(", ")
                        ks.readline()

                    temp = [eval(n) for n in temp]

                    final = key_offset(temp, len(full_octave) - full_octave.index(key[0]))
                    chord_weights.append(final)
                    flag = False
            if(flag):
                chord_weights.append(empty)

    return chord_weights


def create_measures(loc, tempo, timsig, sensitivity = 0.2):
    current_measure = (tempo * timsig) + loc[0]
    measure_locations = [0]
    for i in range(len(loc) - 1):
        if(current_measure > loc[i] - sensitivity and current_measure < loc[i] + sensitivity):
            measure_locations.append(i)
            current_measure = (tempo * timsig) + loc[i]
    
    return measure_locations