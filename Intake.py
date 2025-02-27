import wpilib
import rev
from buttons import g_xbox_360
from wpimath.controller import PIDController
import math

class Intake():
    
    def __init__(self):

        self.intake_motion = rev.SparkMax(50, rev.SparkLowLevel.MotorType.kBrushless)
        self.intake_rotation = rev.SparkMax(52, rev.SparkLowLevel.MotorType.kBrushless)

        self.second_controller = wpilib.Joystick(1)

        self.encoder_virtual = 0

        self.limit_switch = wpilib.DigitalInput(0)

        self.pid = PIDController(0.02,0.01,0)

        self.pid.setTolerance(1,1)

        self.xbox_360 = wpilib.Joystick(1)

        self.controle_var = 0
        


    def go_to_position(self,setpoint):
        self.intake_motion.set(self.pid.calculate(self.intake_motion.getEncoder().getPosition(), setpoint))
        print(self.pid.calculate(self.intake_motion.getEncoder().getPosition(), setpoint))

    def intake_zera_encoder(self):
        self.intake_motion.getEncoder().setPosition(0)

    def reajust_encoder(self):
        if self.limit_switch.get() == 1:
            self.intake_motion.getEncoder().setPosition(0)
        else:
            pass


    def intake_receiving_position(self):
        self.go_to_position(30)
        
    def intake_removing_position(self):
        self.go_to_position(50)
        
    def intake_rest_position(self):
        self.go_to_position(0)
        
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

    def intake_control(self):
        if self.xbox_360.getRawButton(g_xbox_360["x"]):
            self.intake_expel()
        elif self.xbox_360.getRawButton(g_xbox_360["a"]): 
            self.intake_absorb()
        else:
            self.deactivate_intake()

        #controle das posições do intake
            
        if self.xbox_360.getRawButtonPressed(g_xbox_360["y"]):
            self.controle_var = 2
            
        if self.xbox_360.getRawButtonPressed(g_xbox_360["b"]):
            self.controle_var = 1
            
        if self.xbox_360.getRawButtonPressed(g_xbox_360["press_left_stick"]):
            self.controle_var = 0
           
        match self.controle_var:
            case 0:
                self.intake_rest_position()
            case 1:
                self.intake_receiving_position()
            case 2:
                self.intake_removing_position()



    