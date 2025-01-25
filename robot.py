import wpilib
import wpilib.drive
import rev
import phoenix5
from buttons import steering_wheel, dualshock4
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

        # Initialize steering_wheel for controlling the robot
        self.steering_wheel = wpilib.Joystick(0)
        self.dualshock_4 = wpilib.Joystick(1)
        # self.elevation = ElevationSys()

        self.r_encoder = wpilib.Encoder(4, 5)
        self.l_encoder = wpilib.Encoder(2, 3)

        self.pulsos_p_m_r = 4753
        self.pulsos_p_m_l = 2839

        self.left_climber = phoenix5.WPI_VictorSPX(1)
        self.right_climber = phoenix5.WPI_VictorSPX(2)
        self.right_climber.setInverted(True)

        self.climber = wpilib.MotorControllerGroup(self.left_climber,self.right_climber)
        self.chooser = wpilib.SendableChooser()
        self.defaultController_option = "dois controles"
        self.steering_wheel_option = "volante"

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

    def climberControl (self):
        if self.dualshock_4.getRawButton(dualshock4["l1"]):
            return -1.0
        elif self.dualshock_4.getRawButton(dualshock4["r1"]):
            return 1.0
        else:
            return 0
        
    def teleopPeriodic(self):
        # Get steering_wheel axis values for movement and rotation
        move_value = self.axis_X()  # Y-axis
        rotate_value = self.steering_wheel.getRawAxis(steering_wheel["turn-axis"])  # X-axis

        # Use arcade drive to move the robot
        self.robot_drive.arcadeDrive(move_value, rotate_value)
        
        self.climber.set(self.climberControl())
