import numpy as np
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