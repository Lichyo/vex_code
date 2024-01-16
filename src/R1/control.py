from vex import *
brain=Brain()
gps = Gps(Ports.PORT20, 75.00, 220.00, MM, 1)
vision_20__SIG_1 = Signature(1, -6525, -6011, -6268,-5617, -5049, -5334,11, 0)
vision = Vision(Ports.PORT14, 50, vision_20__SIG_1)
controller = Controller()
switch_direction = False

class ButtonControl:
    def __init__(self):
        self.L1 = 'free'
        self.L2 = 'free'
        self.R1 = 'free' 
        self.R2 = 'free'
        self.x = 'free'
        self.y = 'free'
        self.a = 'free'
        self.b = 'free'

    def pressing(self, button, function):
        if button == 'free':
            button = 'pressing'
            function()
            button = 'free'
        else:
            return


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
arm.set_max_torque(100,PERCENT)
arm.set_stopping(HOLD)
hammer = Motor(Ports.PORT4, GearSetting.RATIO_18_1, False)
driver.set_drive_velocity(65, PERCENT)
driver.set_turn_velocity(15, PERCENT)
driver.set_stopping(COAST)
left_wing = Motor(Ports.PORT15, GearSetting.RATIO_18_1, True)
right_wing = Motor(Ports.PORT5, GearSetting.RATIO_18_1, False)
wings = MotorGroup(left_wing, right_wing)
wings.set_max_torque(100,PERCENT)
wings.set_velocity(40,PERCENT)
wings.set_timeout(1,SECONDS)
is_arrived = False 
global is_wings_open
is_wings_open = False
is_wings_spin = 0
control = ButtonControl()

def empty_function():
    pass

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
    wings.spin_for(FORWARD, 230, DEGREES)
    return

def close_wings():
    wings.spin_for(REVERSE, 230, DEGREES)
    return

def right_wing_open():
    brain.screen.print('right_wing_open()')
    brain.screen.next_row()
    right_wing.spin_for(FORWARD, 230, DEGREES)
    return

def left_wing_open():
    brain.screen.print('left_wing_open()')
    brain.screen.next_row()
    left_wing.spin_for(FORWARD, 230, DEGREES)
    return

def right_wing_close():
    brain.screen.print('right_wing_close()')
    brain.screen.next_row()
    right_wing.spin_for(REVERSE, 230, DEGREES)
    return

def left_wing_close():
    brain.screen.print('left_wing_close()')
    brain.screen.next_row()
    left_wing.spin_for(REVERSE, 230, DEGREES)
    return

thread = Thread(empty_function)
while True:
    if controller.buttonL1.pressing():
        arm.spin(FORWARD)
    elif controller.buttonL2.pressing():
        arm.spin(REVERSE)
    else:
        arm.stop()

    if controller.buttonR1.pressing():
        roller.spin(FORWARD)
    elif controller.buttonR2.pressing():
        roller.spin(REVERSE)
    else:
        roller.stop()

    if controller.buttonDown.pressing():
        driver, left_wheels, right_wheels = init_driver(False)
        
    if controller.buttonUp.pressing():
        driver, left_wheels, right_wheels = init_driver(True)
        
    if controller.buttonX.pressing():
        thread.stop()
        thread = Thread(lambda: control.pressing(control.b, left_wing_open))
    else:
        pass

    if controller.buttonY.pressing():
        thread.stop()
        thread = Thread(lambda: control.pressing(control.y, left_wing_close))
    else:
        pass

    if controller.buttonA.pressing():
        thread.stop()
        thread = Thread(lambda: control.pressing(control.a, right_wing_open))
    else:
        pass

    if controller.buttonB.pressing():
        thread.stop()
        thread = Thread(lambda: control.pressing(control.x, right_wing_close))
    else:
        pass


    left_velocity = 0
    right_velocity = 0
    v = controller.axis3.position()*1.25 
    h = controller.axis1.position()*0.75
    left_velocity = v + h 
    right_velocity = v - h
    left_wheels.set_velocity(left_velocity, RPM) 
    right_wheels.set_velocity(right_velocity, RPM) 
    left_wheels.spin(FORWARD) 
    right_wheels.spin(FORWARD)