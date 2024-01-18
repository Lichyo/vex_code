from vex import *
left_motor_a = Motor(Ports.PORT5, GearSetting.RATIO_18_1, False)
left_motor_b = Motor(Ports.PORT6, GearSetting.RATIO_18_1, False)
left_wheels = MotorGroup(left_motor_a, left_motor_b)
right_motor_a = Motor(Ports.PORT7, GearSetting.RATIO_18_1, True)
right_motor_b = Motor(Ports.PORT8, GearSetting.RATIO_18_1, True)
right_wheels = MotorGroup(right_motor_a, right_motor_b)
drivetrain_gps = Gps(Ports.PORT19, 160.00, 20.00, MM, 180)
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
arm = Motor(Ports.PORT15, GearSetting.RATIO_36_1, False)
arm.set_timeout(1,SECONDS)
throw.set_stopping(HOLD)
throw.set_velocity(40, PERCENT)
throw.set_max_torque(100, PERCENT)
stretch.set_velocity(80, PERCENT)
stretch.set_stopping(COAST)
stretch.set_timeout(1, SECONDS)
throw.set_timeout(1, SECONDS)
is_strethced = False

class Axis:
    def __init__(self):
        self.x0 = 0
        self.y0 = 0

    def position(self): 
        self.x = drivetrain_gps.x_position(MM)
        self.y = drivetrain_gps.y_position(MM)
        self.head = drivetrain_gps.heading()
        self.a = abs(self.x-self.x0)
        self.c = abs(self.y-self.y0)
        self.b = math.sqrt(math.pow(self.a,2)+math.pow(self.c,2))
    
    def set_quadrant(self):
        self.position()
        if self.x > 0:
            if self.y > 0:
                self.quadrant = 1
            else:
                self.quadrant = 4
        else:
            if self.y > 0:
                self.quadrant = 2
            else:
                self.quadrant = 3

    def set_quadrant_with_target(self):
        self.position()
        if self.x - self.x0 > 0:
            if self.y - self.y0 > 0:
                self.quadrant_with_target = 1
            else:
                self.quadrant_with_target = 4
        else:
            if self.y - self.y0 > 0:
                self.quadrant_with_target = 2
            else:
                self.quadrant_with_target = 3

    def set_target(self, x, y):
        self.x0 = x
        self.y0 = y
        self.update()

    def update(self):
        self.set_quadrant_with_target()
        self.set_theta_with_target()
        self.position()

    def info(self):
        while True:
            self.update()
            brain.screen.clear_screen()
            brain.screen.set_cursor(1, 1)
            brain.screen.print('check locaion: ', self.check_location())
            brain.screen.next_row()
            brain.screen.print('x0: ',self.x0, 'y0: ',self.y0)
            brain.screen.next_row()
            brain.screen.print('x: ',self.x)
            brain.screen.next_row()
            brain.screen.print('y: ',self.y)
            brain.screen.next_row()
            brain.screen.print('head: ',self.head)
            brain.screen.next_row()
            brain.screen.print('quadrant: ',self.quadrant_with_target)
            brain.screen.next_row()
            brain.screen.print('theta:' , self.theta)
            brain.screen.next_row()
            brain.screen.print('correct: ' , self.correct_angle_in_radian_with_target)
            brain.screen.next_row()
            brain.screen.print('quadrant with target: ' , self.quadrant_with_target)
            brain.screen.next_row()
            wait(0.1,SECONDS)

    def set_theta_with_target(self):
        self.set_quadrant_with_target()
        self.position()
        cos = self.a/self.b
        self.correct_angle_in_radian_with_target = math.acos(cos)
        self.correct_angle_in_radian_with_target = math.degrees(self.correct_angle_in_radian_with_target)
        if self.quadrant_with_target == 1:
            self.theta = 270 - self.correct_angle_in_radian_with_target
        elif self.quadrant_with_target == 2:
            self.theta = 90 + self.correct_angle_in_radian_with_target
        elif self.quadrant_with_target == 3:
            self.theta = 90 - self.correct_angle_in_radian_with_target
        else:
            self.theta = 270 + self.correct_angle_in_radian_with_target

    def check_location(self):
        if (axis.x < axis.x0 + 150 and axis.x > axis.x0 - 150) and (axis.y > axis.y0 -150 and axis.y < axis.y0 + 150):
            return True
        else:
            return False
    def move_to_target(self, x , y):
        self.set_target(x, y)
        driver.set_drive_velocity(35, PERCENT)
        while not self.check_location():
            adjust_direction(self.theta)
            driver.drive_for(FORWARD, 150, MM)
        driver.stop()
        return

def adjust_direction(angles):
    driver.set_turn_velocity(10, PERCENT)
    if angles > 354 or angles < 6:
        driver.turn_to_heading(0, DEGREES)
    elif not(axis.head < angles + 5 and axis.head > angles -5):
        driver.turn_to_heading(angles,DEGREES)

class Accepter:
    def __init__(self):
        self.prepared = False
        self.is_stretching = False
    
    def throw_prepare(self,ir):
        throw.set_velocity(80, PERCENT)
        while ir.value() == 1: 
            throw.spin(FORWARD)
        throw.stop()
        
    def stretch_prepare(self):
        if self.is_stretching:
            pass
        else:
            self.is_stretching = True
            stretch.spin_for(FORWARD, 470, DEGREES)
    
    def prepare(self,ir):
        if self.is_stretching:
           self.set_stop()
        else:
            Thread(lambda: driver.drive_for(REVERSE, 2, MM))
            Thread(self.stretch_prepare)
            self.throw_prepare(ir)
            self.prepared = True


        
            
    def execute_preload(self): 
        Thread(lambda: arm.spin_for(FORWARD,180,DEGREES) )
        self.prepare(ir)
        arm.spin_for(REVERSE,180,DEGREES)
        

    def set_stop(self):
        throw.stop()
        stretch.stop()

    def shoot(self):
        if self.prepared:
            throw.set_velocity(60, PERCENT)
            stretch.spin_for(REVERSE, 450, DEGREES)
            throw.spin_for(FORWARD,50,DEGREES)
            self.prepared = False
            self.is_stretching = False
        else:
            self.set_stop()
    
    
counter = 0
axis = Axis()
accepter = Accepter()
# accepter.execute_preload()
# while True and counter < 23:
#     if not accepter.prepared:
#         accepter.prepare(ir)
#     else:
#         objects = vision.take_snapshot(vision_1__SIG_1)
#         if objects == None:
#             pass
#         else:
#             objects = vision.largest_object()
#             if objects.height > 30 and objects.width > 50:
#                 accepter.shoot()
#                 counter = counter + 1
driver.drive_for(FORWARD, 150, MM)
drivetrain_gps.calibrate()
wait(0.2, SECONDS)
axis.set_target(0, 0)
wait(0.1, SECONDS)
driver.set_turn_velocity(20, PERCENT)
driver.turn_to_heading(axis.theta)
driver.set_drive_velocity(50, PERCENT)
driver.drive_for(FORWARD, 1400, MM)
axis.set_target(-1200, 1500)
wait(0.1, SECONDS)
driver.set_drive_velocity(20, PERCENT)
driver.set_turn_velocity(20, PERCENT)
driver.turn_to_heading(axis.theta)
driver.set_drive_velocity(50, PERCENT)
driver.drive_for(FORWARD, 1400, MM)
driver.turn_to_heading(120)
driver.drive_for(REVERSE, 400, MM)
