import wpilib
import wpilib.drive
import phoenix5
from buttons import dualshock4 as ds_keymap

class driveTrain():
    def __init__(self):
    # Initialize motors using CAN IDs
        self.left_front_motor = phoenix5.WPI_VictorSPX(4)
        self.left_rear_motor = phoenix5.WPI_VictorSPX(3) 
        # self.left_rear_motor.setInverted(True)

        self.right_front_motor = phoenix5.WPI_VictorSPX(1)
        self.right_rear_motor = phoenix5.WPI_VictorSPX(2)

        # Group left and right motors
        self.left = wpilib.MotorControllerGroup(self.left_front_motor, self.left_rear_motor)
        self.right = wpilib.MotorControllerGroup(self.right_front_motor, self.right_rear_motor)

        self.right.setInverted(True)

        # # Set up differential drive for arcade driving
        self.robot_drive = wpilib.drive.DifferentialDrive(self.left, self.right)

        self.dualshock4 = wpilib.Joystick(0)
    
    

    def axis_X(self):
        if self.dualshock4.getRawAxis(ds_keymap[""]):
            return 1.0
        elif self.dualshock4.getRawButton(ds_keymap["lb"]):
            return -1.0
        elif self.dualshock4.getRawButton(ds_keymap["a"]):
            return 0.3
        elif self.dualshock4.getRawButton(ds_keymap["x"]):
            return -0.3        
        else:
            return 0
        
    def safetyProgram(self):
        self.robot_drive.setExpiration(0.1)
        self.robot_drive.setSafetyEnabled(True)

    def arcadeDrive(self):
        # Get steering_wheel axis values for movement and rotation

        move_value = -(self.dualshock4.getRawAxis(ds_keymap["left-trigger-axis"]) -
             self.dualshock4.getRawAxis(ds_keymap["right-trigger-axis"]) )

        # move_value = self.axis_X()  # Y-axis
        rotate_value = -self.dualshock4.getRawAxis(ds_keymap["left-x-axis"])  # X-axis

        # Use arcade drive to move the robot
        self.robot_drive.arcadeDrive(move_value, rotate_value)