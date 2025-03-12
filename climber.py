import wpilib
import phoenix5
import constants

class Climber:
    def __init__(self) -> None:
        self.climber = phoenix5.WPI_VictorSPX(constants.CLIMBER_ID)

    def climber_control(self, left: float, right: float) -> None:
        combined_value = right - left
        self.climber.set(combined_value)
        
    def climb_up(self) -> None:
        self.climber.set(1)
    
    def climb_down(self) -> None:
        self.climber.set(-1)
        
    def idle(self) -> None:
        self.climber.set(0)
