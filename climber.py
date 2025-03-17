import wpilib
import phoenix5

class Climber:
    def __init__(self):
        self.climber = phoenix5.WPI_VictorSPX(12)

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
