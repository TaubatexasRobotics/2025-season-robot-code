import wpilib
import rev
import constants
from typing import Literal
from wpimath.controller import PIDController
#from pixycam import PixyCam

class AlgaeIntake:
    def __init__(self):
        self.arm_pivot_motor = rev.SparkMax(constants.INTAKE_MOTION_ID, rev.SparkLowLevel.MotorType.kBrushless)
        self.rotation_motor = rev.SparkMax(constants.INTAKE_ROTATION_ID, rev.SparkLowLevel.MotorType.kBrushless)
        self.lower_limit_switch = wpilib.DigitalInput(constants.LIMIT_SWITCH_INTAKE_PORT)
        self.pid = PIDController(*constants.PID_INTAKE)
        self.motor_response = 0
        self.pid.setTolerance(1,1)
        self.setpoint = 10
        self.arm_encoder = self.arm_pivot_motor.getEncoder()
        self.arm_control_type: Literal["position", "duty_cycle"] = "position"
        self.arm_positions = constants.ARM_POSITIONS
        self.target_position: Literal["REMOVING", "RECEIVING", "HOMING"] = "HOMING"

        #self.pixycam = PixyCam(constants.BAUD_RATE)

    def dashboardInit(self, dashboard) -> None:
        self.arm_positions["HOMING"] = dashboard.putNumber("Homing Position", constants.ARM_POSITIONS["HOMING"])
        self.arm_positions["RECEIVING"] = dashboard.putNumber("Receiving Position", constants.ARM_POSITIONS["RECEIVING"])
        self.arm_positions["REMOVING"] = dashboard.putNumber("Removing Position", constants.ARM_POSITIONS["REMOVING"])

    def updateDashboard(self, dashboard) -> None:
        dashboard.putData("PID Intake Arm", self.pid)
        dashboard.putNumber("Arm Angle", self.arm_encoder.getPosition())
        dashboard.putBoolean("Arm on position mode", self.arm_control_type == "position")
        dashboard.putBoolean("Arm on duty cycle mode", self.arm_control_type == "duty_cycle")
        dashboard.putNumber("Setpoint", self.setpoint)  
        dashboard.putNumber("Motor Response", self.motor_response)
        dashboard.putBoolean("Limit Switch", self.lower_limit_switch.get())

        self.arm_positions["HOMING"] = dashboard.getNumber("Homing Position", constants.ARM_POSITIONS["HOMING"])
        self.arm_positions["RECEIVING"] = dashboard.getNumber("Receiving Position", constants.ARM_POSITIONS["RECEIVING"])
        self.arm_positions["REMOVING"] = dashboard.getNumber("Removing Position", constants.ARM_POSITIONS["REMOVING"])

    def robotPeriodic(self):
        self.update_encoder()

    def teleopPeriodic(self):
        if self.arm_control_type == "position":
            self.motor_response = self.pid.calculate(self.arm_encoder.getPosition(), self.setpoint)
            if(self.is_arm_homed() and self.motor_response > 0): self.motor_response = 0
            
            self.arm_pivot_motor.set(self.motor_response)

    #def detect_algae(self):
        #if self.pixycam.get_algae_size()[0] < constants.ALGAE_WIDTH:
            #self.go_to_position(self.arm_positions[constants.ARM_POSITIONS["HOMING"]])

    def go_to_position(self, setpoint):
        self.setpoint = setpoint

    def reset_intake(self):
        self.arm_encoder.setPosition(0)

    def update_encoder(self):
        if self.is_arm_homed():
            self.arm_encoder.setPosition(0)

    def is_at_setpoint(self):
        return self.pid.atSetpoint()
    
    def intake_absorb(self):
        self.rotation_motor.set(constants.INTAKE_ROTATION_SPEED)

    def deactivate_intake(self):
        self.rotation_motor.set(0)

    def intake_expel(self):
        self.rotation_motor.set(-constants.INTAKE_ROTATION_SPEED)

    def is_arm_homed(self):
        return not self.lower_limit_switch.get()
    
    def move_arm_by_duty_cycle(self, axis_value:float) -> None:
        if(self.is_arm_homed() and axis_value > 0): return
        self.motor_response = axis_value * 0.5
        self.arm_pivot_motor.set(self.motor_response)
