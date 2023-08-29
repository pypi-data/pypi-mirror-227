"""This module has a util function named mymean
"""
import os
import sys
import numpy as np
import time
import camerasimulatordb
sys.path.insert(0, os.path.abspath(os.path.join(
    os.path.dirname(__file__), '../..')))


def mymean():
    """This function generate a random image which pass to sensor
    process method and get the mean of the returned image

    Returns:
        float: Mean of the sensor processed image
    """
    time.sleep(0.2)
    height = 100
    width = 100
    original_image = np.random.random((height, width))
    sensor_processor = camerasimulatordb.Sensor(gain=5, enable=True)
    processed_image = sensor_processor.process(
        image=original_image, height=height, width=width)
    return np.mean(processed_image)


if __name__ == "__main__":
    mymean()
