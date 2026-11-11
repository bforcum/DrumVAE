import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from pathlib import Path 
import urllib.request
import zipfile

from mido import MidiFile

# Open data
groove_path = "data/groove/"

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

noteMap = {
    36: [1, "Kick"],
    37: [2, "Snare"],
    38: [2, "Snare"],
    40: [3, "Rimshot"],
    48: [4, "High Tom"],
    50: [4, "High Tom"],
    45: [5, "Low-Mid Tom"],
    47: [5, "Low-Mid Tom"],
    43: [6, "High Floor Tom"],
    58: [6, "High Floor Tom"],
    26: [7, "Open HH"],
    42: [7, "Open HH"],
    22: [8, "Closed HH"],
    44: [9, "Pedal HH"],
    49: [10, "Crash"],
    55: [10, "Crash"],
    57: [10, "Crash"],
    52: [10, "Crash"],
    51: [11, "Ride Cymbal"],
    59: [11, "Ride Cymbal"],
    53: [12, "Ride Bell"],
    
}


df_raw = pd.read_csv("data/groove/info.csv", usecols=["midi_filename", "time_signature", "split"])
df = df_raw[df_raw["time_signature"] == "4-4"]
df.drop(columns="time_signature")
df["midi_filename"] = groove_path + df["midi_filename"]


# Parse data
mid = MidiFile(df["midi_filename"][0])

hits = []
notes = []
micro = []

rate = 1 / mid.ticks_per_beat

ticks = 0
print(mid.tracks[0][:6])

for msg in mid.tracks[0]:
    ticks += msg.time 
    if msg.type == 'note_on':
        hitTime = ticks * rate
        hits.append(hitTime)
        notes.append(noteMap[msg.note][0])
        micro.append(4 * hitTime - round(4 * hitTime))

plt.figure()
plt.subplot(211)
plt.scatter(hits, notes)
plt.xticks(np.arange(0,int(ticks*rate), 4))
plt.subplot(212)
plt.hist(micro, bins=32)

plt.show()

