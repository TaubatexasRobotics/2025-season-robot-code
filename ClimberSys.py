import wpilib
import phoenix5
import wpilib.drive
from buttons import g_xbox_360

class Climber():
    def __init__(self):


        self.climber = phoenix5.WPI_VictorSPX(12)

        self.second_controller = wpilib.Joystick(1)


    def climberControl(self):
        rt_value = self.second_controller.getRawAxis(g_xbox_360['right-trigger-axis'])
        lt_value = self.second_controller.getRawAxis(g_xbox_360['left-trigger-axis'])

        combined_value =  rt_value - lt_value
        self.climber.set(combined_value)
        