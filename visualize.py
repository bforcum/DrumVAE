import matplotlib as matplot
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time

import groove
import constants


start = time.time()
df = groove.asPandas(preSplit=False)
end = time.time()

print(f"It took {end - start:.3f} seconds to parse all {len(df)} MIDI files")

instrumentCounts = df["data"].apply(lambda x: np.sum(x[:,:,0], axis=0)).sum(axis=0)
print(instrumentCounts.shape)
print(instrumentCounts)

track1 = df["data"].iloc[0]

counts = np.sum(track1[:,:,0],axis=0)
print(counts.shape)
print(counts)

display = track1[16:48,:,1]

plt.figure(figsize=(10,6))

plt.subplot(211)
plt.title("Beat Sample")
plt.imshow(display.transpose(), origin="lower", interpolation=None, extent=[1,33,-0.5,11.5])

plt.xticks(np.arange(1,33,4), np.arange(1,9))
plt.yticks(np.arange(0,12), constants.instrumentMap.values())
plt.xlabel("Beats")

plt.subplot(212)
plt.title("Drum Counts")
plt.bar(constants.instrumentMap.values(), instrumentCounts)
plt.xticks(rotation=-90)

plt.tight_layout()
plt.show()

