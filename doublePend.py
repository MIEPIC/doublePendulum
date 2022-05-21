from random import getrandbits
import pygame
from pygame.locals import *
import math

var_escape = False
global stretchColor
g = 10
scale = 50
hinge = (300, 300)

pygame.init()
window = pygame.display.set_mode((600, 600))

window.fill((255, 255, 0))

def clamp(n, smallest, largest):
    return max(smallest, min(n, largest))


def drawPendulums(theta1, theta2, theta3, l1, l2, l3, scale):
    #Drawing arms along with scaling factor
    pygame.draw.line(window, (0,0,0), [hinge[0], hinge[1]], [hinge[0]+math.sin(theta1)*l1*scale, hinge[1]+math.cos(theta1)*l1*scale])
    pygame.draw.line(window, (0,0,0), [hinge[0]+math.sin(theta1)*l1*scale, hinge[1]+math.cos(theta1)*l1*scale], [hinge[0]+math.sin(theta1)*l1*scale + math.sin(theta2)*l2*scale, hinge[1]+math.cos(theta1)*l1*scale + math.cos(theta2)*l2*scale])
    pygame.draw.line(window, (0,0,0), [hinge[0]+math.sin(theta1)*l1*scale + math.sin(theta2)*l2*scale, hinge[1]+math.cos(theta1)*l1*scale + math.cos(theta2)*l2*scale], [hinge[0]+math.sin(theta1)*l1*scale + math.sin(theta2)*l2*scale + math.sin(theta3)*l3*scale, hinge[1]+math.cos(theta1)*l1*scale + math.cos(theta2)*l2*scale + math.cos(theta3)*l3*scale])
    #Drawing balls at ends of arms
    pygame.draw.circle(window, (0,0,0), [hinge[0]+math.sin(theta1)*l1*scale, hinge[1]+math.cos(theta1)*l1*scale], 3)
    pygame.draw.circle(window, (0,0,0), [hinge[0]+math.sin(theta1)*l1*scale + math.sin(theta2)*l2*scale, hinge[1]+math.cos(theta1)*l1*scale + math.cos(theta2)*l2*scale], 3)

    return (hinge[0]+math.sin(theta1)*l1*scale, hinge[1]+math.cos(theta1)*l1*scale)

def getTheta1Accel(m1, m2, m3, l1, l2, l3, theta1, theta2, theta3, dtheta1, dtheta2, dtheta3, g):
    theta1Accel = -(m2+m3)*l1*l2*dtheta2**2*math.sin(theta1-theta2)-m3*l1*l3*dtheta3**2*math.sin(theta1-theta3)-(m1+m2+m3)*g*l1*math.sin(theta1)
    return theta1Accel



#not mine
"""def getTheta1Accel(m1, m2, l1, l2, theta1, theta2, dtheta1, dtheta2, g):
    theta1Accel = (m2*l2/((m1+m2)*l1))*math.sin(theta2-theta1)*(dtheta2**2)-g*math.sin(theta1)/l1
    return theta1Accel"""

def getTheta2Accel(m1, m2, m3, l1, l2, l3, theta1, theta2, theta3, dtheta1, dtheta2, dtheta3, g):
    theta2Accel = (m2+m3)*l1*l2*dtheta1**2*math.sin(theta1-theta2)-m3*l2*l3*dtheta3**2*math.sin(theta2-theta3)-(m2+m3)*g*l2*math.sin(theta2)
    return theta2Accel

def getTheta3Accel(m1, m2, m3, l1, l2, l3, theta1, theta2, theta3, dtheta1, dtheta2, dtheta3, g):
    theta3Accel = m3*l1*l3*dtheta1**2*math.sin(theta1-theta3)+m3*l2*l3*dtheta2**2*math.sin(theta2-theta3)-m3*g*l3*math.sin(theta3)
    return theta3Accel

"""def getTheta2Accel(m1, m2, l1, l2, theta1, theta2, dtheta1, dtheta2, g):
    theta2Accel = -(l1*math.sin(theta2-theta1)*(dtheta1**2)) / l2 - g*math.sin(theta2)/l2
    return theta2Accel"""

def main_game(m1, m2, m3, l1, l2, l3, initialTheta1, initialTheta2, initialTheta3, initialDTheta1, initialDTheta2, initialDTheta3):
    

    """angularSpeed = idt
    rSpeed = idr
    theta = it
    r = ir"""

    theta1 = initialTheta1
    theta2 = initialTheta2
    theta3 = initialTheta3
    dTheta1 = initialDTheta1
    dTheta2 = initialDTheta2
    dTheta3 = initialDTheta3

    FPS = 60
    clock = pygame.time.Clock()
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()  
        
        clock.tick(FPS)
        
        try:
            timetick = 1/clock.get_fps()
        except:
            timetick = 0

        dTheta1 = dTheta1 + (timetick)*getTheta1Accel(m1, m2, m3, l1, l2, l3, theta1, theta2, theta3, dTheta1, dTheta2, dTheta3, g)
        dTheta2 = dTheta2 + (timetick)*getTheta2Accel(m1, m2, m3, l1, l2, l3, theta1, theta2, theta3, dTheta1, dTheta2, dTheta3, g)
        dTheta3 = dTheta3 + (timetick)*getTheta3Accel(m1, m2, m3, l1, l2, l3, theta1, theta2, theta3, dTheta1, dTheta2, dTheta3, g)
        theta1 = theta1 + (timetick)*dTheta1
        theta2 = theta2 + (timetick)*dTheta2
        theta3 = theta3 + (timetick)*dTheta3

        window.fill((255,255,255))
        drawPendulums(theta1, theta2, theta3, l1, l2, l3, scale)
        #pygame.draw.circle(window, (255,0,0), [hinge[0]+math.sin(theta1)*l1*scale + math.sin(theta2)*l2*scale, hinge[1]+math.cos(theta1)*l1*scale + math.cos(theta2)*l2*scale], 1)
        pygame.display.update()



while True:
    #main_game(5, 0.5, 1, 1, math.pi/2, math.pi/2, 0, 0)
    main_game(1, 1, 1, 1, 1, 1, math.pi/2, 0, 0, 0, 0, 0)