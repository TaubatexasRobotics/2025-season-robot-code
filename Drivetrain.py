import wpilib
import wpilib.drive
import phoenix5
from buttons import steering_wheel

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

        self.steering_wheel = wpilib.Joystick(0)
    
    def axis_X(self):
        if self.steering_wheel.getRawButton(steering_wheel["rb"]):
            return 1.0
        elif self.steering_wheel.getRawButton(steering_wheel["lb"]):
            return -1.0
        elif self.steering_wheel.getRawButton(steering_wheel["a"]):
            return 0.3
        elif self.steering_wheel.getRawButton(steering_wheel["x"]):
            return -0.3        
        else:
            return 0
        
    def safetyProgram(self):
        self.robot_drive.setExpiration(0.1)
        self.robot_drive.setSafetyEnabled(True)

    def arcadeDrive(self):
        # Get steering_wheel axis values for movement and rotation
        move_value = self.axis_X()  # Y-axis
        rotate_value = self.steering_wheel.getRawAxis(steering_wheel["turn-axis"])  # X-axis

        # Use arcade drive to move the robot
        self.robot_drive.arcadeDrive(move_value, rotate_value)