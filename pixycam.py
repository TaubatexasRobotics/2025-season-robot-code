import wpilib
import constants

class PixyCam:
    def __init__(self) -> None:
        self.arduino = wpilib.SerialPort(constants.BAUD_RATE, wpilib.SerialPort.Port.kUSB1)
    
    def getDistance(self) -> float:
        if self.arduino.getBytesReceived() <= 0:
            return -1
        buffer = bytearray(self.arduino.getBytesReceived())
        sz = self.arduino.read(buffer)
        return float(buffer[:sz].decode("ascii"))
