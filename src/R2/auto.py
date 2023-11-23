from vex import *
arm = Motor(Ports.PORT15, GearSetting.RATIO_18_1, False)
left_motor_a = Motor(Ports.PORT5, GearSetting.RATIO_18_1, False)
left_motor_b = Motor(Ports.PORT6, GearSetting.RATIO_18_1, False)
left_wheels = MotorGroup(left_motor_a, left_motor_b)
right_motor_a = Motor(Ports.PORT7, GearSetting.RATIO_18_1, True)
right_motor_b = Motor(Ports.PORT8, GearSetting.RATIO_18_1, True)
right_wheels = MotorGroup(right_motor_a, right_motor_b)
h_wheel = Motor(Ports.PORT16, GearSetting.RATIO_18_1, False)
gps = Gps(Ports.PORT20, 160.00, 20.00, MM, 180)
driver = SmartDrive(left_wheels, right_wheels, gps, 319.19, 320, 40, MM, 1)
brain = Brain()
controller = Controller()
driver.set_drive_velocity(10, PERCENT)
h_wheel.set_velocity(70, PERCENT)
h_wheel.set_max_torque(100, PERCENT)

vision_1__SIG_1 = Signature(1, -4789, -4193, -4492,-5041, -4557, -4800,3.9, 0)
vision = Vision(Ports.PORT1, 50, vision_1__SIG_1)
stretch = Motor(Ports.PORT2, GearSetting.RATIO_18_1, False)
throw_1 = Motor(Ports.PORT4, GearSetting.RATIO_36_1, False)
throw_2 = Motor(Ports.PORT3, GearSetting.RATIO_36_1, True)
roller = Motor(Ports.PORT10, GearSetting.RATIO_36_1, True)
throw= MotorGroup(throw_1, throw_2)
throw.set_stopping(HOLD)
throw.set_velocity(50, PERCENT)
throw.set_max_torque(100, PERCENT)
stretch.set_velocity(90, PERCENT)
stretch.set_stopping(COAST)
stretch.set_timeout(1, SECONDS)
throw.set_timeout(2, SECONDS)
roller.set_velocity(100, PERCENT)
is_timeout = False

class Axis:
    def __init__(self):
        self.x0 = 0
        self.y0 = 0

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

    def position(self): 
        self.x = gps.x_position(MM)
        self.y = gps.y_position(MM)
        self.head = gps.heading()
        self.a = abs(self.x-self.x0)
        self.c = abs(self.y-self.y0)
        self.b = math.sqrt(math.pow(self.a,2)+math.pow(self.c,2))
        
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

    def update(self):
        self.set_quadrant_with_target()
        self.set_theta_with_target()
        self.position()
        
    def check_location(self):
        if (axis.x < axis.x0 + 100 and axis.x > axis.x0 - 100) and (axis.y > axis.y0 -100 and axis.y < axis.y0 + 100):
            return True
        else:
            return False
        
    def move_to_target(self,):
        driver.set_drive_velocity(40, PERCENT)
        while not self.check_location():
            adjust_direction(self.theta)
            driver.drive_for(FORWARD, 100, MM)
        driver.stop()
        return

    def move_out_to_shoot(self):
        # roller.spin(REVERSE)
        # self.set_target(300,400)
        # self.move_to_target()
        # driver.turn_to_heading(270)
        # driver.drive_for(FORWARD,100,MM)
        # driver.drive_for(REVERSE,200,MM)

        h_wheel.spin_for(REVERSE, 7, TURNS)

        # driver.drive_for(FORWARD,200,MM)

def adjust_direction(angles):
    driver.set_turn_velocity(10, PERCENT)
    if angles > 354 or angles < 6:
        driver.turn_to_heading(0, DEGREES)
    elif not(axis.head < angles + 5 and axis.head > angles -5):
        driver.turn_to_heading(angles)
        
    
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
            stretch.spin_for(FORWARD, 500, DEGREES)
    
    
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
            stretch.spin_for(REVERSE, 500, DEGREES)
            throw.spin_for(FORWARD, 200, DEGREES)
            throw.stop()
            self.prepared = False
            self.is_stretching = False
        else:
            self.set_stop()
            
    def execute_preload(self): 
        Thread(lambda: arm.spin_for(FORWARD,180,DEGREES) )
        self.throw_prepare()
        stretch.spin_for(FORWARD, 500, DEGREES)
        arm.spin_for(REVERSE,180,DEGREES)
        self.prepared = True
        self.is_stretching = True
        self.shoot()
        
def timeout():
    wait(50,SECONDS)
    is_timeout = True
gps.calibrate()
axis = Axis()
Thread(axis.info)
# timeout()          
accepter = Accepter()
# accepter.execute_preload()
axis.move_out_to_shoot() 
# while True:
#     if not accepter.prepared and not is_timeout :
#         accepter.prepare()
#     elif accepter.prepared:
#         objects = vision.take_snapshot(vision_1__SIG_1)
#         if objects == None:
#             pass
#         else:
#             objects = vision.largest_object()
#             if objects.height > 20 and objects.width > 30:
#                 accepter.shoot()
#     else:  
#         axis.move_out_to_shoot() 
