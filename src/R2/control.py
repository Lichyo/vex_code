from vex import *
arm = Motor(Ports.PORT15, GearSetting.RATIO_18_1, False)
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

prepared = False
stretch_is_out = False
is_Auto = True

class Accepter:
    def __init__(self):
        self.prepared = False
        self.is_stretching = False
    
    def throw_prepare(self):
        throw.spin_for(FORWARD, 160, DEGREES)

    def stretch_prepare(self):
        if self.is_stretching:
            pass
        else:
            self.is_stretching = True
            stretch.spin_for(FORWARD, 800, DEGREES)
    
    def prepare(self):
        if self.is_stretching:
           self.set_stop()
        else:
            Thread(lambda: driver.drive_for(REVERSE, 10, MM))
            Thread(self.throw_prepare)
            self.stretch_prepare()
            self.prepared = True
        

    def set_stop(self):
        throw.stop()
        stretch.stop()

    def shoot(self):
        if self.prepared:
            stretch.spin_for(REVERSE, 800, DEGREES)
            throw.spin_for(FORWARD, 200, DEGREES)
            throw.stop()
            self.prepared = False
            self.is_stretching = False
        else:
            self.set_stop()
            
    def execute_preload(self): 
        Thread(lambda: arm.spin_for(FORWARD,180,DEGREES) )
        self.throw_prepare()
        stretch.spin_for(FORWARD, 730, DEGREES)
        arm.spin_for(REVERSE,180,DEGREES)
        self.prepared = True
        self.is_stretching = True
        self.shoot()
            
accepter = Accepter()

def auto():
    if not accepter.prepared:
        accepter.prepare()
    else:
        objects = vision.take_snapshot(vision_1__SIG_1)
        if objects == None:
            pass
        else:
            objects = vision.largest_object()
            if objects.height > 10 and objects.width > 20:
                accepter.shoot()

while True:
    if is_Auto:
        auto()
    elif controller.buttonX.pressing():
        is_Auto = not is_Auto
            
    else:       
        
        if controller.buttonUp.pressing():
            stretch.spin_for(FORWARD, 800, DEGREES)
        elif controller.buttonDown.pressing():
            stretch.spin_for(REVERSE, 800, DEGREES)
                
        if controller.buttonA.pressing():
            throw.spin_for(FORWARD, 200, DEGREES)
        elif controller.buttonB.pressing():
            throw.spin_for(FORWARD, 160, DEGREES)
        else:
            pass
    
        left_velocity = 0
        right_velocity = 0
        v = controller.axis3.position()
        h = controller.axis4.position()
        if v > 0:
            left_velocity = v
            right_velocity = v
            if h > 0:
                left_velocity += abs(h)
            else:
                right_velocity += abs(h)
            left_wheels.set_velocity(left_velocity, RPM)
            right_wheels.set_velocity(right_velocity, RPM)
            left_wheels.spin(FORWARD)
            right_wheels.spin(FORWARD)
        else:
            driver.stop()