import wpilib
import constants

class PixyCam:
    def __init__(self) -> None:
        self.arduino = wpilib.SerialPort(constants.BAUD_RATE, wpilib.SerialPort.Port.kUSB1)
    
    def readBytes(self, port) ->