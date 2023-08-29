import numpy as np
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(
    os.path.dirname(__file__), '../..')))

import camerasimulatordb


def mymean():
    original_image = np.random.random((100, 100))
    sensor_processor = camerasimulatordb.Sensor(gain=5, enable=True)
    processed_image = sensor_processor.process(image=original_image)
    return np.mean(processed_image)


if __name__ == "__main__":
    mymean()
