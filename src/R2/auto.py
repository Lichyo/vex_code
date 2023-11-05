from vex import *

left_motor_a = Motor(Ports.PORT5, GearSetting.RATIO_18_1, False)
left_motor_b = Motor(Ports.PORT6, GearSetting.RATIO_18_1, False)
left_wheels = MotorGroup(left_motor_a, left_motor_b)
right_motor_a = Motor(Ports.PORT7, GearSetting.RATIO_18_1, True)
right_motor_b = Motor(Ports.PORT8, GearSetting.RATIO_18_1, True)
right_wheels = MotorGroup(right_motor_a, right_motor_b)
drivetrain_gps = Gps(Ports.PORT9, 160.00, 20.00, MM, 180)
driver = SmartDrive(left_wheels, right_wheels, drivetrain_gps, 319.19, 320, 40, MM, 1)
brain = Brain()
controller = Controller()
driver.set_drive_velocity(10, PERCENT)

vision_1__SIG_1 = Signature(1, -4789, -4193, -4492,-5041, -4557, -4800,3.9, 0)
vision = Vision(Ports.PORT1, 50, vision_1__SIG_1)
stretch = Motor(Ports.PORT2, GearSetting.RATIO_18_1, False)
throw_1 = Motor(Ports.PORT4, GearSetting.RATIO_36_1, False)
throw_2 = Motor(Ports.PORT3, GearSetting.RATIO_36_1, True)
throw= MotorGroup(throw_1, throw_2)
throw.set_stopping(HOLD)
throw.set_velocity(35, PERCENT)
throw.set_max_torque(100, PERCENT)
stretch.set_velocity(90, PERCENT)
stretch.set_stopping(COAST)
stretch.set_timeout(1, SECONDS)
throw.set_timeout(1, SECONDS)


class Accepter:
    def __init__(self):
        self.prepared = False
        self.is_stretching = False
    
    def throw_prepare(self):
        throw.spin_for(FORWARD, 165, DEGREES)

    def stretch_prepare(self):
        if self.is_stretching:
            pass
        else:
            self.is_stretching = True
            stretch.spin_for(FORWARD, 900, DEGREES)
    
    def prepare(self):
        if self.is_stretching:
           self.set_stop()
        else:
            Thread(lambda: driver.drive_for(REVERSE, 30, MM))
            Thread(self.throw_prepare)
            self.stretch_prepare()
            self.prepared = True
        

    def set_stop(self):
        throw.stop()
        stretch.stop()

    def shoot(self):
        if self.prepared:
            stretch.spin_for(REVERSE, 900, DEGREES)
            throw.spin_for(FORWARD, 195, DEGREES)
            self.prepared = False
            self.is_stretching = False
        else:
            self.set_stop()
            
accepter = Accepter()
while True:
    if not accepter.prepared:
        accepter.prepare()
    else:
        objects = vision.take_snapshot(vision_1__SIG_1)
        if objects == None:
            pass
        else:
            objects = vision.largest_object()
            if objects.height > 30 and objects.width > 50:
                accepter.shoot()