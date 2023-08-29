"""This module has the Lens processor
"""
import numpy as np

from .baseProcessor import BaseProcessor


class Lens(BaseProcessor):
    """Lens processor which inherit base processor

    Attributes:
        height (int): Value of height property to lens processor
        width (int): Value of width property to lens processor
    """

    def __init__(self, height: int, width: int, enable: bool):
        self.__height = height
        self.__width = width
        super().__init__(enable)

    def get_height(self) -> int:
        """Height property getter method

        Returns:
            int: Value of height property
        """
        return self.__height

    def get_width(self) -> int:
        """Width property getter method

        Returns:
            int: Value of width property
        """
        return self.__width

    def set_height(self, height: int):
        """Height property setter method

        Args:
            height (int): New value for height property
        """
        self.__height = height

    def set_width(self, width: int):
        """Width property setter method

        Args:
            width (int): New value for width property
        """
        self.__width = width

    def process(self, image: np.array, height: int = None, width: int = None) -> np.array:
        """Implementation for process abstract method to Lens processor 

        Args:
            image (np.array): Input image to be process
            height (int): Value of height to lens process if property is None, 
            if param is also None then the method use default value -> 200
            width (int): Value of width to lens process if property is None, 
            if param is also None then the method use default value -> 200

        Raises:
            ValueError: Image isn't a 2d image
            ValueError: Error if image shape doesn't match with lens properties

        Returns:
            np.array: Output image if the shape matches with lens properties
        """

        if height is None:
            height = 200
        if width is None:
            width = 200

        process_height = self.__height if self.__height is not None else height
        process_width = self.__width if self.__width is not None else width

        if image.shape == (process_height, process_width):
            return image
        if len(image.shape) > 2:
            raise ValueError("Image isn't a 2d image")

        raise ValueError("Image shape doesn't match with lens properties")
