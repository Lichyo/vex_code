from vex import *
# from enum import Enum, auto
brain=Brain()
controller = Controller()

# driving declaration
left_motor_a = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
left_motor_b = Motor(Ports.PORT2, GearSetting.RATIO_18_1, False)
left_drive_smart = MotorGroup(left_motor_a, left_motor_b)
right_motor_a = Motor(Ports.PORT3, GearSetting.RATIO_18_1, True)
right_motor_b = Motor(Ports.PORT4, GearSetting.RATIO_18_1, True)
right_drive_smart = MotorGroup(right_motor_a, right_motor_b)
driver = DriveTrain(left_drive_smart, right_drive_smart, 319.19, 295, 40, MM, 1)

# fixing objects devices
accepter = Motor(Ports.PORT7, GearSetting.RATIO_18_1, True)
arm = Motor(Ports.PORT8, GearSetting.RATIO_18_1, False)

wing1 = Motor(Ports.PORT13, GearSetting.RATIO_18_1, True)
wing2 = Motor(Ports.PORT14, GearSetting.RATIO_18_1, False)
wings = MotorGroup(wing1,wing2)

# setup
driver_mode = False
driver.set_stopping(COAST)
driver.set_drive_velocity(60, PERCENT)
is_wings_open = False
wings.set_max_torque(90, PERCENT)
wings.set_velocity(30,PERCENT)
wings.set_timeout(1,SECONDS)
accepter.set_velocity(80, PERCENT)
arm.set_stopping(HOLD)

while True:

    # if controller.buttonA.pressing():
    #     if drive_mode != driving_mode.normal:
    #         drive_mode = driving_mode.normal
    #         driver.set_drive_velocity(50,PERCENT)
    #     elif drive_mode != driving_mode.speed_up:
    #         drive_mode = driving_mode.speed_up
    #         driver.set_drive_velocity(50,PERCENT)
    
    axis_horizontal = controller.axis4.position()
    axis_vertical = controller.axis3.position()

    brain.screen.clear_screen()
    brain.screen.set_cursor(1,1)
    brain.screen.print('axis_horizontal: ',axis_horizontal)
    brain.screen.next_row()
    brain.screen.print('axis_vertical: ',axis_vertical)
    brain.screen.next_row()
    # wait(0.5, SECONDS)
    if axis_horizontal > 10:
        driver.turn(RIGHT)
    elif axis_horizontal < -10:
        driver.turn(LEFT)
    elif axis_vertical > 15:
        driver.drive(FORWARD)
    elif axis_vertical < -15:
        driver.drive(REVERSE)
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

    
    
        
