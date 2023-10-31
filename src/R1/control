from vex import *

left_motor_a = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
left_motor_b = Motor(Ports.PORT2, GearSetting.RATIO_18_1, False)
left_drive_smart = MotorGroup(left_motor_a, left_motor_b)
right_motor_a = Motor(Ports.PORT3, GearSetting.RATIO_18_1, True)
right_motor_b = Motor(Ports.PORT4, GearSetting.RATIO_18_1, True)
right_drive_smart = MotorGroup(right_motor_a, right_motor_b)
drivetrain = DriveTrain(left_drive_smart, right_drive_smart, 319.19, 295, 40, MM, 1)

brain=Brain()

left_motor_a = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
left_motor_b = Motor(Ports.PORT2, GearSetting.RATIO_18_1, False)
left_drive_smart = MotorGroup(left_motor_a, left_motor_b)
right_motor_a = Motor(Ports.PORT3, GearSetting.RATIO_18_1, True)
right_motor_b = Motor(Ports.PORT4, GearSetting.RATIO_18_1, True)
right_drive_smart = MotorGroup(right_motor_a, right_motor_b)
driver = DriveTrain(left_drive_smart, right_drive_smart, 319.19, 295, 40, MM, 1)



accepter = Motor(Ports.PORT7, GearSetting.RATIO_18_1, False)
arm = Motor(Ports.PORT8, GearSetting.RATIO_18_1, False)
driver_mode = False

# wing1 = Motor(Ports.PORT3, GearSetting.RATIO_18_1, True)
# wing2 = Motor(Ports.PORT4, GearSetting.RATIO_18_1, False)
# wings = MotorGroup(wing1,wing2)
driver_mode = False
controller = Controller()
driver.set_stopping(COAST)
is_wing_open = False
# wings.set_max_torque(80, PERCENT)
# wings.set_velocity(50,PERCENT)
# wings.set_max_torque(80,PERCENT)
# wings.set_timeout(3,SECONDS)


left_drive_smart.spin_for(REVERSE, 1000, DEGREES)
right_drive_smart.spin_for(REVERSE, 1000, DEGREES)
# right_motor_a.spin_for(REVERSE, 1000, DEGREES)
# right_motor_b.spin_for(REVERSE, 1000, DEGREES)
# while True:

#     # if controller.buttonA.pressing():
#     #     driver_mode = not driver_mode
#     #     driver.set_drive_velocity(100, PERCENT)
#     # else:
#     #     driver.set_drive_velocity(60, PERCENT)
    
    
#     axis_horizontal = controller.axis4.position()
#     axis_vertical = controller.axis3.position()

#     brain.screen.clear_screen()
#     brain.screen.set_cursor(1,1)
#     brain.screen.print('axis_horizontal: ',axis_horizontal)
#     brain.screen.next_row()
#     brain.screen.print('axis_vertical: ',axis_vertical)
#     brain.screen.next_row()
#     # wait(0.5, SECONDS)
#     if axis_horizontal > 10:
#         driver.turn(RIGHT)
#     elif axis_horizontal < -10:
#         driver.turn(LEFT)
#     elif axis_vertical > 15:
#         driver.drive(FORWARD)
#     elif axis_vertical < -15:
#         driver.drive(REVERSE)
#     else:
#         driver.stop()

#     # if controller.buttonL1.pressing() and not is_wing_open:
#     #     wings.spin_for(FORWARD,200,DEGREES)
#     #     is_wing_open = True
#     # elif controller.buttonL2.pressing() and is_wing_open:
#     #     wings.spin_for(REVERSE,200,DEGREES)
#     #     is_wing_open = False
#     # else:
#     #     wings.stop()