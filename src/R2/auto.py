from vex import *

left_motor_a = Motor(Ports.PORT5, GearSetting.RATIO_18_1, False)
left_motor_b = Motor(Ports.PORT6, GearSetting.RATIO_18_1, False)
left_drive_smart = MotorGroup(left_motor_a, left_motor_b)
right_motor_a = Motor(Ports.PORT7, GearSetting.RATIO_18_1, True)
right_motor_b = Motor(Ports.PORT8, GearSetting.RATIO_18_1, True)
right_drive_smart = MotorGroup(right_motor_a, right_motor_b)
drivetrain_gps = Gps(Ports.PORT9, 160.00, 20.00, MM, 180)
drivetrain = SmartDrive(left_drive_smart, right_drive_smart, drivetrain_gps, 319.19, 320, 40, MM, 1)
brain = Brain()
controller = Controller()

vision_1__SIG_1 = Signature(1, -4789, -4193, -4492,-5041, -4557, -4800,3.9, 0)
vision = Vision(Ports.PORT1, 50, vision_1__SIG_1)
stretch = Motor(Ports.PORT2, GearSetting.RATIO_18_1, False)
throw_1 = Motor(Ports.PORT4, GearSetting.RATIO_36_1, False)
throw_2 = Motor(Ports.PORT3, GearSetting.RATIO_36_1, True)
throw= MotorGroup(throw_1, throw_2)
throw.set_stopping(HOLD)
throw.set_velocity(25, PERCENT)
throw.set_max_torque(100, PERCENT)
stretch.set_velocity(90, PERCENT)
stretch.set_stopping(COAST)
global is_stretching
global prepared

prepared = False
is_stretching = False

def throw_prepare():
    throw.spin_for(FORWARD, 220, DEGREES)

def stretch_prepare():
    stretch.spin_for(FORWARD, 900, DEGREES)
 
def prepare():
    global prepared
    Thread(throw_prepare)
    Thread(stretch_prepare)
    prepared = True

def set_stop():
    throw.stop()
    stretch.stop()

def shoot():
    global prepared
    stretch.spin_for(REVERSE, 900, DEGREES)
    throw.spin_for(FORWARD, 140, DEGREES)
    prepared = False

while True:
    if not prepared:
        prepare()
    else:
        objects = vision.take_snapshot(vision_1__SIG_1)
        if objects == None:
            pass
        else:
            objects = vision.largest_object()
            if objects.height > 30 and objects.width > 50:
                shoot()