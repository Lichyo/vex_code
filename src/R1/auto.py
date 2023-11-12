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
wings.set_max_torque(100,PERCENT)
wings.set_velocity(40,PERCENT)
wings.set_timeout(1,SECONDS)

accepter.set_velocity(80, PERCENT)
is_arrived = False 
global is_wings_open
is_wings_open = False
global status
status = 'stop'

global timeout 
timeout = False
class Axis:
    def __init__(self):
        self.x0 = -1100
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

    def set_target(self, x, y):
        self.x0 = x
        self.y0 = y
        self.update()

    def update(self):
        self.set_quadrant()
        self.set_theta()
        self.position()

    def info(self):
        while True:
            self.update()
            brain.screen.clear_screen()
            brain.screen.set_cursor(1, 1)
            brain.screen.print('x0: ',self.x0, 'y0: ',self.y0)
            brain.screen.next_row()
            brain.screen.print('x: ',self.x)
            brain.screen.next_row()
            brain.screen.print('y: ',self.y)
            brain.screen.next_row()
            brain.screen.print('head: ',self.head)
            brain.screen.next_row()
            brain.screen.print('quadrant: ',self.quadrant)
            brain.screen.next_row()
            brain.screen.print('theta:' , self.theta)
            brain.screen.next_row()
            brain.screen.print('correct: ' , self.correct_angle_in_radian)
            brain.screen.next_row()
            wait(0.1,SECONDS)

    def set_theta(self):
        self.set_quadrant
        self.position()
        cos = self.a/self.b
        self.correct_angle_in_radian = math.acos(cos)
        self.correct_angle_in_radian = math.degrees(self.correct_angle_in_radian)
        if self.x < self.x0:
            if self.quadrant == 1:
                self.theta = 90 + self.correct_angle_in_radian
            elif self.quadrant == 2:
                self.theta = 90 + self.correct_angle_in_radian
            elif self.quadrant == 3:
                self.theta = 90 - self.correct_angle_in_radian
            else:
                self.theta = 90 - self.correct_angle_in_radian
        else:
            if self.quadrant == 1:
                self.theta = 270 - self.correct_angle_in_radian
            elif self.quadrant == 2:
                self.theta = 270 - self.correct_angle_in_radian
            elif self.quadrant == 3:
                self.theta = 270 + self.correct_angle_in_radian
            else:
                self.theta = 270 + self.correct_angle_in_radian
    def check_location(self):
        if (axis.x < axis.x0 + 100 and axis.x > axis.x0 - 100) and (axis.y > axis.y0 -100 and axis.y < axis.y0 +100):
            return True
        else:
            return False
    def move_to_target(self, direction):
        while not axis.check_location():
            self.set_theta()
            adjust_direction(self.theta)
            driver.drive(direction)

####################################################################################

def adjust_direction(angles):
    if not(axis.head < angles + 10 and axis.head > angles -10):
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
    if center_x < 110:
        driver.turn(LEFT, 5, PERCENT)
    elif center_x > 180:
        driver.turn(RIGHT, 5, PERCENT)
    else : 
        driver.drive(FORWARD)



def shooting():
    global status
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
    global status
    status = 'forward'
    driver.drive_for(FORWARD, 30, MM)
    driver.turn(LEFT, 15, PERCENT)   
            
def grabbing(center_x):
    global status
    status = 'forward'
    closing_object(center_x)        
            
def bouncing():
    global status
    driver.turn_to_heading(270)
    driver.drive_for(FORWARD, 200, MM)
    accepter.spin_for(REVERSE,2,TURNS)
    driver.drive_for(REVERSE, 500, MM)
    driver.turn_to_heading(245)
    status = 'release'
            
def accepter_activated():
    global status
    if status == 'forward':
        Thread(lambda: accepter.spin(FORWARD))
    elif status == 'release':
        Thread(lambda:accepter.spin_for(REVERSE, 5, TURNS))
    else:
        accepter.stop() 

axis = Axis()
drivetrain_gps.calibrate()
wait(0.3,SECONDS)

def cross_line():
    accepter.stop()
    arm.spin_for(REVERSE, 270, DEGREES)
    arm.stop()
    driver.set_timeout(5,SECONDS)
    axis.set_target(500, 0)
    axis.set_theta()
    driver.set_drive_velocity(60, PERCENT)
    axis.move_to_target(FORWARD)
    driver.stop()
    axis.update()
    driver.turn_to_heading(90)
    wait(0.1, SECONDS)
    driver.turn_to_heading(90)
    axis.set_target(-800,0)
    driver.turn_to_heading(90)
    while not(axis.check_location()):
        driver.drive_for(REVERSE,500,MM)

        if axis.x < -450:
            driver.turn_to_heading(270)
            open_wings()
            driver.set_drive_velocity(80,PERCENT)
            driver.turn_to_heading(270)
            driver.drive_for(FORWARD,800,MM)
            close_wings()
            driver.set_drive_velocity(50, PERCENT)
            break

def timer():
    global timeout
    wait(30,SECONDS)
    timeout = True
    driver.set_timeout(5, SECONDS)

def execute_preload():
    arm.set_stopping(COAST)
    
    driver.drive_for(FORWARD, 1800, MM)
    driver.set_timeout(1.5, SECONDS)
    arm.spin_for(FORWARD, 270, DEGREES)
    driver.drive_for(REVERSE, 300, MM)
    driver.turn_to_heading(245)
    arm.stop()


Thread(axis.info)
Thread(timer)    
execute_preload()
while True:
    if timeout:
        cross_line()
        driver.drive_for(REVERSE, 100, MM)
        driver.turn_to_heading(190)
        open_wings()
        driver.drive_for(FORWARD, 1400, MM)
        axis.set_target(-1500, -800)
        close_wings()
        axis.move_to_target(FORWARD)
        right_wing.spin_for(FORWARD, 200, DEGREES)
        driver.set_drive_velocity(70, PERCENT)
        driver.drive_for(REVERSE,300,MM)
        driver.drive_for(FORWARD,400,MM)
        driver.drive_for(REVERSE,300,MM)
        driver.drive_for(FORWARD,400,MM)
        

    else:
        accepter_activated()
        shooting()