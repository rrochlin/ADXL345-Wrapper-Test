class ZipTestBoard: 

    def __init__() -> None:
        """Raises ConnectionError on fail"""
        ...

    def turn_on_ps(supply: str) -> None:
        """Turns on PS for provided string arg"""
        ...
    
    def turn_off_ps(supply: str) -> None:
        """Turns off PS for provided string arg"""
        ...

    def i2c_setup(sda: str, scl: str, freq: int) -> None:
        """
        Turns on provided string sda and scl pins as seen in diagram "MCU_DIO1"
        and integer frequency in Hz
        """
        ...
    
    def i2c_cmd(addr: str, data: list[str], resp_len: int=0) -> list[str]|int:
        """
        Writes a byte list data to the provided address addr expecting 
        response of length resp_len. 0 means no response. Raises I2CError on exception
        """
        ...
    
    def actuator_move(config: str) -> None:
        """
        function "blocks" the thread...
        Config options: "slow_climb", "sharp_turn", "quick_drop"
        Raises ActuatorError exception on fail
        """
        ...