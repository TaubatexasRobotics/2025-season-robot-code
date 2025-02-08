import wpilib
import phoenix5
import wpilib.drive
from buttons import dualshock4


class Climber():
    def __init__(self):

        self.left_climber = phoenix5.WPI_VictorSPX(12)
        self.right_climber = phoenix5.WPI_VictorSPX(9)
        self.right_climber.setInverted(True)


        self.climber = wpilib.MotorControllerGroup(self.left_climber,self.right_climber)

        self.dualshock_4 = wpilib.Joystick(1)

    def climberControl (self):
        if self.dualshock_4.getRawButton(dualshock4["l1"]):
            self.climber.set(-1.0)

        elif self.dualshock_4.getRawButton(dualshock4["r1"]):
            self.climber.set(1.0)
        else:
            self.climber.set(0)
        
        


    def individualControl(self):

        self.right_climber.set((self.dualshock_4.getRawAxis(5)*-1))
        self.left_climber.set((self.dualshock_4.getRawAxis(1)*-1))