from vex import *

brain=Brain()

vision_20__SIG_1 = Signature(1, -6525, -6011, -6268,-5617, -5049, -5334,11, 0)
vision = Vision(Ports.PORT14, 50, vision_20__SIG_1)
controller = Controller()

left_motor_a = Motor(Ports.PORT11, GearSetting.RATIO_18_1, False)
left_motor_b = Motor(Ports.PORT12, GearSetting.RATIO_18_1, False)
left_wheels = MotorGroup(left_motor_a, left_motor_b)
right_motor_a = Motor(Ports.PORT1, GearSetting.RATIO_18_1, True)
right_motor_b = Motor(Ports.PORT2, GearSetting.RATIO_18_1, True)
right_wheels = MotorGroup(right_motor_a, right_motor_b)
roller = Motor(Ports.PORT3, GearSetting.RATIO_18_1, True)
arm_left = Motor(Ports.PORT6, GearSetting.RATIO_18_1, True)
arm_right = Motor(Ports.PORT13, GearSetting.RATIO_18_1, True)
arm = MotorGroup(arm_left, arm_right)
arm.set_max_torque(100, PERCENT)
arm.set_velocity(5, PERCENT)
arm.set_stopping(HOLD)
hammer = Motor(Ports.PORT4, GearSetting.RATIO_18_1, False)
hammer.set_max_torque(100, PERCENT)
hammer.set_velocity(30, PERCENT)
# drivetrain_gps = Gps(Ports.PORT11, 75.00, 150.00, MM, 180)
driver = DriveTrain(left_wheels, right_wheels, 319.19, 320, 40, MM, 1)
driver.set_drive_velocity(65, PERCENT)
driver.set_turn_velocity(15, PERCENT)
driver.set_stopping(COAST)
left_wing = Motor(Ports.PORT15, GearSetting.RATIO_18_1, False)
right_wing = Motor(Ports.PORT5, GearSetting.RATIO_18_1, True)
wings = MotorGroup(left_wing, right_wing)
wings.set_max_torque(100, PERCENT)
wings.set_velocity(40, PERCENT)
wings.set_timeout(1, SECONDS)
is_arrived = False 
global is_wings_open
is_wings_open = False

#1500o
while True:
    if controller.buttonUp.pressing():
        arm.spin(FORWARD)
    elif controller.buttonDown.pressing():
        arm.spin(REVERSE)
    else:
        arm.stop()

    if controller.buttonX.pressing()and not is_wings_open:
        wings.spin_for(REVERSE, 200, DEGREES)
        is_wings_open = not is_wings_open
    elif controller.buttonY.pressing() and is_wings_open:
        wings.spin_for(FORWARD, 200, DEGREES)
        is_wings_open = not is_wings_open            
    else:
        wings.stop()

    if controller.buttonA.pressing():
        hammer.spin_for(FORWARD, 1500, DEGREES)
    elif controller.buttonB.pressing():
        hammer.spin_for(FORWARD, 300, DEGREES)
    else:
        hammer.stop()

    if controller.buttonR1.pressing():
        roller.spin(FORWARD)
    elif controller.buttonR2.pressing():
        roller.spin(REVERSE)
    else:
        roller.stop()

    left_velocity = 0
    right_velocity = 0
    v = controller.axis3.position()
    h = controller.axis4.position()
    if v > 10:
        left_velocity = v
        right_velocity = v
        if h > 10:
            left_velocity += abs(h)
        elif h < -10:
            right_velocity += abs(h)
        else:
            pass
        left_wheels.set_velocity(left_velocity, RPM)
        right_wheels.set_velocity(right_velocity, RPM)
        left_wheels.spin(FORWARD)
        right_wheels.spin(FORWARD)
    elif v < -10:
        driver.drive(REVERSE, 120, RPM)
    else:
        if h > 10:
            driver.turn(RIGHT)
        elif h < -10:
            driver.turn(LEFT)
        else:
            driver.stop()
        


