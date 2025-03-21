import phoenix5
import constants

class CoralIntake:
    def __init__(self) -> None:
        self.motor = phoenix5.WPI_VictorSPX(constants.CORAL_INTAKE_ID)
    
    def enable(self) -> None:
        self.motor.set(0.5)
    
    def disable(self) -> None:
        self.motor.set(0)
    
    def invert(self) -> None:
        self.motor.set(-0.8)

    def enable_half(self) -> None:
        self.motor.set(0.4)

    def invert_half(self) -> None:
        self.motor.set(-0.4)
