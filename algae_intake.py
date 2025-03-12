import wpilib
import rev
from wpimath.controller import PIDController
import constants
from typing import Literal

class AlgaeIntake:
    def __init__(self):
        self.intake_motion = rev.SparkMax(constants.INTAKE_MOTION_ID, rev.SparkLowLevel.MotorType.kBrushless)
        self.intake_rotation = rev.SparkMax(constants.INTAKE_ROTATION_ID, rev.SparkLowLevel.MotorType.kBrushless)
        self.limit_switch = wpilib.DigitalInput(constants.LIMIT_SWITCH_INTAKE_PORT)
        self.pid = PIDController(*constants.PID_INTAKE)
        self.pid.setTolerance(1,1)
        self.setpoint = 10
        self.arm_control_type: Literal["position", "duty_cycle"] = "position"

    def teleopPeriodic(self):
        if self.arm_control_type == "position":
            motor_response = self.pid.calculate(self.intake_motion.getEncoder().getPosition(), self.setpoint)
            if(self.is_arm_homed() and motor_response > 0): motor_response = 0
            
            self.intake_motion.set(motor_response)

    def go_to_position(self,setpoint):
        self.setpoint = setpoint

    def reset_intake(self):
        self.intake_motion.getEncoder().setPosition(0)

    def reajust_encoder(self):
        if self.limit_switch.get() is False:
            self.intake_motion.getEncoder().setPosition(0)

    def intake_receiving_position(self):
        self.go_to_position(30)
        
    def intake_removing_position(self):
        self.go_to_position(50)
        
    def intake_reset_position(self):
        self.go_to_position(0)
        
    def testeI(self):
        print(self.intake_motion.getEncoder().getPosition())

    def is_at_setpoint(self):
        return self.pid.atSetpoint()
    
    def intake_absorb(self):
        self.intake_rotation.set(0.4)

    def deactivate_intake(self):
        self.intake_rotation.set(0)

    def intake_expel(self):
        self.intake_rotation.set(-0.4)

    def is_arm_homed(self):
        return not self.down_limit_switch.get()
    
    def move_arm_by_duty_cycle(self, axis_value:float) -> None:
        if(self.is_arm_homed() and axis_value > 0): return
        self.set_angle_duty_cycle(axis_value*0.5)
        