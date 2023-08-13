import numpy as np
import matplotlib.pyplot as plt
from pydub import AudioSegment


def find_note_locations(file_path, SENSITIVITY = 5, NOTE_LENGTH = 10, DEBUG = False):
    song = AudioSegment.from_file(file_path)

    note_locations = []

    # Noise filter
    song = song.low_pass_filter(2000).high_pass_filter(10)
    SEGMENT_MS = 10
    volume = [segment.dBFS for segment in song[::SEGMENT_MS]]
    # plt.savefig("MS50")
    for i in range(1, len(volume)):
        if(volume[i] > -45 and              # Finds when audio is above a certain volume threshold (-45dB)
           volume[i] - volume[i - 1] > SENSITIVITY):  # Checks if there was a significant jump immediately prior to this point
            if(len(note_locations) == 0 or  # If the array is empty, this is the first note, so it adds it no matter what
                                            # Otherwise, it checks to see if the previously added note was a certain time
                                            # away (10 frames after scaling)
               i - note_locations[len(note_locations)-1] / SEGMENT_MS * 1000 > NOTE_LENGTH):
                note_locations.append(i * SEGMENT_MS / 1000)    # Adds the note to the array of notes in the file
    note_locations.append(len(volume) * SEGMENT_MS / 1000)


    if(DEBUG):
        x_axis = np.arange(len(volume)) * (SEGMENT_MS / 1000)
        plt.plot(x_axis, volume)
        for n in note_locations:
            plt.axvline(x=n, color='r', linewidth=0.5, linestyle="-")   # Adds a line signifying the start of each note

        plt.show()

    return note_locations