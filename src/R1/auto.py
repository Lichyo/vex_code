from vex import *

brain=Brain()

vision_20__SIG_1 = Signature(1, -6525, -6011, -6268,-5617, -5049, -5334,11, 0)
vision = Vision(Ports.PORT20, 50, vision_20__SIG_1)
controller = Controller()

left_motor_a = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
left_motor_b = Motor(Ports.PORT2, GearSetting.RATIO_18_1, False)
left_drive_smart = MotorGroup(left_motor_a, left_motor_b)
right_motor_a = Motor(Ports.PORT3, GearSetting.RATIO_18_1, True)
right_motor_b = Motor(Ports.PORT4, GearSetting.RATIO_18_1, True)
right_drive_smart = MotorGroup(right_motor_a, right_motor_b)
accepter = Motor(Ports.PORT7, GearSetting.RATIO_18_1, True)
arm = Motor(Ports.PORT8, GearSetting.RATIO_18_1, False)
drivetrain_gps = Gps(Ports.PORT11, 0.00, -40.00, MM, 0)
driver = SmartDrive(left_drive_smart, right_drive_smart, drivetrain_gps, 319.19, 320, 40, MM, 1)
arm.set_stopping(COAST)

driver.set_drive_velocity(50, PERCENT)
driver.set_turn_velocity(15, PERCENT)
driver.set_stopping(COAST)
driver.set_timeout(5, SECONDS)

left_wing = Motor(Ports.PORT13, GearSetting.RATIO_18_1, False)
right_wing = Motor(Ports.PORT14, GearSetting.RATIO_18_1, True)
wings = MotorGroup(left_wing, right_wing)
wings.set_velocity(20,PERCENT)
wings.set_timeout(1,SECONDS)
wings.set_max_torque(100, PERCENT)
accepter.set_velocity(80, PERCENT)
arm.set_stopping(COAST)
global is_wings_open
is_wings_open = False

global status
status = 'stop'

global timeout 
timeout = False

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

########################################################################################################################################################################

def adjust_direction(angles):
    driver.set_turn_velocity(10, PERCENT)
    if angles > 354 or angles < 6:
        driver.turn_to_heading(0, DEGREES)
    elif not(axis.head < angles + 5 and axis.head > angles -5):
        driver.turn_to_heading(angles,DEGREES)

def open_wings():
    global is_wings_open
    if is_wings_open:
        pass
    else:
        wings.spin_for(FORWARD, 200, DEGREES)
        is_wings_open = not is_wings_open    

def close_wings():
    global is_wings_open
    if is_wings_open:
        wings.spin_for(REVERSE, 200, DEGREES)
        is_wings_open = not is_wings_open    


def closing_object(center_x):
    if center_x < 100:
        driver.turn(LEFT, 5, PERCENT)
    elif center_x > 190:
        driver.turn(RIGHT, 5, PERCENT)
    else : 
        driver.drive_for(FORWARD, 80, MM)

def shooting():
    objects = vision.take_snapshot(vision_20__SIG_1)
    
    if objects == None:
        finding_object()
    else:
        objects = vision.largest_object()
        center_x = objects.centerX
        w = objects.width 
        h = objects.height
        
        if w > 210 and h > 110:
            bouncing()
        elif w > 30 and h > 30:
            grabbing(center_x)
        else :
            finding_object()
            
def finding_object():
    Thread(lambda: accepter.stop())
    driver.turn_for(RIGHT, 10, DEGREES)   
            
def grabbing(center_x):
    Thread(lambda: accepter.spin(FORWARD))
    closing_object(center_x)        
            
def bouncing():
    adjust_direction(270)
    driver.drive_for(FORWARD, 200, MM)
    accepter.spin_for(REVERSE,2,TURNS)
    driver.drive_for(REVERSE, 300, MM)
    driver.turn_to_heading(295)
    Thread(lambda: accepter.spin(REVERSE))

def rush_in_front_of_goal():
    driver.set_drive_velocity(90,PERCENT)
    Thread(close_wings)
    adjust_direction(270)
    driver.drive_for(REVERSE,500,MM)
    Thread(open_wings)
    # adjust_direction(270)
    driver.set_timeout(1.2,SECONDS)
    driver.drive_for(FORWARD,1000,MM)


def timer():
    global timeout
    wait(15,SECONDS)
    timeout = True
    driver.set_timeout(5, SECONDS)

def execute_preload():
    driver.set_stopping(COAST)
    driver.set_timeout(2, SECONDS)
    driver.set_drive_velocity(50,PERCENT)
    driver.drive_for(FORWARD, 300, MM)
    driver.set_drive_velocity(90,PERCENT)
    driver.drive_for(FORWARD, 1200, MM)
    driver.set_timeout(1, SECONDS)
    arm.spin_for(FORWARD, 270, DEGREES)
    arm.set_stopping(COAST)
    arm.stop()
    driver.drive_for(REVERSE, 300, MM)
    driver.turn_to_heading(245)

########################################################################################################################################################################
    
# init state
axis = Axis()
drivetrain_gps.calibrate()
wait(0.5, SECONDS)
Thread(axis.info)
Thread(timer)

execute_preload()
driver.set_drive_velocity(40, PERCENT)
driver.set_turn_velocity(30, PERCENT)
while True:
    if timeout:
        accepter.stop()
        arm.spin_for(REVERSE, 270, DEGREES)
        arm.stop()
        # driver.turn_to_heading(0)
        adjust_direction(0)
        driver.set_drive_velocity(50, PERCENT)
        while not(axis.check_location()):
            driver.drive(REVERSE)
            if axis.y < -1450:
                break
        driver.set_turn_velocity(30, PERCENT)
        driver.set_timeout(2,SECONDS)
        adjust_direction(270)
        axis.set_target(-1100, -1500)
        driver.set_drive_velocity(70, PERCENT)
        while not(axis.check_location()):
            driver.drive(FORWARD)
            if axis.x < -300:
                right_wing.spin_for(FORWARD, 200, DEGREES)
            if axis.x < -800:
                break
        axis.set_target(-1000, -1300)
        axis.move_to_target()
        left_wing.spin_for(FORWARD, 200, DEGREES)
        is_wings_open = True
        axis.set_target(-400,-100)
        axis.move_to_target()
        axis.set_target(-900,100)
        axis.move_to_target()
        close_wings()
        rush_in_front_of_goal()
        wait(0.1,SECONDS)
        rush_in_front_of_goal()
    else:
        shooting()