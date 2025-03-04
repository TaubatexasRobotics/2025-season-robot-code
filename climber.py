import wpilib
import phoenix5

class Climber:
    def __init__(self):
        self.climber = phoenix5.WPI_VictorSPX(12)

    def climberControl(self, left, right):
        combined_value = right - left
        self.climber.set(combined_value)
        