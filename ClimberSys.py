import wpilib
import phoenix5
import wpilib.drive
from buttons import g_xbox_360

class Climber():
    def __init__(self):

        self.left_climber = phoenix5.WPI_VictorSPX(12)
        self.right_climber = phoenix5.WPI_VictorSPX(9)
        self.right_climber.setInverted(True)


        self.climber = wpilib.MotorControllerGroup(self.left_climber,self.right_climber)

        self.second_controller = wpilib.Joystick(1)

    def climberControl (self):
        isRbPressed = self.second_controller.getRawButton(g_xbox_360["rb"])
        isLbPressed = self.second_controller.getRawButton(g_xbox_360["lb"])

        if isLbPressed or isRbPressed:
            self.individualControl()
        else:
            self.climbCombined()

    def climbCombined(self):
        rt_value = self.second_controller.getRawAxis(g_xbox_360['right-trigger-axis'])
        lt_value = self.second_controller.getRawAxis(g_xbox_360['left-trigger-axis'])

        combined_value =  rt_value - lt_value
        self.climber.set(combined_value)
        
    def individualControl(self):
        if self.second_controller.getRawButton(g_xbox_360["rb"]):
            self.right_climber.set(-self.second_controller.getRawAxis(g_xbox_360["left-y-stick"]))
        if self.second_controller.getRawButton(g_xbox_360["lb"]):
            self.left_climber.set(-self.second_controller.getRawAxis(g_xbox_360["left-y-stick"]))