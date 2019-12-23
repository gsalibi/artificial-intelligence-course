import sys, time
sys.path.insert(0, '../aux')
from robot import Robot
from skfuzzy import control as ctrl
from math import pi, atan2
import skfuzzy as fuzz
import numpy as np


def speed(dist, position, orientation):
    # angulo entre goal e posicao atual do robo
    a = atan2(position[1] - GOAL[1], GOAL[0] - position[0])

    # angulo que robo precisa rotacionar
    angle_1 = a + 2*pi
    angle_2 = orientation[2] + 2*pi
    angle = (angle_1 + angle_2) % (2*pi)
    if angle >= pi:
        angle -= 2*pi

    vel_ctrl.input["direction"] = angle

    for i in range(len(dist)):
        vel_ctrl.input['s' + str(i)] = dist[i]

    vel_ctrl.compute()
    return [vel_ctrl.output['v_left'], vel_ctrl.output['v_right']]


def is_goal(position):
    # compara a posicao do robô com tolerância de 0.1
    return position[0] > GOAL[0] - 0.1 and position[0] < GOAL[0] + 0.1 and position[1] > GOAL[1] - 0.1 and position[1] < GOAL[1] + 0.1


GOAL = (2.3, -2.5) # DEFINE OBJETIVO
MAX_SPEED = 3
robot = Robot()

# ditancia dos obstaculos
distance = []
for i in range(0, 8):
    distance.append(ctrl.Antecedent(np.arange(0, 6, 0.01), 's' + str(i)))
    # FIRST SETUP
    distance[i]['close'] = fuzz.trapmf(distance[i].universe, [0.0, 0.0, 0.3, 0.6])
    distance[i]['away'] = fuzz.trapmf(distance[i].universe, [0.3, 0.6, 5.0, 5.0])

    # SECOND SETUP
    # distance[i]['close'] = fuzz.trapmf(distance[i].universe, [0.0, 0.0, 0.6, 0.9])
    # distance[i]['away'] = fuzz.trapmf(distance[i].universe, [0.6, 0.9, 5.0, 5.0])

    distance[i].view()

# direcao do robo com relacao ao obstaculo
direction = ctrl.Antecedent(np.arange(-pi, pi, 0.0001), "direction")
direction['left'] = fuzz.trimf(direction.universe, [-pi, -pi/2, 0])
direction['right'] = fuzz.trimf(direction.universe, [0, pi/2, pi])
direction['front'] = fuzz.trimf(direction.universe, [-pi/2, 0, pi/2])
direction['zero'] = fuzz.trimf(direction.universe, [0, 0, 0]) #

direction.view()

v_left = ctrl.Consequent(np.arange(-MAX_SPEED, 1.0 + MAX_SPEED, 0.01), 'v_left')
v_right = ctrl.Consequent(np.arange(-MAX_SPEED, 1.0 + MAX_SPEED, 0.01), 'v_right')

v_left['positive'] = fuzz.trimf(v_left.universe, [0, MAX_SPEED, MAX_SPEED])
v_left['negative'] = fuzz.trimf(v_left.universe, [-MAX_SPEED, -MAX_SPEED, 0])
v_right['positive'] = fuzz.trimf(v_left.universe, [0, MAX_SPEED, MAX_SPEED])
v_right['negative'] = fuzz.trimf(v_left.universe, [-MAX_SPEED, -MAX_SPEED, 0])

v_left.view()
v_right.view()

no_obstacle = distance[0]['away'] & distance[1]['away'] & distance[2]['away'] & distance[3]['away'] & distance[4]['away'] & distance[5]['away'] & distance[6]['away'] & distance[7]['away']
obstacle_front = distance[2]['close'] | distance[3]['close'] | distance[4]['close'] | distance[5]['close']
obstable_left = distance[0]['close'] | distance[1]['close'] | distance[2]['close'] | distance[3]['close']
obstacle_right = distance[4]['close'] | distance[5]['close'] | distance[6]['close'] | distance[7]['close']


rule1 = ctrl.Rule(obstable_left, v_left['positive'])
rule2 = ctrl.Rule(obstacle_right & obstacle_front, v_left['negative'])
rule3 = ctrl.Rule(obstacle_right & ~ obstacle_front, v_left['positive'])
rule4 = ctrl.Rule(no_obstacle & (direction['front'] | direction['right']), v_left['positive'])
rule5 = ctrl.Rule(no_obstacle & direction['left'], v_left['negative'])
rule6 = ctrl.Rule(obstable_left & obstacle_front, v_right['negative'])
rule7 = ctrl.Rule(obstable_left & ~ obstacle_front, v_right['positive'])
rule8= ctrl.Rule(obstacle_right, v_right['positive'])
rule9 = ctrl.Rule(no_obstacle & (direction['front'] | direction['left']), v_right['positive'])
rule10 = ctrl.Rule(no_obstacle & direction['right'], v_right['negative'])

vel_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10])
vel_ctrl =  ctrl.ControlSystemSimulation(vel_ctrl)


while((robot.get_connection_status() != -1) and not is_goal(robot.get_current_position())):
    ultrassonic = robot.read_ultrassonic_sensors()[0:8]
    pos = robot.get_current_position()
    orient = robot.get_current_orientation()
    vel = speed(ultrassonic, pos, orient)
    robot.set_left_velocity(vel[0])  # rad/s
    robot.set_right_velocity(vel[1])
    print(robot.get_current_position())
    print(robot.get_simulation_time())
    time.sleep(0.1)

robot.set_left_velocity(0)
robot.set_right_velocity(0)

time.sleep(0.1)

if robot.get_connection_status() != -1:
    print("Destino alcançado")