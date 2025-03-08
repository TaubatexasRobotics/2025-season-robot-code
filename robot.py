import wpilib
import wpilib.drive
import constants

from climber import Climber
from drivetrain import Drivetrain
from buttons import dualshock4_map
from algae_intake import AlgaeIntake
from coral_intake import CoralIntake

class TestRobot(wpilib.TimedRobot):
    def robotInit(self):
        self.climber = Climber()
        self.drivetrain = Drivetrain()
        self.algae_intake = AlgaeIntake()
        self.coral_intake = CoralIntake()

        self.dualshock4 = wpilib.Joystick(constants.DUALSHOCK4_ID)
        self.dualshock4_2 = wpilib.Joystick(constants.DUALSHOCK4_2_ID)
        
        self.chooser = wpilib.SendableChooser()
        self.default_controller_option = constants.SENDABLE_CHOOSER_TWO_JOYSTICKS_OPTION
        self.steering_wheel_option = constants.SENDABLE_CHOOSER_STEERING_WHEEL_OPTION

    def robotPeriodic(self):
        self.drivetrain.updateEncoders()

    def autonomousInit(self):
        pass

    def autonomousPeriodic(self):
        self.drivetrain.arcadeDriveAlign(3)

    def teleopInit(self):
        self.drivetrain.safetyMode()
        self.algae_intake.reset_intake()
        
    def teleopPeriodic(self):
        if self.dualshock4.getRawButton(dualshock4_map["cross"]):
            self.drivetrain.slowdrive(
                self.dualshock4.getRawAxis(dualshock4_map["left-trigger-axis"]),
                self.dualshock4.getRawAxis(dualshock4_map["right-trigger-axis"]),
                -self.dualshock4.getRawAxis(dualshock4_map["left-x-axis"]) 
            )
        else:
            self.drivetrain.arcadeDrive(
                self.dualshock4.getRawAxis(dualshock4_map["left-trigger-axis"]),
                self.dualshock4.getRawAxis(dualshock4_map["right-trigger-axis"]),
                -self.dualshock4.getRawAxis(dualshock4_map["left-x-axis"]) 
            )

        
        if self.dualshock4_2.getPOV() == 0:
            self.climber.climbUp()
        elif self.dualshock4_2.getPOV() == 180:
            self.climber.climbDown()
        else:
            self.climber.idle()
            
            
        if self.dualshock4_2.getRawButton(dualshock4_map["r2"]):
            self.algae_intake.intake_expel()
        elif self.dualshock4_2.getRawButton(dualshock4_map["l2"]): 
            self.algae_intake.intake_absorb()
        else:
            self.algae_intake.deactivate_intake()
        
        if self.dualshock4_2.getRawButton(dualshock4_map["l1"]):
            self.coral_intake.enable()
        elif self.dualshock4_2.getRawButton(dualshock4_map["r1"]):
            self.coral_intake.invert()
        else:
            self.coral_intake.disable()

        #self.intake.readjust_encoder()
        wpilib.SmartDashboard.putBoolean("Limit Switch", self.algae_intake.limit_switch.get())

        # Intake control position
        if self.dualshock4_2.getRawButtonPressed(dualshock4_map["triangle"]):
            self.algae_intake.setControlVal(2)
            
        if self.dualshock4_2.getRawButtonPressed(dualshock4_map["circle"]):
            self.algae_intake.setControlVal(1)
            
        if self.dualshock4_2.getRawButtonPressed(dualshock4_map["cross"]):
            self.algae_intake.setControlVal(0)
           
        match self.algae_intake.getControlVal():
            case 0:
                self.algae_intake.intake_reset_position()
            case 1:
                self.algae_intake.intake_receiving_position()
            case 2:
                self.algae_intake.intake_removing_position()
