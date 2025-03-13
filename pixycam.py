import wpilib
import constants

class PixyCam:
    def __init__(self, baud_rate: int) -> None:
        self.arduino = wpilib.SerialPort(baud_rate, wpilib.SerialPort.Port.kUSB1)
    
    def get_algae_size(self) -> float:
        if self.arduino.getBytesReceived() <= 0:
            return -1

        buffer = bytearray(self.arduino.getBytesReceived())
        sz = self.arduino.read(buffer)
        result = buffer[:sz].decode("ascii")

        pattern = f"{dimension}:\s*(\d+)"
        match = re.search(pattern, data)
        if match:
            return float(match.group(1))

        return -1
