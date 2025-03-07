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



def average(num_list: list) -> float:
    if not num_list:
        return 0
    return sum(num_list) / len(num_list)



def find_mode_index(list: list):
    if not list:
        return -1
    index = 0
    for i in range(len(list)):
        if(len(list[i]) > len(list[index])):
            index = i

    return index



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



    note_distances = []

    for current_distance in distance_between_notes:

        closest_distance_index = -1
        closest_distance = 100
        for i in range(len(note_distances)):
            if abs(current_distance - average(note_distances[i])) < closest_distance:
                closest_distance_index = i
                closest_distance = abs(current_distance - average(note_distances[i]))

        if closest_distance > distance_sensitivity:
            note_distances.append([current_distance])

        else:
            note_distances[closest_distance_index].append(current_distance)



    mode_distance = average(note_distances[find_mode_index(note_distances)])



    print(tempo_mode_test(mode_distance, 1, distance_sensitivity, note_timestamps, notes_in_melody, key_of_melody))
    print(tempo_mode_test(mode_distance, 1/2, distance_sensitivity, note_timestamps, notes_in_melody, key_of_melody))
    print(tempo_mode_test(mode_distance, 2, distance_sensitivity, note_timestamps, notes_in_melody, key_of_melody))
    print(tempo_mode_test(mode_distance, 1/4, distance_sensitivity, note_timestamps, notes_in_melody, key_of_melody))
    print(tempo_mode_test(mode_distance, 4, distance_sensitivity, note_timestamps, notes_in_melody, key_of_melody))
    print(tempo_mode_test(mode_distance, 1/3, distance_sensitivity, note_timestamps, notes_in_melody, key_of_melody))
    print(tempo_mode_test(mode_distance, 3, distance_sensitivity, note_timestamps, notes_in_melody, key_of_melody))



    return mode_distance, 0