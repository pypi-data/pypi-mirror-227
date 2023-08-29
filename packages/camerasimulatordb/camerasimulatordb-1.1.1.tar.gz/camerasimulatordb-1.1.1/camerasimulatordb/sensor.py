"""This module has the Sensor processor
"""
from functools import wraps
import numpy as np

from .baseProcessor import BaseProcessor
from .lens import Lens


def lens_process_decorator(func):
    """Lens decorator to execute lens process method before sensor process method

    Args:
        func (Function): Sensor process method to be execute
    """
    lens_processor = Lens(None, None, True)

    @wraps(func)
    def wrapper(*args, **kwargs):
        image = kwargs.get('image')
        height = kwargs.get('height')
        width = kwargs.get('width')
        sensor_result = func(*args, **kwargs)
        lens_result = lens_processor.process(image, height, width)
        return [sensor_result, lens_result]
    return wrapper


class Sensor(BaseProcessor):
    """Sensor processor which inherit base processor

    Attributes:
        gain (float): Value of gain property to sensor processor
        image_list ([np.array]): Value of image_list property to sensor processor
    """

    def __init__(self, gain: float, enable: bool, image_list: [np.array] = None):
        self.__gain = gain
        self.__image_list = [] if image_list is None else image_list
        self.current_index = 0
        self.max_iterations = 10
        super().__init__(enable)

    def __iter__(self):
        return self

    def __next__(self):
        if self.current_index < len(self.__image_list) and self.current_index < self.max_iterations:
            image_data = self.__image_list[self.current_index]
            self.current_index += 1
            return self.iteration_process(image=image_data, iteration= self.current_index -1)
        else:
            raise StopIteration

    def get_gain(self) -> float:
        """Gain property getter method

        Returns:
            float: Value of gain property
        """
        return self.__gain

    def set_gain(self, gain: float):
        """Gain property setter method

        Args:
            gain (float): New value for gain property
        """
        self.__gain = gain

    def get_image_list(self) -> [np.array]:
        """imageList property getter method

        Returns:
            [np.array]: Value of image_list property
        """
        return self.__image_list

    def set_image_list(self, image_list: [np.array]):
        """imageList property setter method

        Args:
            imageList ([np.array]): New value for imageList property
        """
        self.__image_list = image_list

    @lens_process_decorator
    def process(self, image: np.array, height: int = None, width: int = None) -> np.array:
        """Implementation for process abstract method to Sensor processor

        Args:
            image (np.array): Input image to be process
            height (int): Value of height to lens process if property is None
            width (int): Value of width to lens process if property is None

        Raises:
            ValueError: Image isn't a 2d image

        Returns:
            np.array: Output image scaled by gain value
        """
        if len(image.shape) > 2:
            raise ValueError("Image isn't a 2d image")
        return self.__gain*image

    def iteration_process(self, image: np.array, iteration:int) -> np.array:
        """Implementation for process method to Sensor processor iterable

        Args:
            image (np.array): Input image to be process
            iteration (int): Value of iteration to be added to the image

        Raises:
            ValueError: Image isn't a 2d image

        Returns:
            np.array: Output image increased by num of iteration
        """
        if len(image.shape) > 2:
            raise ValueError("Image isn't a 2d image")
        return image + iteration
