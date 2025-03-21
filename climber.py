import wpilib
import phoenix5
import constants

class Climber:
    def __init__(self):
        self.climber = phoenix5.WPI_VictorSPX(constants.CLIMBER_ID)
        self.detect = wpilib.DigitalInput(2)
        self.light = wpilib.Relay(0)

    def climberControl(self, left, right):
        combined_value = right - left
        self.climber.set(combined_value)
        
    def climbUp(self):
        self.climber.set(1)
    
    def climbDown(self):
        self.climber.set(-1)
        
    def idle(self):
        self.climber.set(0)
        
    def startMotor(self) -> None:
        self.climber.setNeutralMode(phoenix5.NeutralMode.Coast)

    def finishMotor(self) -> None:
        self.climber.setNeutralMode(phoenix5.NeutralMode.Brake)
    
    def isFinished(self) -> None:
        if self.detect.get() is False:
            self.light.set(wpilib.Relay.Value.kOn)
        else:
            self.light.set(wpilib.Relay.Value.kOff)
