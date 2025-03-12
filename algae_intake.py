import wpilib
import rev
from wpimath.controller import PIDController
import constants
from typing import Literal

class AlgaeIntake:
    def __init__(self):
        self.arm_pivot_motor = rev.SparkMax(constants.INTAKE_MOTION_ID, rev.SparkLowLevel.MotorType.kBrushless)
        self.rotation_motor = rev.SparkMax(constants.INTAKE_ROTATION_ID, rev.SparkLowLevel.MotorType.kBrushless)
        self.lower_limit_switch = wpilib.DigitalInput(constants.LIMIT_SWITCH_INTAKE_PORT)
        self.pid = PIDController(*constants.PID_INTAKE)
        self.pid.setTolerance(1,1)
        self.setpoint = 10
        self.arm_encoder = self.arm_pivot_motor.getEncoder()
        self.arm_control_type: Literal["position", "duty_cycle"] = "position"

        self.target_position: Literal["REMOVING", "RECEIVING", "HOMING"] = "HOMING"

        self.rotation_speed = 0.4

    def robotPeriodic(self):
        self.update_encoder()

    def teleopPeriodic(self):
        if self.arm_control_type == "position":
            motor_response = self.pid.calculate(self.arm_encoder.getPosition(), self.setpoint)
            if(self.is_arm_homed() and motor_response > 0): motor_response = 0
            
            self.arm_pivot_motor.set(motor_response)

    def go_to_position(self,setpoint):
        self.setpoint = setpoint

    def reset_intake(self):
        self.arm_encoder.setPosition(0)

    def update_encoder(self):
        if self.is_arm_homed():
            self.arm_encoder.setPosition(0)

    def is_at_setpoint(self):
        return self.pid.atSetpoint()
    
    def intake_absorb(self):
        self.rotation_motor.set(self.rotation_speed)

    def deactivate_intake(self):
        self.rotation_motor.set(0)

    def intake_expel(self):
        self.rotation_motor.set(-self.rotation_speed)

    def is_arm_homed(self):
        return not self.lower_limit_switch.get()
    
    def move_arm_by_duty_cycle(self, axis_value:float) -> None:
        if(self.is_arm_homed() and axis_value > 0): return
        self.arm_pivot_motor.set(axis_value*0.5)
        