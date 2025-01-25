import wpilib
import wpilib.drive
import rev
import phoenix5
from buttons import steering_wheel
# from ClimbSys import ElevationSys

class TestRobot(wpilib.TimedRobot):
    def robotInit(self):
        # Initialize motors using CAN IDs
        self.left_front_motor = rev.SparkMax(50, rev.SparkLowLevel.MotorType.kBrushed)
        self.left_rear_motor = phoenix5.WPI_VictorSPX(9) 
        # self.left_rear_motor.setInverted(True)

        self.right_front_motor = rev.SparkMax(53, rev.SparkLowLevel.MotorType.kBrushed)
        self.right_rear_motor = rev.SparkMax(52, rev.SparkLowLevel.MotorType.kBrushed)

        # Group left and right motors
        self.left = wpilib.MotorControllerGroup(self.left_front_motor, self.left_rear_motor)
        self.right = wpilib.MotorControllerGroup(self.right_front_motor, self.right_rear_motor)

        self.right.setInverted(True)

        # # Set up differential drive for arcade driving
        self.robot_drive = wpilib.drive.DifferentialDrive(self.left, self.right)

        # Initialize joystick for controlling the robot
        self.joystick = wpilib.Joystick(0)

        # self.elevation = ElevationSys()

        self.r_encoder = wpilib.Encoder(4, 5)
        self.l_encoder = wpilib.Encoder(2, 3)

        self.pulsos_p_m_r = 4753
        self.pulsos_p_m_l = 2839

        wpilib.SmartDashboard.putNumber('Encoder left', self.l_encoder.get())
        wpilib.SmartDashboard.putNumber('Encoder right' , self.r_encoder.get())


    def robotPeriodic(self):
        self.left_pulses = self.l_encoder.get()
        self.right_pulses = self.r_encoder.get()
        self.left_position = self.left_pulses /self.pulsos_p_m_l
        self.right_position = self.right_pulses /self.pulsos_p_m_r
        
        print("left position:", self.left_pulses)
        print("right position:", self.right_pulses)

    def autonomousInit(self):
        pass

    def autonomousPeriodic(self):
        pass

    def teleopInit(self):
        self.robot_drive.setExpiration(0.1)
        self.robot_drive.setSafetyEnabled(True)
        # self.elevation

    def axis_X(self):
        if self.joystick.getRawButton(steering_wheel["rb"]):
            return 1.0
        
        elif self.joystick.getRawButton(steering_wheel["lb"]):
            return -1.0
        
        elif self.joystick.getRawButton(steering_wheel["a"]):
            return 0.3
        
        elif self.joystick.getRawButton(steering_wheel["x"]):
            return -0.3
        
        else :
            return 0
        

    def teleopPeriodic(self):
        # Get joystick axis values for movement and rotation
        move_value = self.axis_X()  # Y-axis
        rotate_value = self.joystick.getRawAxis(0)  # X-axis

        # Use arcade drive to move the robot
        self.robot_drive.arcadeDrive(move_value, rotate_value)

        # self.elevation.teleop()