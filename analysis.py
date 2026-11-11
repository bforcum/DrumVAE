import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from pathlib import Path 
import urllib.request
import zipfile

from mido import MidiFile
import time

# Open data
groove_path = "data/groove/"

start = time.time()

if not Path(groove_path).is_dir():
    try:
        print("Directory doesn't exist")
        # Create data directory and child downloads directory
        Path("data/downloads/").mkdir(parents=True, exist_ok=True)
        groove_url = "https://storage.googleapis.com/magentadata/datasets/groove/groove-v1.0.0-midionly.zip"
        # Pass data_dir directly into the load function
        urllib.request.urlretrieve(groove_url, "data/downloads/groove.zip")

        zipfile.ZipFile('data/downloads/groove.zip', 'r').extractall('data/')
    except:
        # Zip archive contains a reference to an incorrectly
        # formatted path and always throws an error
        pass

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


df_raw = pd.read_csv("data/groove/info.csv", usecols=["midi_filename", "time_signature", "split"])
df = df_raw[df_raw["time_signature"] == "4-4"]
df.drop(columns="time_signature")
df["midi_filename"] = groove_path + df["midi_filename"]


# Parse data

counts = np.zeros(12)

for i, fileName in enumerate(df["midi_filename"]):
    if i % 100 == 0:
        print(f"{i} tracks analyzed")
    
    mid = MidiFile(fileName)

    # hits = []
    # notes = []
    # micro = []

    # rate = 1 / mid.ticks_per_beat

    # ticks = 0
    for msg in mid.tracks[0]:
        # ticks += msg.time 
        if msg.type == 'note_on' and msg.velocity > 0:
            counts[noteMap[msg.note]] += 1
            # hitTime = ticks * rate
            # hits.append(hitTime)
            # notes.append(noteMap[msg.note])
            # micro.append(4 * hitTime - round(4 * hitTime))

end = time.time()

print(f"It took {end - start:.3f} seconds to parse all {len(df)} MIDI files")

plt.figure()

plt.bar(instrumentMap.values(), counts)

plt.show()

