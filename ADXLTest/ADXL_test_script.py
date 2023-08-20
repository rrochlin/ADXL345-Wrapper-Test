from zip_test_fwk import ZipTestBoard
import time
import threading

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


def handle_fail(start: float, error: Exception) -> None:
    stop=time.perf_counter()
    print(f"TEST FAILED in {stop-start} sec due to: {error}")
    return

def validate_xyz(board: ZipTestBoard, x_range: tuple=None, y_range: tuple=None, z_range: tuple=None) -> None:
    # Gs = Measurement Value * (G-range/(2^10)) or Gs = Measurement Value * (32/1024)
    response = board.i2c_cmd(ADXL345_READ_ADDRESS, REGISTER_X_AXIS_LSB, 6)
    if x_range:
        x = ((response[1]<<8) | response[0])*0.03125
        assert (x_range[0] <= x) and (x_range[1] >= x), f"x_values fall outside of range{x}"
    if y_range:
        y = ((response[2]<<8) | response[3])*0.03125
        assert (y_range[0] <= y) and (y_range[1] >= y), f"y_values fall outside of range {y}"
    if y_range:
        z = ((response[4]<<8) | response[5])*0.03125
        assert (z_range[0] <= z) and (z_range[1] >= z), f"z_values fall outside of range {z}"


def config_accelerometer(board: ZipTestBoard) -> None:
    """Configure the accelerometer to output x,y,z measurements at the max data rate"""
    board.turn_on_ps("1V8")
    board.turn_on_ps("2V5")
    board.i2c_setup("MCU_DIO_2", "MCU_DIO_1", 400)

    # set to low power mode
    bw_rate_state = board.i2c_cmd(ADXL345_READ_ADDRESS, BW_RATE, 1)[0]
    board.i2c_cmd(BW_RATE, bw_rate_state & ~0x10, 0)

    # set range to +/- 16g
    initial_data_format = board.i2c_cmd(ADXL345_READ_ADDRESS, DATA_FORMAT_REGISTER, 1)[0]
    board.i2c_cmd(DATA_FORMAT_REGISTER, initial_data_format & ~0x03, 0)
    return


def run_and_validate_self_test(board: ZipTestBoard) -> None:
    """Run self test protocol"""

    # get current state of DATA_FORMAT register
    initial_data_format = board.i2c_cmd(ADXL345_READ_ADDRESS, DATA_FORMAT_REGISTER, 1)[0]

    # make sure test bit is 0 and get initial acceleration values
    board.i2c_cmd(DATA_FORMAT_REGISTER, initial_data_format & ~0x80, 0)
    response = board.i2c_cmd(ADXL345_READ_ADDRESS, REGISTER_X_AXIS_LSB, 6)
    test_0_xyz = [(response[1]<<8) | response[0], (response[2]<<8) | response[3], (response[4]<<8) | response[5]]

    # set test bit to 1
    board.i2c_cmd(DATA_FORMAT_REGISTER, initial_data_format | 0x80, 0)
    response = board.i2c_cmd(ADXL345_READ_ADDRESS, REGISTER_X_AXIS_LSB, 6)
    test_1_xyz = [(response[1]<<8) | response[0], (response[2]<<8) | response[3], (response[4]<<8) | response[5]]

    tolerance = 0.01  # checking that results are within 0.01
    ratios = [abs(1 - b/a) for (a,b) in zip(test_0_xyz, test_1_xyz)]
    for ratio in ratios:
        assert ratio < tolerance, "self test results are not within tolerance"

    # Turn test bit off
    board.i2c_cmd(DATA_FORMAT_REGISTER, initial_data_format & ~0x80, 0)
    return


def run_slow_climb(board: ZipTestBoard) -> None:
    thread = threading.Thread(target=board.actuator_move, args=("slow_climb",))
    thread.start()
    time.sleep(0.1) # pause for 0.1 seconds to allow function to start
    while (thread.is_alive()):
        validate_xyz(board, y_range=(-1,1), z_range=(6,8))
        time.sleep(0.1) # pause for 0.1 seconds to catch process ending
    thread.join()
    return


def run_sharp_turn(board: ZipTestBoard) -> None:
    thread = threading.Thread(target=board.actuator_move, args=("sharp_turn",))
    thread.start()
    time.sleep(0.1)  # pause for 0.1 seconds to allow function to start
    while (thread.is_alive()):
        validate_xyz(board, x_range=(5,16), y_range=(5,16))
        time.sleep(0.1)  # pause for 0.1 seconds to catch process ending
    thread.join()
    return


def run_quick_drop(board: ZipTestBoard) -> None:
    thread = threading.Thread(target=board.actuator_move, args=("quick_drop",))
    thread.start()
    time.sleep(0.1)  # pause for 0.1 seconds to allow function to start
    threading.Thread()
    while (thread.is_alive()):
        validate_xyz(board, z_range=(-16,-8))
        time.sleep(0.1)  # pause for 0.1 seconds to catch process ending
    thread.join()
    return


def main():
    start = time.perf_counter()
    try:
        board = ZipTestBoard()
    except Exception as e:
        return handle_fail(start, e)

    tests = [
        config_accelerometer,
        run_and_validate_self_test,
        run_slow_climb,
        run_sharp_turn,
        run_quick_drop
        ]

    for test in tests:
        try:
            test(board)
        except Exception as e:
            return handle_fail(start, e)

    stop=time.perf_counter()
    print(f"TEST PASSED in {stop-start} sec")


if __name__ == "__main__":
    main()
