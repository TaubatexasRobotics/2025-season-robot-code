import wpilib
import wpilib.drive
import phoenix5

class Drivetrain:
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

        # Setup differential drive for arcade drive
        self.robot_drive = wpilib.drive.DifferentialDrive(self.left, self.right)
        self.r_encoder = wpilib.Encoder(4, 5)
        self.l_encoder = wpilib.Encoder(2, 3)

        wpilib.SmartDashboard.putNumber("Encoder Left", 0)
        wpilib.SmartDashboard.putNumber("Encoder Right", 0)

    def updateEncoders(self) -> None:
        self.pulsos_p_m_r = 4753
        self.pulsos_p_m_l = 2839
        self.left_pulses = self.l_encoder.get()
        self.right_pulses = self.r_encoder.get()
        self.left_position = self.left_pulses / self.pulsos_p_m_l
        self.right_position = self.right_pulses / self.pulsos_p_m_r
        
        wpilib.SmartDashboard.putNumber("Encoder Left", self.left_pulses)
        wpilib.SmartDashboard.putNumber("Encoder Right", self.right_pulses)

    def safetyMode(self):
        self.robot_drive.setExpiration(0.1)
        self.robot_drive.setSafetyEnabled(True)

    def arcadeDrive(self, fwd_left, fwd_right, turn):
        # Get steering_wheel axis values for movement and rotation
        move_value = -(fwd_left - fwd_right)

        # move_value = self.axis_X()  # Y-axis

        # Use arcade drive to move the robot
        self.robot_drive.arcadeDrive(move_value, turn)

    def slowdrive(self, fwd_left, fwd_right, turn):
        # Get steering_wheel axis values for movement and rotation
        move_value = -(fwd_left - fwd_right)

        # move_value = self.axis_X()  # Y-axis

        # Use arcade drive to move the robot
        self.robot_drive.arcadeDrive((move_value/2.6), (turn/1.5))
        print(move_value/1.5, turn/2)
