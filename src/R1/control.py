#region VEXcode Generated Robot Configuration
from vex import *
import urandom

# Brain should be defined by default
brain=Brain()

# Robot configuration code
gps_20 = Gps(Ports.PORT20, 75.00, 220.00, MM, 1)


# wait for rotation sensor to fully initialize
wait(30, MSEC)


def play_vexcode_sound(sound_name):
    # Helper to make playing sounds from the V5 in VEXcode easier and
    # keeps the code cleaner by making it clear what is happening.
    print("VEXPlaySound:" + sound_name)
    wait(5, MSEC)

# add a small delay to make sure we don't print in the middle of the REPL header
wait(200, MSEC)
# clear the console to make sure we don't have the REPL in the console
print("\033[2J")

#endregion VEXcode Generated Robot Configuration
from vex import *
brain=Brain()
gps = Gps(Ports.PORT20, 75.00, 220.00, MM, 1)
vision_20__SIG_1 = Signature(1, -6525, -6011, -6268,-5617, -5049, -5334,11, 0)
vision = Vision(Ports.PORT14, 50, vision_20__SIG_1)
controller = Controller()
switch_direction = False

def init_driver(switch_direction):
    drivetrain_gps = Gps(Ports.PORT13, 0.00, -40.00, MM, 0)
    left_motor_a = Motor(Ports.PORT11, GearSetting.RATIO_18_1, switch_direction)
    left_motor_b = Motor(Ports.PORT12, GearSetting.RATIO_18_1, switch_direction)
    left_wheels = MotorGroup(left_motor_a, left_motor_b)
    right_motor_a = Motor(Ports.PORT1, GearSetting.RATIO_18_1, not switch_direction)
    right_motor_b = Motor(Ports.PORT2, GearSetting.RATIO_18_1, not switch_direction)
    right_wheels = MotorGroup(right_motor_a, right_motor_b)
    if switch_direction:
        temp = left_wheels
        left_wheels = right_wheels
        right_wheels = temp
    driver = SmartDrive(left_wheels, right_wheels, drivetrain_gps, 319.19, 320, 40, MM, 1)
    return driver, left_wheels, right_wheels

driver, left_wheels, right_wheels = init_driver(False)
roller = Motor(Ports.PORT3, GearSetting.RATIO_18_1, True)
roller.set_velocity(80,PERCENT)
right_arm = Motor(Ports.PORT6, GearSetting.RATIO_18_1, True)
left_arm = Motor(Ports.PORT13, GearSetting.RATIO_18_1, True)
arm = MotorGroup(right_arm, left_arm)
arm.set_max_torque(90,PERCENT)
hammer = Motor(Ports.PORT4, GearSetting.RATIO_18_1, False)
driver.set_drive_velocity(65, PERCENT)
driver.set_turn_velocity(15, PERCENT)
driver.set_stopping(COAST)
left_wing = Motor(Ports.PORT15, GearSetting.RATIO_18_1, False)
right_wing = Motor(Ports.PORT5, GearSetting.RATIO_18_1, True)
wings = MotorGroup(left_wing, right_wing)
wings.set_max_torque(100,PERCENT)
wings.set_velocity(40,PERCENT)
wings.set_timeout(1,SECONDS)
is_arrived = False 
global is_wings_open
is_wings_open = False

def loading():
    arm.set_velocity(30, PERCENT)
    roller.spin(FORWARD)
    arm.set_stopping(COAST)
    arm.spin_for(FORWARD, 250, DEGREES) # 180 -> 300
    arm.stop()
    wait(0.5, SECONDS)
    arm.set_stopping(HOLD)
    arm.spin_for(REVERSE, 270, DEGREES)
    arm.stop()

def open_wings():
    global is_wings_open
    if is_wings_open:
        pass
    else:
        wings.spin_for(FORWARD, 230, DEGREES)
        is_wings_open = not is_wings_open    

def close_wings():
    global is_wings_open
    if is_wings_open:
        wings.spin_for(REVERSE, 230, DEGREES)
        is_wings_open = not is_wings_open   



while True:
    if controller.buttonUp.pressing():
        arm.spin(FORWARD)
    elif controller.buttonDown.pressing():
        arm.spin(REVERSE)
    else:
        arm.stop()

    if controller.buttonX.pressing()and not is_wings_open:
        wings.spin_for(REVERSE, 230, DEGREES)
        is_wings_open = not is_wings_open
    elif controller.buttonY.pressing() and is_wings_open:
        wings.spin_for(FORWARD, 230, DEGREES)
        is_wings_open = not is_wings_open            
    else:
        wings.stop()

    if controller.buttonA.pressing():
        hammer.spin(FORWARD)
    else:
        hammer.stop()
    
    if controller.buttonB.pressing():
        switch_direction = not switch_direction
        driver, left_wheels, right_wheels = init_driver(switch_direction= switch_direction)
        wait(0.3, SECONDS)

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