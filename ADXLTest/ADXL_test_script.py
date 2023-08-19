from zip_test_fwk import ZipTestBoard
import time

def handle_fail(start: float, error: Exception):
    stop=time.perf_counter()
    print(f"TEST FAILED in {stop-start} sec due to: {error}")
    return


def config_accelerometer(board: ZipTestBoard) -> None:
    """Configure the accelerometer to output x,y,z measurements at the max data rate"""
    board.turn_on_ps("1V8")
    board.turn_on_ps("2V5")
    board.i2c_setup("MCU_DIO_2", "MCU_DIO_1", 400)
    return


def run_and_validate_self_test(board: ZipTestBoard):
    """Run self test protocol"""
    board.i2c_cmd("0x2C",["0x00"], 0)
    board.i2c_cmd("0x31",["0x08"], 0) # 2 byte responses
    board.i2c_cmd("0x")
    # response = 
    # if response:
    #     ...
    # else:
    #     raise Exception("no response from self test")






def main():
    start = time.perf_counter()

    try:
        board = ZipTestBoard()
    except Exception as e:
        return handle_fail(start, e)

    try:
        config_accelerometer(board)
    except Exception as e:
        return handle_fail(start, e)
    
    try:
        run_and_validate_self_test(board)
    except Exception as e:
        return handle_fail(start, e)
    


    


if __name__ == "__main__":
    main()