import wpilib
import wpilib.drive
from ClimberSys import Climber
from Drivetrain import driveTrain
from buttons import dualshock4, g_xbox_360
from Intake import Intake

# from ClimbSys import ElevationSys

class TestRobot(wpilib.TimedRobot):
    def robotInit(self):

        self.climber = Climber()
        self.drivetrain = driveTrain()
        self.intake = Intake()

        self.dualshock4 = wpilib.Joystick(0)
        self.xbox_360 = wpilib.Joystick(1)

         
        
        # self.elevation = ElevationSys()

        self.r_encoder = wpilib.Encoder(4, 5)
        self.l_encoder = wpilib.Encoder(2, 3)

        self.pulsos_p_m_r = 4753
        self.pulsos_p_m_l = 2839

        
        self.chooser = wpilib.SendableChooser()
        self.defaultController_option = "dois controles"
        self.steering_wheel_option = "volante"
        wpilib.SmartDashboard.putNumber("Encoder Left", 0)
        wpilib.SmartDashboard.putNumber("Encoder Right", 0)

    def robotPeriodic(self):
        self.left_pulses = self.l_encoder.get()
        self.right_pulses = self.r_encoder.get()
        self.left_position = self.left_pulses /self.pulsos_p_m_l
        self.right_position = self.right_pulses /self.pulsos_p_m_r
        
        #print("left position:", self.left_pulses)
        #print("right position:", self.right_pulses)
        wpilib.SmartDashboard.putNumber("Encoder Left", self.left_pulses)
        wpilib.SmartDashboard.putNumber("Encoder Right", self.right_pulses)

    def autonomousInit(self):
        pass

    def autonomousPeriodic(self):
        pass

    def teleopInit(self):
        self.drivetrain.safetyProgram()

        self.intake.intake_zera_encoder()
        
        
    def teleopPeriodic(self):
        
        if self.dualshock4.getRawButton(dualshock4["cross"]):
            self.drivetrain.slowdrive()
        else:
            self.drivetrain.arcadeDrive()
        
        self.climber.climberControl()

        self.intake.intake_control()

        