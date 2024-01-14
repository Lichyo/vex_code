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
limit = DigitalIn(brain.three_wire_port.d)
ir = DigitalIn(brain.three_wire_port.a)

controller = Controller()
driver.set_drive_velocity(70, PERCENT)
roller = Motor(Ports.PORT10, GearSetting.RATIO_18_1, False)
vision_1__SIG_1 = Signature(1, -4789, -4193, -4492,-5041, -4557, -4800,3.9, 0)
vision = Vision(Ports.PORT1, 50, vision_1__SIG_1)
stretch = Motor(Ports.PORT2, GearSetting.RATIO_18_1, False)
throw_1 = Motor(Ports.PORT4, GearSetting.RATIO_36_1, False)
throw_2 = Motor(Ports.PORT3, GearSetting.RATIO_36_1, True)
throw= MotorGroup(throw_1, throw_2)
arm = Motor(Ports.PORT15, GearSetting.RATIO_36_1, False)
arm.set_timeout(1,SECONDS)
throw.set_stopping(HOLD)
throw.set_velocity(40, PERCENT)
throw.set_max_torque(100, PERCENT)
stretch.set_velocity(80, PERCENT)
stretch.set_stopping(COAST)
stretch.set_timeout(1, SECONDS)
throw.set_timeout(1, SECONDS)
roller.set_velocity(80, PERCENT)
is_strethced = False
auto = True


class Accepter:
    def __init__(self):
        self.prepared = False
        self.is_stretching = False
    
    def throw_prepare(self,ir):
        while ir.value() == 1: 
            throw.spin(FORWARD)
        throw.stop()
    def stretch_prepare(self):
        if self.is_stretching:
            pass
        else:
            self.is_stretching = True
            stretch.spin_for(FORWARD, 540, DEGREES)
    
    def prepare(self,ir):
        if self.is_stretching:
           self.set_stop()
        else:
            Thread(lambda: driver.drive_for(REVERSE, 10, MM))
            Thread(self.stretch_prepare)
            self.throw_prepare(ir)
            self.prepared = True


        
            
    def execute_preload(self):
        Thread(lambda: arm.spin_for(FORWARD,180,DEGREES))
        self.prepare(ir)
        arm.spin_for(REVERSE,180,DEGREES)
        

    def set_stop(self):
        throw.stop()
        stretch.stop()

    def shoot(self, limit):
        
        if self.prepared:
            while limit.value() == 1:
                stretch.spin(REVERSE)
            throw.spin_for(FORWARD,50,DEGREES)
            self.prepared = False
            self.is_stretching = False
        else:
            self.set_stop()
    
accepter = Accepter()
accepter.execute_preload()

while True:
    if controller.buttonX.pressing():
        auto = not auto
        wait(0.2, SECONDS)

    if auto:
        if not accepter.prepared:
            accepter.prepare(ir)
        else:
            objects = vision.take_snapshot(vision_1__SIG_1)
            if objects == None:
                pass
            else:
                objects = vision.largest_object()
                if objects.height > 30 and objects.width > 50:
                    accepter.shoot(limit)
    else:
        if controller.buttonDown.pressing():
            stretch.spin(FORWARD)
        elif controller.buttonUp.pressing():
            stretch.spin(REVERSE)
        else:
            stretch.stop()
                    
        if controller.buttonA.pressing():
            throw.spin(FORWARD)
        else:
            throw.stop()

        if controller.buttonY.pressing():
            roller.spin(FORWARD)
        else:
            roller.stop()

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