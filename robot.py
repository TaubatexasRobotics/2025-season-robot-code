import wpilib
import wpilib.drive
import constants

from climber import Climber
from drivetrain import Drivetrain
from buttons import dualshock4_map, g_xbox_360_map
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
        self.drivetrain.update_data()

    def autonomousInit(self):
        self.drivetrain.safety_mode()
        self.drivetrain.reset()

    def autonomousPeriodic(self):
        self.drivetrain.aim_drive(3)

    def teleopInit(self):
        self.drivetrain.safety_mode()
        self.drivetrain.reset()
        self.algae_intake.reset_intake()
        
    def teleopPeriodic(self):
        if self.dualshock4.getRawButton(dualshock4_map["cross"]):
            self.drivetrain.slow_drive(
                self.dualshock4.getRawAxis(dualshock4_map["right-trigger-axis"]),
                self.dualshock4.getRawAxis(dualshock4_map["left-trigger-axis"]),
                -self.dualshock4.getRawAxis(dualshock4_map["left-x-axis"]) 
            )
        elif self.dualshock4.getRawButton(dualshock4_map["square"]):
            self.drivetrain.turn_to_degrees()
        else:
            self.drivetrain.arcade_drive(
                self.dualshock4.getRawAxis(dualshock4_map["right-trigger-axis"]),
                self.dualshock4.getRawAxis(dualshock4_map["left-trigger-axis"]),
                -self.dualshock4.getRawAxis(dualshock4_map["left-x-axis"]) 
            )

        
        if self.dualshock4_2.getPOV() == 0:
            self.climber.climbUp()
        elif self.dualshock4_2.getPOV() == 180:
            self.climber.climbDown()
        else:
            self.climber.idle()
            
        if self.dualshock4_2.getRawAxis(g_xbox_360_map["left-trigger-axis"]) > 0:
            self.algae_intake.intake_expel()
        elif self.dualshock4_2.getRawAxis(g_xbox_360_map["right-trigger-axis"]) > 0: 
            self.algae_intake.intake_absorb()
        else:
            self.algae_intake.deactivate_intake()
        
        if self.dualshock4_2.getRawButton(g_xbox_360_map["lb"]):
            self.coral_intake.enable()
        elif self.dualshock4_2.getRawButton(g_xbox_360_map["rb"]):
            self.coral_intake.invert()
        else:
            self.coral_intake.disable()

        #self.algae_intake.move_arm_by_joystick(self.dualshock4_2.getRawAxis(g_xbox_360_map["right-y-stick"]))

        # Intake control position
        if self.dualshock4_2.getRawButtonPressed(g_xbox_360_map["y"]):
            self.algae_intake.setControlVal(2)
            
        if self.dualshock4_2.getRawButtonPressed(g_xbox_360_map["b"]):
            self.algae_intake.setControlVal(1)
            
        if self.dualshock4_2.getRawButtonPressed(g_xbox_360_map["a"]):
            self.algae_intake.setControlVal(0)
           
        match self.algae_intake.get_control_val():
            case 0:
                self.algae_intake.intake_reset_position()
            case 1:
                self.algae_intake.intake_receiving_position()
            case 2:
                self.algae_intake.intake_removing_position()
