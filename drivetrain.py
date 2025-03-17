import wpilib
import wpilib.drive
import phoenix5
import constants
import wpimath.geometry
from typing import Optional

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

        #self.left_front_motor.setNeutralMode(phoenix5.NeutralMode.Brake)
        #self.left_back_motor.setNeutralMode(phoenix5.NeutralMode.Brake)

        #self.right_front_motor.setNeutralMode(phoenix5.NeutralMode.Brake)
        #self.right_back_motor.setNeutralMode(phoenix5.NeutralMode.Brake)

        # Group left and right motors
        self.left = wpilib.MotorControllerGroup(self.left_front_motor, self.left_back_motor)
        self.right = wpilib.MotorControllerGroup(self.right_front_motor, self.right_back_motor)

        self.right.setInverted(True)

        # Setup differential drive for arcade drive
        self.drivetrain = wpilib.drive.DifferentialDrive(self.left, self.right)
        self.r_encoder = wpilib.Encoder(constants.RIGHT_ENCODER_A, constants.RIGHT_ENCODER_B)
        self.l_encoder = wpilib.Encoder(constants.LEFT_ENCODER_A, constants.LEFT_ENCODER_B)

        self.navx = AHRS.create_spi()
        self.navx.reset()

        self.field = wpilib.Field2d()
        rotation = wpimath.geometry.Rotation2d.fromDegrees(self.navx.getAngle())
        initial_pose = wpimath.geometry.Pose2d(*constants.INITIAL_POSE)
        self.odometry = wpimath.kinematics.DifferentialDriveOdometry(rotation, 0, 0, initial_pose)

        self.pid_angular = PIDController(*constants.PID_ANGULAR_DRIVETRAIN)
        self.pid_angular.enableContinuousInput(-180, 180)
        self.pid_angular.setSetpoint(180)

        self.camera = AprilTagCamera(constants.PHOTONVISION_CAMERA_NAME) 

        wpilib.SmartDashboard.putData("PID Angular Drivetrain", self.pid_angular)

    def updateData(self) -> None:
        self.pulsos_p_m_r = 4753
        self.pulsos_p_m_l = 2839
        self.left_pulses = self.l_encoder.get()
        self.right_pulses = self.r_encoder.get()
        self.left_position = self.left_pulses / self.pulsos_p_m_l
        self.right_position = self.right_pulses / self.pulsos_p_m_r

        rotation = wpimath.geometry.Rotation2d.fromDegrees(self.navx.getAngle())
        self.odometry.update(rotation, self.left_position, self.right_position)

        wpilib.SmartDashboard.putNumber("Encoder Left", self.left_pulses)
        wpilib.SmartDashboard.putNumber("Encoder Right", self.right_pulses)
        wpilib.SmartDashboard.putData("navX", self.navx)
        
        self.timer = wpilib.Timer()
        self.timer.reset()

    def reset(self) -> None:
        self.drivetrain.arcadeDrive(0, 0)

    def safetyMode(self):
        self.drivetrain.setExpiration(0.1)
        self.drivetrain.setSafetyEnabled(True)

    def arcadeDrive(self, fwd_left, fwd_right, turn) -> None:
        move_value = -(fwd_left - fwd_right)

        # Use arcade drive to move the robot
        self.drivetrain.arcadeDrive(move_value, turn)
    
    def myArcadeDrive(self, fwd_left, fwd_right, turn) -> None:
        forward = -(fwd_left - fwd_right)

        left = forward + turn
        right = forward - turn
        
        self.left.set(left)
        self.right.set(right * 0.8)

    def arcadeDriveAlign(self, tag: int) -> None:
        yaw = self.camera.getYaw(tag)
        turn = self.pid_angular.calculate(yaw, 0) if yaw != -1 else 0
        self.drivetrain.arcadeDrive(0, turn)

    def turnToDegrees(self, setpoint: Optional[int]) -> None:
        turn = 0

        turn = self.pid_angular.calculate(self.navx.getAngle(), self.pid_angular.getSetpoint())
        self.drivetrain.arcadeDrive(0, turn)

    def slowdrive(self, fwd_left, fwd_right, turn) -> None:
        move_value = -(fwd_left - fwd_right)

        # Use arcade drive to move the robot
        self.drivetrain.arcadeDrive((move_value/2.6), (turn/1.5))
