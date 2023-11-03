from vex import *

brain=Brain()
vision_1__SIG_1 = Signature(1, -4789, -4193, -4492,-5041, -4557, -4800,3.9, 0)
vision_1 = Vision(Ports.PORT1, 50, vision_1__SIG_1)
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
driver.set_drive_velocity(65, PERCENT)
driver.set_turn_velocity(15, PERCENT)
driver.set_stopping(COAST)
left_wing = Motor(Ports.PORT13, GearSetting.RATIO_18_1, False)
right_wing = Motor(Ports.PORT14, GearSetting.RATIO_18_1, True)
wings = MotorGroup(left_wing, right_wing)
wings.set_max_torque(100,PERCENT)
wings.set_velocity(40,PERCENT)
wings.set_timeout(1,SECONDS)
is_arrived = False 
global is_wings_open
is_wings_open = False


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
        wait(0.3,SECONDS)

    def set_theta(self):
        self.set_quadrant
        self.position()
        cos = self.a/self.b
        self.correct_angle_in_radian = math.acos(cos)
        self.correct_angle_in_radian = math.degrees(self.correct_angle_in_radian)
    
        if self.quadrant == 1:
            self.theta = 270 - self.correct_angle_in_radian
        elif self.quadrant == 2:
            self.theta = 270 - self.correct_angle_in_radian
        elif self.quadrant == 3:
            self.theta = 270 + self.correct_angle_in_radian
        else:
            self.theta = 270 + self.correct_angle_in_radian

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
    

axis = Axis()

drivetrain_gps.calibrate()
wait(0.5,SECONDS)

while True:
    axis.info()
    if not is_arrived:
        if axis.x > 300:
            axis.set_target(100, 0)
            adjust_direction(axis.theta)
            driver.drive(FORWARD)
        elif axis.x > -200:
            adjust_direction(270)
            open_wings()
            driver.drive_for(FORWARD, 700, MM)
        elif axis.x > -600:
            axis.set_target(-1100, 0)
            adjust_direction(axis.theta)
            driver.drive(FORWARD)
        else:
            adjust_direction(270)
            driver.drive_for(FORWARD, 1000, MM)
            is_arrived = True
    else:
        driver.stop()