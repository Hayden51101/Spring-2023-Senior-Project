def create_measures(tempo: int, grouping: int, notes: list, note_locations: list, key: list, key_weights: list, one_octave: list) -> tuple[int, list[list]]:
    if(grouping == 4):
        return iterator(tempo, "data\\simple_time_signature_weights.txt", notes, note_locations, key, key_weights, one_octave)



def iterator(tempo: int, path: str, notes: list, note_locations: list, key: list, key_weights: list, one_octave: list) -> tuple[int, list[list]]:
    with open(path, "r") as f:
        time_signature_weights = []
        for l in f.readlines():
            l = l.strip("\n")
            time_signature_weights.append([int(i) for i in l.split(", ")])
        print(time_signature_weights)

        time_signature_accuracies = []
        time_signature_measures = []

        for ts in range(len(time_signature_weights)):
            time_signature_accuracies.append(0)
            time_signature_measures.append(define_measures(tempo, time_signature_weights[ts][0], note_locations, notes))
            for m in range(len(time_signature_measures[ts])):
                print("Measure " + str(m) + ": " + str(time_signature_measures[ts][m]))
                for n in time_signature_measures[ts][m]:
                    if(n[1] != "None"):
                        note_weight = key_weights[one_octave.index(n[1][0])] * measure_position(n[0], note_locations[0] + (time_signature_weights[ts][0] * tempo * m), tempo, time_signature_weights[ts])
                        print(note_weight)
                        time_signature_accuracies[ts]+=note_weight
                print("\n")
        
        for t in time_signature_accuracies:
            print(t)
        
        return time_signature_weights[time_signature_accuracies.index(max(time_signature_accuracies))][0], time_signature_measures[time_signature_accuracies.index(max(time_signature_accuracies))]
            


def measure_position(note: float, measure_start_time: float, tempo: float, time_signature_weight: list, sensitivity = 0.05) -> int:
    possible_note_positions = []
    for i in range(len(time_signature_weight[1:])):
        possible_note_positions.append(measure_start_time + (i * tempo / 2))

    for pnp in possible_note_positions:
        if(pnp + sensitivity > note and pnp - sensitivity < note):
            return time_signature_weight[possible_note_positions.index(pnp) + 1]
    
    return 0



def define_measures(tempo: int, measure_length: int, note_locations: list, notes: list) -> list[list]:
    index = 0
    measure = 0
    start_point = note_locations[0]
    stop_point = note_locations[len(note_locations) - 1]
    measure_time = measure_length * tempo
    print(measure_time)
    measures = [[]]

    while(start_point + (measure * measure_time) < stop_point):
        measures.append([])
        while(index < len(note_locations) and note_locations[index] < (measure + 1) * measure_time):
            measures[measure].append([note_locations[index], notes[index]])
            index+=1
        measure+=1

    return measures