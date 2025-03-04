import wpilib
import wpilib.drive
from climber import Climber
from drivetrain import Drivetrain
from buttons import dualshock4, g_xbox_360
from intake import Intake

class TestRobot(wpilib.TimedRobot):
    def robotInit(self):
        self.climber = Climber()
        self.drivetrain = Drivetrain()
        self.intake = Intake()

        self.dualshock4 = wpilib.Joystick(0)
        self.xbox_360 = wpilib.Joystick(1)
        
        self.chooser = wpilib.SendableChooser()
        self.default_controller_option = "dois controles"
        self.steering_wheel_option = "volante"

    def robotPeriodic(self):
        self.drivetrain.updateEncoders()

    def autonomousInit(self):
        pass

    def autonomousPeriodic(self):
        pass

    def teleopInit(self):
        self.drivetrain.safetyMode()
        self.intake.reset_intake()
        
    def teleopPeriodic(self):
        if self.dualshock4.getRawButton(dualshock4["cross"]):
            self.drivetrain.slowdrive(
                self.dualshock4.getRawAxis(dualshock4["left-trigger-axis"]),
                self.dualshock4.getRawAxis(dualshock4["right-trigger-axis"]),
                -self.dualshock4.getRawAxis(dualshock4["left-x-axis"]) 
            )
        else:
            self.drivetrain.arcadeDrive(
                self.dualshock4.getRawAxis(dualshock4["left-trigger-axis"]),
                self.dualshock4.getRawAxis(dualshock4["right-trigger-axis"]),
                -self.dualshock4.getRawAxis(dualshock4["left-x-axis"]) 
            )
        
        self.climber.climberControl(
            self.xbox_360.getRawAxis(g_xbox_360['left-trigger-axis']),
            self.xbox_360.getRawAxis(g_xbox_360['right-trigger-axis']),
        )

        if self.xbox_360.getRawButton(g_xbox_360["x"]):
            self.intake.intake_expel()
        elif self.xbox_360.getRawButton(g_xbox_360["a"]): 
            self.intake.intake_absorb()
        else:
            self.intake.deactivate_intake()

        # Intake control position
        if self.xbox_360.getRawButtonPressed(g_xbox_360["y"]):
            self.intake.setControlVal(2)
            
        if self.xbox_360.getRawButtonPressed(g_xbox_360["b"]):
            self.intake.setControlVal(1)
            
        if self.xbox_360.getRawButtonPressed(g_xbox_360["press_left_stick"]):
            self.intake.setControlVal(0)
           
        match self.intake.getControlVal():
            case 0:
                self.intake.intake_reset_position()
            case 1:
                self.intake.intake_receiving_position()
            case 2:
                self.intake.intake_removing_position()