import wpilib
import rev
from wpimath.controller import PIDController
import constants
from enum import Enum

class State(Enum):
    IDLE = 0
    OPENING = 1
    CLOSING = 2

class AlgaeIntake:
    def __init__(self):
        self.intake_motion = rev.SparkMax(constants.INTAKE_MOTION_ID, rev.SparkLowLevel.MotorType.kBrushless)
        self.intake_rotation = rev.SparkMax(constants.INTAKE_ROTATION_ID, rev.SparkLowLevel.MotorType.kBrushless)

        self.encoder_virtual = 0

        self.limit_switch = wpilib.DigitalInput(4)

        self.pid = PIDController(*constants.PID_INTAKE)

        self.pid.setTolerance(1,1)

        self.control_val = 0

        self.state = State.IDLE
        self.intake_motion.set(0)

    def go_to_position(self,setpoint):
        self.intake_motion.set(self.pid.calculate(self.intake_motion.getEncoder().getPosition(), setpoint))

    def reset_intake(self):
        self.intake_motion.getEncoder().setPosition(3)

    def reajust_encoder(self):
        print(self.intake_motion.getEncoder().getPosition())
        if self.limit_switch.get() is False and self.state == State.CLOSING:
            self.reset_intake()
            self.pid.setPID(0, 0, 0)
            self.state = State.IDLE

    def intake_receiving_position(self):
        self.go_to_position(30)
        self.pid.setPID(*constants.PID_INTAKE)
        self.state = State.OPENING
        
    def intake_removing_position(self):
        self.go_to_position(50)
        self.pid.setPID(*constants.PID_INTAKE)
        self.state = State.OPENING
        
    def intake_reset_position(self):
        self.go_to_position(3)
        self.state = State.CLOSING
        
    def testeI(self):
        print(self.intake_motion.getEncoder().getPosition())
6y
    def position(self):
        return self.pid.atSetpoint()
    
    def intake_absorb(self):
        self.intake_rotation.set(0.4)

    def deactivate_intake(self):
        self.intake_rotation.set(0)

    def intake_expel(self):
        self.intake_rotation.set(-0.4)

    def setControlVal(self, control_val) -> None:
        self.control_val = control_val
    
    def getControlVal(self) -> float:
        return self.control_val