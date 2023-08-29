"""This module has the base processor to be inherited by specific processors
"""
import abc
import numpy as np


class BaseProcessor:
    """Base class to processors

    Attributes:
        enable (bool): Value of enable property to base processor
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, enable: bool):
        self.__enable = enable

    def get_enable(self) -> bool:
        """Enable property getter method

        Returns:
            bool: Value of enable property
        """
        return self.__enable

    def set_enable(self, enable: bool):
        """Enable property setter method

        Args:
            enable (bool): New value for enable property
        """
        self.__enable = enable

    @abc.abstractmethod
    def process(self, image: np.array) -> np.array:
        """Abstract method to process 2D numpy data(image)

        Args:
            image (np.array): Input image to be process

        Returns:
            np.array: Output processed image
        """
        return image
