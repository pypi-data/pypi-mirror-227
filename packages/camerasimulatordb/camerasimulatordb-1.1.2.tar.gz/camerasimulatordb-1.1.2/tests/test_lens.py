"""This module have the tests for lens processor class
"""
import pytest
from skimage import data
from .context import camerasimulatordb
class TestLens:
    """Test for Lens processor class
    """
    def test_init(self):
        """This method test the initialization for a lens processor.
            Checking the lens processor object properties are the expected properties
        """
        lens_processor = camerasimulatordb.Lens(
            200, 200, True,
        )

        assert lens_processor.get_height() == 200
        assert lens_processor.get_width() == 200
        assert lens_processor.get_enable()

    def test_set_properties(self):
        """This method test the setters for lens properties
            Checking the lens processor object properties was changed
        """
        lens_processor = camerasimulatordb.Lens(
            200, 200, True,
        )

        lens_processor.set_enable(False)
        lens_processor.set_height(250)
        lens_processor.set_width(250)

        assert lens_processor.get_height() != 200
        assert lens_processor.get_width() != 200
        assert lens_processor.get_height() == 250
        assert lens_processor.get_width() == 250
        assert ~lens_processor.get_enable()

    def test_process_error(self):
        """This method test raised error from process image
            Checking the image shape doesn't match with lens processor properties
        """
        scikit_coins = data.coins()
        lens_processor = camerasimulatordb.Lens(
            200, 200, True,
        )
        with pytest.raises(ValueError) as error_info:
            lens_processor.process(scikit_coins)

        assert error_info.type is ValueError
        assert error_info.value.args[0] == "Image shape doesn't match with lens properties"

    def test_process_error_dim(self):
        """This method test raised error from process image
            Checking the image shape isn't a 2d image
        """
        scikit_cat = data.chelsea()
        shape = scikit_cat.shape
        lens_processor = camerasimulatordb.Lens(
            shape[0], shape[1], True,
        )
        with pytest.raises(ValueError) as error_info:
            lens_processor.process(scikit_cat)

        assert error_info.type is ValueError
        assert error_info.value.args[0] == "Image isn't a 2d image"

    def test_process_success(self):
        """This method test a success process image
            Checking the returned image is equal to the input image 
        """
        scikit_coins = data.coins()
        shape = scikit_coins.shape
        lens_processor = camerasimulatordb.Lens(
            shape[0], shape[1], True,
        )

        assert (lens_processor.process(scikit_coins) == scikit_coins).all()
