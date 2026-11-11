import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time

import groove
import constants


start = time.time()
train_set, val_set, test_set = groove.asPandas()
end = time.time()

print(f"It took {end - start:.3f} seconds to parse all {len(train_set) + len(val_set) + len(test_set)} MIDI files")



track1 = train_set["data"].iloc[0]

display = track1[16:48,:,1]

plt.figure(figsize=(10,5))

plt.imshow(display.transpose(), origin="lower", interpolation=None, extent=[1,33,-0.5,11.5])

plt.xticks(np.arange(1,33,4), np.arange(1,9))
plt.yticks(np.arange(0,12), constants.instrumentMap.values())
plt.xlabel("Beats")

plt.tight_layout()
plt.show()

