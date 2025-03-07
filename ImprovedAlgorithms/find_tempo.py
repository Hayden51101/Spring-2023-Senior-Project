import numpy as np
import re



def tempo_mode_test(mode_tempo: float, dilation: float, sensitivity: float, timestamps: list, notes: list, key: list):
    """
    
    """



    test_tempo = mode_tempo * dilation
    correct_notes = 0

    for i in range(len(notes)):
        for n in range(len(notes) - i - 1):
            if(timestamps[i] + test_tempo > timestamps[i + n + 1] - sensitivity and
               timestamps[i] + test_tempo < timestamps[i + n + 1] + sensitivity):
                correct_notes+=1
                if notes[i] == key[0]:
                    correct_notes+=1

    return correct_notes / len(notes)



def get_tempo(note_timestamps: list, notes_in_melody: list, key_of_melody: list, distance_sensitivity = 0.05, pass_threshold = 0.95, DEBUG = False) -> tuple[int, int]:
    """
    
    """



    distance_between_notes = []
    previous_note = None

    for note in note_timestamps:
        if previous_note == None:
            previous_note = note

        else:
            distance_between_notes.append(note - previous_note)
            previous_note = note

    print("\n\n" + str(distance_between_notes) + "\n\n")



    note_distances = []
    distance_occurances = []

    for current_distance in distance_between_notes:

        closest_distance_index = -1
        closest_distance = 100
        for i in range(len(note_distances)):
            if abs(current_distance - note_distances[i]) < closest_distance:
                closest_distance_index = i
                closest_distance = abs(current_distance - note_distances[i])

        if closest_distance > distance_sensitivity:
            note_distances.append(current_distance)
            distance_occurances.append(1)

        else:
            distance_occurances[closest_distance_index]+=1



    for i in range(len(note_distances)):
        print(str(note_distances[i]) + " - " + str(distance_occurances[i]))



    mode_distance = note_distances[distance_occurances.index(max(distance_occurances))]



    print(tempo_mode_test(mode_distance, 1, distance_sensitivity, note_timestamps, notes_in_melody, key_of_melody))
    print(tempo_mode_test(mode_distance, 1/2, distance_sensitivity, note_timestamps, notes_in_melody, key_of_melody))
    print(tempo_mode_test(mode_distance, 2, distance_sensitivity, note_timestamps, notes_in_melody, key_of_melody))
    print(tempo_mode_test(mode_distance, 1/4, distance_sensitivity, note_timestamps, notes_in_melody, key_of_melody))
    print(tempo_mode_test(mode_distance, 4, distance_sensitivity, note_timestamps, notes_in_melody, key_of_melody))
    print(tempo_mode_test(mode_distance, 1/3, distance_sensitivity, note_timestamps, notes_in_melody, key_of_melody))
    print(tempo_mode_test(mode_distance, 3, distance_sensitivity, note_timestamps, notes_in_melody, key_of_melody))



    return mode_distance, 0