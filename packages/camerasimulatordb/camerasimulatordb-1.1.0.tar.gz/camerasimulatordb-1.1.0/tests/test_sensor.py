"""This module have the tests for sensor processor class
"""
import pytest
from skimage import data
from .context import camerasimulatordb


class TestSensor:
    """Test for Sensor processor class
    """

    def test_init(self):
        """This method test the initialization for a sensor processor.
            Checking the sensor processor object properties are the expected properties
        """
        sensor_processor = camerasimulatordb.Sensor(
            20, True,
        )

        assert sensor_processor.get_gain() == 20
        assert sensor_processor.get_enable()

    def test_iter(self):
        """This method test the object returned by iter method is the Sensor object expected
        """
        sensor_processor = camerasimulatordb.Sensor(
            20, True,
        )
        assert iter(sensor_processor) == sensor_processor

    def test_next(self):
        """This method test the iterable process
            Checking the returned image matches with the original
            image increased by the number of iteration
        """
        scikit_coins = data.coins()
        sensor_processor = camerasimulatordb.Sensor(
            20, True, [scikit_coins for _ in range(15)]
        )
        sensor_iter = iter(sensor_processor)
        iternum = 0

        for processed_image in sensor_iter:
            iternum += 1
            assert (processed_image == (scikit_coins + iternum-1)).all()

    def test_set_properties(self):
        """This method test the setters for sensor properties
            Checking the sensor processor object properties was changed
        """
        sensor_processor = camerasimulatordb.Sensor(
            20, True,
        )

        sensor_processor.set_enable(False)
        sensor_processor.set_gain(25)

        assert sensor_processor.get_gain() != 20
        assert sensor_processor.get_gain() == 25
        assert ~sensor_processor.get_enable()

    def test_process_error_dim(self):
        """This method test raised error from process image
            Checking the image shape isn't a 2d image
        """
        scikit_cat = data.chelsea()
        sensor_processor = camerasimulatordb.Sensor(
            5, True,
        )
        with pytest.raises(ValueError) as error_info:
            sensor_processor.process(scikit_cat)

        assert error_info.type is ValueError
        assert error_info.value.args[0] == "Image isn't a 2d image"

    def test_process_success(self):
        """This method test a success process image
            Checking the returned image is equal to the input image scaled by 5
        """
        scikit_coins = data.coins()
        image_shape = scikit_coins.shape
        sensor_processor = camerasimulatordb.Sensor(
            5, True,
        )
        scikit_coins_processed = sensor_processor.process(
            image=scikit_coins, height=image_shape[0], width=image_shape[1])

        assert (scikit_coins_processed[0] == 5*scikit_coins).all()
        assert (scikit_coins_processed[1] == scikit_coins).all()

    def test_iteration_process(self):
        """This method test the process for iterable processes
            Checking the returned image matches with the original image
            increased by the number of iteration
        """
        scikit_coins = data.coins()
        sensor_processor = camerasimulatordb.Sensor(5, True)
        for i in range(5):
            assert (sensor_processor.iteration_process(
                scikit_coins, i) == (scikit_coins + i)).all()
