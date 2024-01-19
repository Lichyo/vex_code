from vex import *
brain=Brain()
vision_20__SIG_1 = Signature(1, -6525, -6011, -6268,-5617, -5049, -5334,11, 0)
vision = Vision(Ports.PORT14, 50, vision_20__SIG_1)
controller = Controller()


left_motor_a = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
left_motor_b = Motor(Ports.PORT2, GearSetting.RATIO_18_1, False)
left_drive_smart = MotorGroup(left_motor_a, left_motor_b)
right_motor_a = Motor(Ports.PORT11, GearSetting.RATIO_18_1, True)
right_motor_b = Motor(Ports.PORT12, GearSetting.RATIO_18_1, True)
right_drive_smart = MotorGroup(right_motor_a, right_motor_b)
drivetrain_gps = Gps(Ports.PORT7, 0.00, 0.00, MM, 0)
driver = SmartDrive(left_drive_smart, right_drive_smart, drivetrain_gps, 319.19, 320, 40, MM, 1)

roller = Motor(Ports.PORT3, GearSetting.RATIO_18_1, True)
roller.set_velocity(60,PERCENT)
right_arm = Motor(Ports.PORT6, GearSetting.RATIO_18_1, False)
left_arm = Motor(Ports.PORT13, GearSetting.RATIO_18_1, False)
arm = MotorGroup(right_arm, left_arm)
arm.set_max_torque(90,PERCENT)
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
need_open_wings = False

def loading():
    arm.set_velocity(25, PERCENT)
    roller.spin(FORWARD)
    arm.set_stopping(COAST)
    arm.spin_for(FORWARD, 220, DEGREES) # 180 -> 300
    arm.stop()
    wait(0.6, SECONDS)
    arm.set_stopping(HOLD)
    arm.spin_for(REVERSE, 200, DEGREES)
    arm.stop()

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
    def move_to_target(self,need_to_open_wings = False):
        driver.set_drive_velocity(35, PERCENT)
        while not self.check_location():
            adjust_direction(self.theta)
            driver.drive_for(FORWARD, 150, MM)
            if need_to_open_wings:
                if axis.y < 500:
                    right_wing.spin_for(FORWARD, 230, DEGREES)
                    is_wings_open = True
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
        wings.spin_for(FORWARD, 250, DEGREES)
        wings.set_stopping(HOLD)
        wings.stop()
        is_wings_open = not is_wings_open    

def close_wings():
    global is_wings_open
    if is_wings_open:
        wings.spin_for(REVERSE, 230, DEGREES)
        wings.set_stopping(COAST)
        wings.stop()
        is_wings_open = not is_wings_open    

def rush(x,y, need_open_wings = False, strong = False, backward_distance = 300):
    axis.set_target(x,y)
    axis.update()
    driver.set_drive_velocity(75,PERCENT)
    Thread(close_wings)
    driver.drive_for(REVERSE,backward_distance,MM)
    adjust_direction(axis.theta)
    if need_open_wings:
        Thread(open_wings)
    adjust_direction(axis.theta)
    driver.set_timeout(1.3,SECONDS)
    rush_distance = 1100
    if strong:
        rush_distance = 1700
    driver.drive_for(FORWARD,rush_distance,MM)


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
    arm.stop()
    driver.drive_for(REVERSE, 350, MM)
    driver.turn_to_heading(60)

########################################################################################################################################################################
    
# init state
drivetrain_gps.calibrate()
axis = Axis()
wait(0.5, SECONDS)
Thread(axis.info)
# Thread(timer)

# execute_preload()
driver.set_drive_velocity(40, PERCENT)
driver.set_turn_velocity(30, PERCENT)
arm.spin_for(FORWARD,50,DEGREES)
arm.set_stopping(HOLD)
arm.stop()
roller.spin_for(REVERSE,350,DEGREES)
# loading()
loading()
loading()
loading()
loading()
loading()
loading()

driver.set_timeout(3, SECONDS)
roller.stop()
arm.set_stopping(COAST)
arm.stop()
driver.set_turn_velocity(10, PERCENT)
driver.turn_to_heading(80)
driver.set_drive_velocity(80,PERCENT)
left_wing.spin_for(FORWARD, 230, DEGREES)
axis.set_target(1200,1500)
while axis.x < 750:
    driver.drive(FORWARD)
driver.stop()
driver.turn_for(RIGHT,70,DEGREES)
right_wing.spin_for(FORWARD, 230, DEGREES)
is_wings_open = True
driver.set_timeout(2,SECONDS)
axis.set_target(1425, 800)
arm.set_stopping(HOLD)
arm.spin_for(FORWARD,80,DEGREES)
arm.stop()
driver.turn_to_heading(axis.theta)
driver.drive_for(FORWARD,650,MM)
axis.move_to_target()
driver.turn_to_heading(180)
Thread(close_wings)
driver.set_timeout(2.3,SECONDS)
rush(1570,500)
rush(1555,500)
rush(1580,500)
driver.drive_for(REVERSE, 500,MM)
left_wing.spin_for(FORWARD, 230, DEGREES)
driver.turn_to_heading(290)
axis.set_target(300,200)
driver.turn_to_heading(axis.theta)
driver.drive_for(FORWARD, 800 ,MM)
axis.move_to_target(need_to_open_wings = True)
driver.turn_to_heading(70)
close_wings()
rush(1300,0, need_open_wings = True, strong = True, backward_distance = 400)
driver.turn_to_heading(90)
rush(1300,0, need_open_wings = True, strong = True, backward_distance = 600)
driver.turn_to_heading(90)
rush(1300,0, need_open_wings = True, strong = True, backward_distance = 600)
driver.drive_for(REVERSE,200,MM)