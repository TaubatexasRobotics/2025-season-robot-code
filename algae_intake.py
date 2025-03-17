import wpilib
import rev
from wpimath.controller import PIDController
import constants

class AlgaeIntake:
    def __init__(self):
        self.intake_motion = rev.SparkMax(constants.INTAKE_MOTION_ID, rev.SparkLowLevel.MotorType.kBrushless)
        self.intake_rotation = rev.SparkMax(constants.INTAKE_ROTATION_ID, rev.SparkLowLevel.MotorType.kBrushless)

        self.encoder_virtual = 0

        self.limit_switch = wpilib.DigitalInput(constants.LIMIT_SWITCH_INTAKE_PORT)

        self.pid = PIDController(*constants.PID_INTAKE)

        self.pid.setTolerance(1,1)

        self.control_val = 0

    def go_to_position(self,setpoint):
        self.intake_motion.set(self.pid.calculate(self.intake_motion.getEncoder().getPosition(), setpoint))
        #print(self.pid.calculate(self.intake_motion.getEncoder().getPosition(), setpoint))

    def reset_intake(self):
        self.intake_motion.getEncoder().setPosition(0)

    def reajust_encoder(self):
        if self.limit_switch.get() is False:
            self.intake_motion.getEncoder().setPosition(0)

    def intake_receiving_position(self):
        self.go_to_position(25)
        
    def intake_removing_position(self):
        self.go_to_position(50)
        
    def intake_reset_position(self):
        self.go_to_position(3)

    def reset_intake(self):
        self.intake_motion.set(-1)
        
    def testeI(self):
        print(self.intake_motion.getEncoder().getPosition())

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
