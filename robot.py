import wpilib
import wpilib.drive
import constants

from climber import Climber
from drivetrain import Drivetrain
from buttons import dualshock4_map, g_xbox_360_map
from algae_intake import AlgaeIntake
from coral_intake import CoralIntake
from wpilib.cameraserver import CameraServer

class TestRobot(wpilib.TimedRobot):
    def robotInit(self):
        self.climber = Climber()
        self.drivetrain = Drivetrain()
        self.algae_intake = AlgaeIntake()
        self.coral_intake = CoralIntake()

        self.dualshock4 = wpilib.Joystick(constants.DUALSHOCK4_ID)
        self.dualshock4_2 = wpilib.Joystick(constants.DUALSHOCK4_2_ID)
        
        self.chooser = wpilib.SendableChooser()

        self.match_mode = False
        self.whichAutonomous = 0

        self.chooser.addOption("Quadra", True)
        self.chooser.setDefaultOption("Pit", False)

        #wpilib.SmartDashboard.putData(self.chooser)

        self.autochooser = wpilib.SendableChooser()
        self.autochooser.setDefaultOption("Apenas Frente", 0)
        self.autochooser.addOption("L1 Meio", 1)
        #self.autochooser.addOption("L1 Dir", 2)
        #self.autochooser.addOption("L1 Esq", 3)

        wpilib.SmartDashboard.putData(self.autochooser)

        self.timer = wpilib.Timer()
        CameraServer().launch()

    def robotPeriodic(self):
        self.drivetrain.updateData()

    def disabledInit(self):
        self.climber.finishMotor()

    def autonomousInit(self):
        self.drivetrain.safetyMode()
        self.drivetrain.reset()
        self.climber.startMotor()
        self.timer.reset()
        self.timer.start()

        self.match_mode = self.chooser.getSelected()
        self.whichAutonomous = self.autochooser.getSelected()

    def autonomousPeriodic(self):
        self.algae_intake.intake_reset_position()
        match self.whichAutonomous:
            case 0:
                if self.timer.get() < 5:
                    self.drivetrain.drivetrain.arcadeDrive(-0.5, 0)
            case 1:
                self.drivetrain.drivetrain.arcadeDrive(-0.5, 0)
                if self.timer.get() >= 8 and self.timer.get() < 10:
                    self.coral_intake.invert()
                else:
                    self.coral_intake.disable()

    def autonomousExit(self):
        self.timer.reset()

    def teleopInit(self):
        self.drivetrain.safetyMode()
        self.algae_intake.reset_intake()

    def teleopExit(self):
        if self.match_mode:
            self.timer.reset()
            self.timer.start()

    def disabledPeriodic(self):
        if self.match_mode and self.timer.get() < 7:
            self.climber.climber.set(-0.5)
        
    def teleopPeriodic(self):
        self.climber.isFinished()

        if self.dualshock4.getRawButton(g_xbox_360_map["a"]):
            self.drivetrain.slowdrive(
                self.dualshock4.getRawAxis(g_xbox_360_map["right-trigger-axis"]),
                self.dualshock4.getRawAxis(g_xbox_360_map["left-trigger-axis"]),
                -self.dualshock4.getRawAxis(g_xbox_360_map["left-x-axis"]) 
            )
        elif self.dualshock4.getRawButton(g_xbox_360_map["b"]):
            self.drivetrain.turnToDegrees()
        else:
            self.drivetrain.arcadeDrive(
                self.dualshock4.getRawAxis(g_xbox_360_map["right-trigger-axis"]),
                self.dualshock4.getRawAxis(g_xbox_360_map["left-trigger-axis"]),
                -self.dualshock4.getRawAxis(g_xbox_360_map["left-x-axis"]) 
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

        #self.intake.readjust_encoder()
        #wpilib.SmartDashboard.putBoolean("Limit Switch", self.algae_intake.limit_switch.get())

        # Intake control position
        if self.dualshock4_2.getRawButtonPressed(g_xbox_360_map["y"]):
            self.algae_intake.setControlVal(2)
           
        if self.dualshock4_2.getRawButtonPressed(g_xbox_360_map["b"]):
            self.algae_intake.setControlVal(1)
            
        if self.dualshock4_2.getRawButtonPressed(g_xbox_360_map["a"]):
            self.algae_intake.setControlVal(0)

        if self.dualshock4_2.getRawButton(g_xbox_360_map["press-left-stick"]):
            self.algae_intake.full_min_intake()

        if self.dualshock4_2.getRawButton(g_xbox_360_map["press-right-stick"]):
            self.algae_intake.full_max_intake()
           
        match self.algae_intake.getControlVal():
            case 0:
                self.algae_intake.intake_reset_position()
            case 1:
                self.algae_intake.intake_receiving_position()
            case 2:
                self.algae_intake.intake_removing_position()
