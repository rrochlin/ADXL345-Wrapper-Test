import time
BW_RATE = 0x2C
ADXL345_WRITE_ADDRESS = 0x3A
ADXL345_READ_ADDRESS = 0x3B
REGISTER_X_AXIS_LSB = 0x32  # x-axis data 0
REGISTER_X_AXIS_MSB = 0x33  # x-axis data 1
REGISTER_Y_AXIS_LSB = 0x34  # y-axis data 0
REGISTER_Y_AXIS_MSB = 0x35  # y-axis data 1
REGISTER_Z_AXIS_LSB = 0x36  # z-axis data 0
REGISTER_Z_AXIS_MSB = 0x37  # z-axis data 1
DATA_FORMAT_REGISTER = 0x31


class ZipTestBoard:
    def __init__(self) -> None:
        """Raises ConnectionError on fail"""
        ...

    def turn_on_ps(self, supply: str) -> None:
        """Turns on PS for provided string arg"""
        ...

    def turn_off_ps(self, supply: str) -> None:
        """Turns off PS for provided string arg"""
        ...

    def i2c_setup(self, sda: int, scl: int, freq: int) -> None:
        """
        Turns on provided string sda and scl pins as seen in diagram "MCU_DIO1"
        and integer frequency in Hz
        """
        ...

    def i2c_cmd(self, addr: int, data: int, resp_len: int = 0) -> list[int] | None:
        """
        Writes a byte list data to the provided address addr expecting
        response of length resp_len. 0 means no response. Raises I2CError on exception
        """
        if addr == ADXL345_READ_ADDRESS:
            time.sleep(0.1)
            return [0x00, 0x08] * resp_len if resp_len > 1 else [0x08]
        ...

    def actuator_move(self, config: str) -> None:
        """
        function blocks the thread...
        Config options: "slow_climb", "sharp_turn", "quick_drop"
        Raises ActuatorError exception on fail
        """
        time.sleep(10)
        ...
