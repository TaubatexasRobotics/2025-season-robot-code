import wpilib
import wpilib.drive
import phoenix5
import constants
import wpimath.geometry

from wpimath.kinematics import DifferentialDriveOdometry
from wpimath.controller import PIDController
from navx import AHRS
from camera import AprilTagCamera

class Drivetrain:
    def __init__(self):
        # Initialize motors using CAN IDs
        self.left_front_motor = phoenix5.WPI_VictorSPX(constants.LEFT_FRONT_ID)
        self.left_back_motor = phoenix5.WPI_VictorSPX(constants.LEFT_BACK_ID)

        self.right_front_motor = phoenix5.WPI_VictorSPX(constants.RIGHT_FRONT_ID)
        self.right_back_motor = phoenix5.WPI_VictorSPX(constants.RIGHT_BACK_ID)

        # Group left and right motors
        self.left = wpilib.MotorControllerGroup(self.left_front_motor, self.left_back_motor)
        self.right = wpilib.MotorControllerGroup(self.right_front_motor, self.right_back_motor)

        self.right.setInverted(True)

        # Setup differential drive for arcade drive
        self.robot_drive = wpilib.drive.DifferentialDrive(self.left, self.right)
        self.r_encoder = wpilib.Encoder(constants.RIGHT_ENCODER_A, constants.RIGHT_ENCODER_B)
        self.l_encoder = wpilib.Encoder(constants.LEFT_ENCODER_A, constants.LEFT_ENCODER_B)

        self.navx = AHRS.create_spi()
        self.navx.reset()

        self.field = wpilib.Field2d()
        rotation = wpimath.geometry.Rotation2d.fromDegrees(self.navx.getAngle())
        initial_pose = wpimath.geometry.Pose2d(*constants.INITIAL_POSE)
        self.odometry = wpimath.kinematics.DifferentialDriveOdometry(rotation, 0, 0, initial_pose)
        self.pid = PIDController(*constants.PID_ANGULAR_DRIVETRAIN)

        self.camera = AprilTagCamera(constants.PHOTONVISION_CAMERA_NAME) 

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

    def arcadeDrive(self, fwd_left, fwd_right, turn) -> None:
        move_value = -(fwd_left - fwd_right)

        # Use arcade drive to move the robot
        self.robot_drive.arcadeDrive(move_value, turn)

    def arcadeDriveAlign(self, tag: int) -> None:
        yaw = self.camera.getYaw(tag)
        turn = self.pid.calculate(yaw, 0) if yaw != -1 else 0
        self.robot_drive.arcadeDrive(0, turn)

    def slowdrive(self, fwd_left, fwd_right, turn) -> None:
        move_value = -(fwd_left - fwd_right)

        # Use arcade drive to move the robot
        self.robot_drive.arcadeDrive((move_value/2.6), (turn/1.5))
