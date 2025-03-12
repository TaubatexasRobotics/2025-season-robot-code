import wpilib
import rev
import constants
from wpimath.controller import PIDController

class AlgaeIntake:
    def __init__(self) -> None:
        self.intake_motion = rev.SparkMax(constants.INTAKE_MOTION_ID, rev.SparkLowLevel.MotorType.kBrushless)
        self.intake_rotation = rev.SparkMax(constants.INTAKE_ROTATION_ID, rev.SparkLowLevel.MotorType.kBrushless)

        self.limit_switch = wpilib.DigitalInput(constants.LIMIT_SWITCH_INTAKE_PORT)
        self.pid = PIDController(*constants.PID_INTAKE)
        self.pid_config = self.intake_motion.getClosedLoopController()
        self.pid.setTolerance(1, 1)
        self.encoder = self.intake_motion.getEncoder()
        self.control_val = 0

    def go_to_position(self, setpoint: float) -> None:
        self.intake_motion.set(self.pid.calculate(self.encoder.getPosition(), setpoint))

    def reset_intake(self) -> None:
        self.encoder.setPosition(0)
        self.set_angle_position(0)

    def reajust_encoder(self) -> None:
        if self.arm_is_at_minimal_position():
            self.reset_intake()

    def intake_receiving_position(self) -> None:
        self.go_to_position(30)
        
    def intake_removing_position(self) -> None:
        self.go_to_position(50)
        
    def intake_reset_position(self) -> None:
        self.go_to_position(0)
        
    def intake_absorb(self) -> None:
        self.intake_rotation.set(0.4)

    def deactivate_intake(self) -> None:
        self.intake_rotation.set(0)

    def intake_expel(self) -> None:
        self.intake_rotation.set(-0.4)

    def set_control_val(self, control_val: float) -> None:
        self.control_val = control_val
    
    def get_control_val(self) -> float:
        return self.control_val
    
    def arm_is_at_minimal_position(self) -> bool:
        return not self.down_limit_switch.get()
    
    def move_arm_by_joystick(self, axis_value: float) -> None:
        if(abs(axis_value) < 0.15): return
        if(self.is_homed() and axis_value > 0): return

        self.set_angle_duty_cycle(axis_value * 0.5)

    def set_angle_duty_cycle(self, duty_cycle: float) -> None:
        self.pid_config.setReference(duty_cycle, rev.SparkLowLevel.kDutyCycle)

    def set_angle_smart_motion(self, angle: float) -> None:
        self.pid_config.setReference(angle, rev.SparkLowLevel.kSmartMotion)

    def set_angle_position(self, angle: float) -> None:
        self.pid_config.setReference(angle, rev.SparkLowLevel.kPosition)
