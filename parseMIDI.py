import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from pathlib import Path 
import urllib.request
import zipfile

from mido import MidiFile
import time

# Open data
groove_path = "data/midi/groove/"
parsed_path = "data/numpy/groove/"

if not Path(groove_path).is_dir():
    print("Downloading dataset...")
    # Create data directory and child downloads directory
    Path("data/downloads/").mkdir(parents=True, exist_ok=True)
    Path("data/midi/").mkdir(parents=True, exist_ok=True)
    groove_url = "https://storage.googleapis.com/magentadata/datasets/groove/groove-v1.0.0-midionly.zip"
    # Pass data_dir directly into the load function
    urllib.request.urlretrieve(groove_url, "data/downloads/groove.zip")
    print("Extracting dataset...")
    try:
        zipfile.ZipFile('data/downloads/groove.zip', 'r').extractall('data/midi/')
    except:
        # Zip archive contains a reference to an incorrectly formatted path and always throws an error
        pass




recordings_info = pd.read_csv(groove_path + "info.csv", usecols=["midi_filename", "time_signature", "split"])
recordings_paths = recordings_info[recordings_info["time_signature"] == "4-4"].drop(columns="time_signature")


# Parse data
instrumentMap = {
    0: "Kick",
    1: "Snare",
    2: "Rimshot",
    3: "High Tom",
    4: "Low-Mid Tom",
    5: "High Floor Tom",
    6: "Open HH",
    7: "Closed HH",
    8: "Pedal HH",
    9: "Crash",
    10: "Ride Cymbal",
    11: "Ride Bell",
}

noteMap = {
    36: 0,
    37: 1,
    38: 1,
    40: 2,
    48: 3,
    50: 3,
    45: 4,
    47: 4,
    43: 5,
    58: 5,
    46: 6,
    26: 6,
    42: 7,
    22: 7,
    44: 8,
    49: 9,
    55: 9,
    57: 9,
    52: 9,
    51: 10,
    59: 10,
    53: 11,  
}


grids = []

for i, fileName in enumerate(recordings_paths["midi_filename"][:3]):
    if i % 100 == 0:
        print(f"{i} tracks analyzed")
    
    mid = MidiFile(groove_path + fileName)

    # Divide each beat (4th) by 4 = 2^2 for 16ths
    ticks_per_16th = mid.ticks_per_beat >> 2
    half_16th = ticks_per_16th >> 1
    inv_ticks_per_16th = 1.0 / ticks_per_16th

    notes = []

    ticks = 0

    for msg in mid.tracks[0]:
        ticks += msg.time 
        if msg.type == 'note_on' and msg.velocity > 0:
            hitTime = (ticks + half_16th) // ticks_per_16th
            instrument = noteMap[msg.note]
            # Hit = 1
            # msg.velocity
            microTime = (ticks - (hitTime * ticks_per_16th)) * inv_ticks_per_16th
            notes.append(((hitTime, instrument), [1, msg.velocity, microTime]))
    grid = np.zeros((-(-ticks // ticks_per_16th), len(instrumentMap), 3))
    for note in notes:
        grid[note[0]] = note[1]
    grids.append(grid)


plt.figure()

plt.imshow(grids[1][0:16,:,1].transpose(), origin="lower")

plt.show()