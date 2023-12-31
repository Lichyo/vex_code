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
driver.set_drive_velocity(10, PERCENT)

vision_1__SIG_1 = Signature(1, -4789, -4193, -4492,-5041, -4557, -4800,3.9, 0)
vision = Vision(Ports.PORT1, 50, vision_1__SIG_1)
stretch = Motor(Ports.PORT2, GearSetting.RATIO_18_1, False)
throw_1 = Motor(Ports.PORT4, GearSetting.RATIO_36_1, False)
throw_2 = Motor(Ports.PORT3, GearSetting.RATIO_36_1, True)
throw= MotorGroup(throw_1, throw_2)
throw.set_stopping(HOLD)
throw.set_velocity(40, PERCENT)
throw.set_max_torque(100, PERCENT)
stretch.set_velocity(80, PERCENT)
stretch.set_stopping(COAST)
stretch.set_timeout(1, SECONDS)
throw.set_timeout(1, SECONDS)
is_strethced = False


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
            # Thread(lambda: driver.drive_for(REVERSE, 30, MM))
            # Thread(self.throw_prepare(ir))
            Thread(self.stretch_prepare)
            self.throw_prepare(ir)
            self.prepared = True
        

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
while True:
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



    # if limit.value() == 0 and not is_stretched:
    #     stretch.spin_for(FORWARD,500,DEGREES)
    #     is_stretched = 1
    # elif limit.value() == 1:
    #     stretch.spin(REVERSE)
    #     is_stretched = 0
    # brain.screen.print(ir.value())
    # if ir.value() == 0 :
    #     throw.spin_for(FORWARD,30,DEGREES)
    # elif ir.value() == 1:
    #     throw.spin(FORWARD)
    # brain.screen.print(ir.value())
    # wait(0.2,SECONDS)
    # brain.screen.clear_screen()
    # brain.screen.set_cursor(1,1)

