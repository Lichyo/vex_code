from vex import *
# from enum import Enum, auto
brain=Brain()
controller = Controller()

# driving declaration
left_motor_a = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
left_motor_b = Motor(Ports.PORT2, GearSetting.RATIO_18_1, False)
left_wheels = MotorGroup(left_motor_a, left_motor_b)
right_motor_a = Motor(Ports.PORT3, GearSetting.RATIO_18_1, True)
right_motor_b = Motor(Ports.PORT4, GearSetting.RATIO_18_1, True)
right_wheels = MotorGroup(right_motor_a, right_motor_b)
driver = DriveTrain(left_wheels, right_wheels, 319.19, 295, 40, MM, 1)

# fixing objects devices
accepter = Motor(Ports.PORT7, GearSetting.RATIO_18_1, True)
arm = Motor(Ports.PORT8, GearSetting.RATIO_18_1, False)

wing1 = Motor(Ports.PORT13, GearSetting.RATIO_18_1, True)
wing2 = Motor(Ports.PORT14, GearSetting.RATIO_18_1, False)
wings = MotorGroup(wing1,wing2)

# setup
driver_speed_up = False
driver.set_stopping(COAST)
driver.set_drive_velocity(60, PERCENT)

is_wings_open = False
wings.set_max_torque(90, PERCENT)
wings.set_velocity(30,PERCENT)
wings.set_timeout(1,SECONDS)

accepter.set_velocity(80, PERCENT)
arm.set_stopping(HOLD)

while True:

    if controller.buttonB.pressing():
        if driver_speed_up:
            driver.set_drive_velocity(50,PERCENT)
            driver_speed_up = False
        else:
            driver.set_drive_velocity(80, PERCENT)
            driver_speed_up = True

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
        left_wheels.set_velocity(left_velocity * 1.3, RPM)
        right_wheels.set_velocity(right_velocity * 1.3, RPM)
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

    if controller.buttonA.pressing():
        if is_wings_open:
            wings.spin_for(REVERSE, 200, DEGREES)
            driver.set_turn_velocity(35, PERCENT)
        else:
            wings.spin_for(FORWARD, 200, DEGREES)
            driver.set_turn_velocity(70, PERCENT)
        is_wings_open = not is_wings_open            
    else:
        wings.stop()
    
    if controller.buttonR1.pressing():
        accepter.spin(FORWARD)
    elif controller.buttonR2.pressing():
        accepter.spin(REVERSE)
    else:
        accepter.stop()
        
    if controller.buttonL1.pressing():
        arm.spin(FORWARD)
    elif controller.buttonL2.pressing():
        arm.spin(REVERSE)
    else:
        arm.stop()

    
    
        
