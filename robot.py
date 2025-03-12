import wpilib
import wpilib.drive
import constants

from climber import Climber
from drivetrain import Drivetrain
from buttons import dualshock4_map
from algae_intake import AlgaeIntake
from coral_intake import CoralIntake
from typing import Literal

class TestRobot(wpilib.TimedRobot):
    def robotInit(self):
        self.climber = Climber()
        self.drivetrain = Drivetrain()
        self.algae_intake = AlgaeIntake()
        self.coral_intake = CoralIntake()
        self.mechanisms = [self.climber, self.drivetrain, self.algae_intake, self.coral_intake]

        self.dashboard = wpilib.SmartDashboard

        self.dualshock4 = wpilib.Joystick(constants.DUALSHOCK4_ID)
        self.dualshock4_2 = wpilib.Joystick(constants.DUALSHOCK4_2_ID)
        
        self.chooser = wpilib.SendableChooser()
        self.default_controller_option = constants.SENDABLE_CHOOSER_TWO_JOYSTICKS_OPTION
        self.steering_wheel_option = constants.SENDABLE_CHOOSER_STEERING_WHEEL_OPTION

    def updateControlType(self) -> Literal["position", "duty_cycle"]:
        position_control_buttons = ["triangle", "circle", "cross"]
        check_is_pressed = self.dualshock4_2.getRawButton

        is_any_control_button_pressed = any(
            check_is_pressed(dualshock4_map[button])
            for button
            in position_control_buttons
        )

        y_axis_value = self.dualshock4_2.getRawAxis(dualshock4_map["right-y-axis"])

        if is_any_control_button_pressed:
            self.algae_intake.arm_control_type = "position"
        elif abs( y_axis_value ) > 0.15:
            self.algae_intake.arm_control_type = "duty_cycle"
        
        return self.algae_intake.arm_control_type
    
    def run_mechanisms_method(self, mechanisms: list, method_name: str, *args, **kwargs) -> None:
        for mechanism in mechanisms:
            if hasattr(mechanism, method_name):
                getattr(mechanism, method_name)(*args, **kwargs)

    def testDashboardResponsiveness(self):
        '''Tests responsiveness of the dashboard with an evergrowing number'''
        if not hasattr(self, "responsiveness_test"):
            self.responsiveness_test = 0
        self.responsiveness_test += 1
        self.dashboard.putNumber("Responsiveness Test", self.responsiveness_test)
    
    def updateDashboard(self):
        # test responsiveness
        self.testDashboardResponsiveness()
        self.run_mechanisms_method(self.mechanisms, "updateDashboard", self.dashboard)

    def robotPeriodic(self):
        self.updateDashboard()
        self.drivetrain.updateData()
        self.run_mechanisms_method(self.mechanisms, "robotPeriodic")

    def autonomousInit(self):
        self.run_mechanisms_method(self.mechanisms, "dashboardInit", self.dashboard)
        self.run_mechanisms_method(self.mechanisms, "autonomousInit")

    def autonomousPeriodic(self):
        self.drivetrain.arcadeDriveAlign(3)

    def teleopInit(self):
        self.run_mechanisms_method(self.mechanisms, "dashboardInit", self.dashboard)
        self.drivetrain.safetyMode()
        self.algae_intake.reset_intake()
        
    def teleopPeriodic(self):
        try:
            if self.dualshock4.getRawButton(dualshock4_map["cross"]):
                self.drivetrain.slowdrive(
                    self.dualshock4.getRawAxis(dualshock4_map["left-trigger-axis"]),
                    self.dualshock4.getRawAxis(dualshock4_map["right-trigger-axis"]),
                    -self.dualshock4.getRawAxis(dualshock4_map["left-x-axis"]) 
                )
            elif self.dualshock4.getRawButton(dualshock4_map["square"]):
                self.drivetrain.turnToDegrees()
            else:
                self.drivetrain.arcadeDrive(
                    self.dualshock4.getRawAxis(dualshock4_map["left-trigger-axis"]),
                    self.dualshock4.getRawAxis(dualshock4_map["right-trigger-axis"]),
                    -self.dualshock4.getRawAxis(dualshock4_map["left-x-axis"]) 
                )
        except Exception as e:
            print(e)

        try:
            self.updateControlType()
            self.algae_intake.teleopPeriodic()

            if self.dualshock4_2.getPOV() == 0:
                self.climber.climbUp()
            elif self.dualshock4_2.getPOV() == 180:
                self.climber.climbDown()
            else:
                self.climber.idle()
            
            if self.dualshock4_2.getRawButton(dualshock4_map["l2"]):
                self.algae_intake.intake_expel()
            elif self.dualshock4_2.getRawButton(dualshock4_map["r2"]): 
                self.algae_intake.intake_absorb()
            else:
                self.algae_intake.deactivate_intake()
            
            if self.dualshock4_2.getRawButton(dualshock4_map["l1"]):
                self.coral_intake.enable()
            elif self.dualshock4_2.getRawButton(dualshock4_map["r1"]):
                self.coral_intake.invert()
            else:
                self.coral_intake.disable()

            if(self.algae_intake.arm_control_type == "position"):
                if self.dualshock4_2.getRawButton(dualshock4_map["triangle"]):
                    self.algae_intake.target_position = "REMOVING"
                if self.dualshock4_2.getRawButton(dualshock4_map["circle"]):
                    self.algae_intake.target_position = "RECEIVING"
                if self.dualshock4_2.getRawButton(dualshock4_map["cross"]):
                    self.algae_intake.target_position = "HOMING"
                self.algae_intake.go_to_position(self.algae_intake.arm_positions[self.algae_intake.target_position])
            else:
                self.algae_intake.move_arm_by_duty_cycle(
                    self.dualshock4_2.getRawAxis(dualshock4_map["right-y-axis"])
                )
        except Exception as e:
            print(e)

