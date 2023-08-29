# camerasimulatordb
    Basic lens and sensor simulator

    Github repo: https://github.com/DanBeltranuwu/camera-simulator
    PypI package: https://pypi.org/project/camerasimulatordb

## Tests
### Test Lens
- Init class test to check the lens processor object properties are the expected properties.
- Setter methods test to check the lens processor object properties was changed.
- Process method shape error test to check the image shape doesn't match with lens processor properties.
- Process method dimension error test to check the image shape isn't a 2d image.
- Process method test to check the returned image is equal to the input image.

### Test Sensor
- Init class test to check the sensor processor object properties are the expected properties.
- Iter class test to check the object returned by iter method is the Sensor object expected.
- Next class test to check the returned image matches with the original image increased by the number of iteration.
- Setter methods test to check the sensor processor object properties was changed.
- Process method dimension error test to check the image shape isn't a 2d image.
- Process method test to check the returned image is equal to the input image scaled by 5.
- Iteration process method test to check the returned image matches with the original image increased by the number of iteration.

