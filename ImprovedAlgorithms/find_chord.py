import re


    
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