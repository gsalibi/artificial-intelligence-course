import sys, time
sys.path.insert(0, '../aux')
from robot import Robot
from skfuzzy import control as ctrl
from math import pi
import skfuzzy as fuzz
import numpy as np


def compute_speed(speed_ctrl, forward, right):
    speed_ctrl.input['distanceF'] = forward
    speed_ctrl.input['distanceR'] = right
    speed_ctrl.compute()
    return (speed_ctrl.output['speed_left'], speed_ctrl.output['speed_right'])



MAX_SPEED  = 3
# FIRST SETUP
VERY_CLOSE = [0.0, 0.0, 0.2, 0.4]
CLOSE      = [0.2, 0.4, 0.6, 0.8]
AWAY       = [0.6, 0.8, 1.0, 1.2]
FAR_AWAY   = [1.0, 1.2, 5.0, 5.0]


# SECOND SETUP
# VERY_CLOSE = [0.0, 0.0, 0.4, 0.5]
# CLOSE      = [0.4, 0.6, 0.8, 1.0]
# AWAY       = [0.8, 1.0, 1.2, 1.4]
# FAR_AWAY   = [1.2, 1.4, 5.0, 5.0]


distanceF = ctrl.Antecedent(np.arange(0, 5, 0.01), 'distanceF')
distanceF['VERY_CLOSE'] = fuzz.trapmf(distanceF.universe, VERY_CLOSE)
distanceF['CLOSE'] = fuzz.trapmf(distanceF.universe, CLOSE)
distanceF['AWAY'] = fuzz.trapmf(distanceF.universe, AWAY)
distanceF['FAR_AWAY'] = fuzz.trapmf(distanceF.universe, FAR_AWAY)

distanceF.view()

distanceR = ctrl.Antecedent(np.arange(0, 5, 0.01), 'distanceR')
distanceR['VERY_CLOSE'] = fuzz.trapmf(distanceR.universe, VERY_CLOSE)
distanceR['CLOSE'] = fuzz.trapmf(distanceR.universe, CLOSE)
distanceR['AWAY'] = fuzz.trapmf(distanceF.universe, AWAY)
distanceR['FAR_AWAY'] = fuzz.trapmf(distanceF.universe, FAR_AWAY)

distanceR.view()

# Set left Speed
speed_left = ctrl.Consequent(np.arange(-MAX_SPEED, MAX_SPEED + 1, 0.01), 'speed_left')
speed_left['positive'] = fuzz.trimf(speed_left.universe, [0.0, MAX_SPEED/2, MAX_SPEED])
speed_left['very_positive'] = fuzz.trimf(speed_left.universe, [MAX_SPEED/2, MAX_SPEED, MAX_SPEED])
speed_left['negative'] = fuzz.trimf(speed_left.universe, [-MAX_SPEED, -MAX_SPEED/2, 0.0])
speed_left['very_negative'] = fuzz.trimf(speed_left.universe, [-MAX_SPEED, -MAX_SPEED, -MAX_SPEED/2])

# Set right Speed
speed_right = ctrl.Consequent(np.arange(-MAX_SPEED, MAX_SPEED + 1, 0.01), 'speed_right')
speed_right['positive'] = fuzz.trimf(speed_right.universe, [0.0, MAX_SPEED/2, MAX_SPEED])
speed_right['very_positive'] = fuzz.trimf(speed_right.universe, [MAX_SPEED/2, MAX_SPEED, MAX_SPEED])
speed_right['negative'] = fuzz.trimf(speed_right.universe, [-MAX_SPEED, -MAX_SPEED/2, 0.0])
speed_right['very_negative'] = fuzz.trimf(speed_right.universe, [-MAX_SPEED, -MAX_SPEED, -MAX_SPEED/2])

speed_left.view()
speed_right.view()

rule1 = ctrl.Rule((distanceF['FAR_AWAY'] | distanceF['AWAY']) & (distanceR['FAR_AWAY'] | distanceR['AWAY']), speed_left['very_positive'])
rule2 = ctrl.Rule((distanceF['FAR_AWAY'] | distanceF['AWAY']) & (distanceR['FAR_AWAY'] | distanceR['AWAY']), speed_right['positive'])
rule3 = ctrl.Rule((distanceF['FAR_AWAY'] | distanceF['AWAY']) & distanceR['CLOSE'], speed_left['very_positive'])
rule4 = ctrl.Rule((distanceF['FAR_AWAY'] | distanceF['AWAY']) & distanceR['CLOSE'], speed_right['very_positive'])
rule5 = ctrl.Rule((distanceF['FAR_AWAY'] | distanceF['AWAY']) & distanceR['VERY_CLOSE'], speed_left['positive'])
rule6 = ctrl.Rule((distanceF['FAR_AWAY'] | distanceF['AWAY']) & distanceR['VERY_CLOSE'], speed_right['very_positive'])
rule7 = ctrl.Rule((distanceF['FAR_AWAY'] | distanceF['AWAY']) & distanceR['VERY_CLOSE'], speed_left['positive'])
rule8 = ctrl.Rule((distanceF['FAR_AWAY'] | distanceF['AWAY']) & distanceR['VERY_CLOSE'], speed_right['very_positive'])
rule9 = ctrl.Rule(distanceF['CLOSE'], speed_left['negative'])
rule10 = ctrl.Rule(distanceF['CLOSE'], speed_right['positive'])
rule11 = ctrl.Rule((distanceF['VERY_CLOSE'] | distanceF['CLOSE']) & (distanceR['FAR_AWAY'] | distanceR['AWAY']), speed_left['very_negative'])
rule12 = ctrl.Rule((distanceF['VERY_CLOSE'] | distanceF['CLOSE']) & (distanceR['FAR_AWAY'] | distanceR['AWAY']), speed_right['negative'])
rule13 = ctrl.Rule((distanceF['VERY_CLOSE'] | distanceF['CLOSE']) & (distanceR['FAR_AWAY'] | distanceR['AWAY']), speed_left['negative'])
rule14 = ctrl.Rule((distanceF['VERY_CLOSE'] | distanceF['CLOSE']) & (distanceR['VERY_CLOSE'] | distanceR['CLOSE']), speed_right['negative'])

speed_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10, rule11, rule12, rule13, rule14])
speed_ctrl = ctrl.ControlSystemSimulation(speed_ctrl)


robot = Robot()
print(robot.get_current_position())

while robot.get_connection_status() != -1:
    robot.set_velocity(0,0)

    ultrassonic = robot.read_ultrassonic_sensors()
    forward = ultrassonic[5]
    right = ultrassonic[8]

    if forward > 4:
        forward = 4

    if right > 4:
        right = 4


    speed_l, speed_r = compute_speed(speed_ctrl, forward, right)
    robot.set_left_velocity(speed_l)
    robot.set_right_velocity(speed_r)

    print("forward = {:07.3f} | right = {:07.3f} | speed_l = {:07.3f} | speed_r = {:07.3f}".format(forward, right, speed_l, speed_r))
    print(robot.get_simulation_time())
    #sleep
    time.sleep(0.1)
