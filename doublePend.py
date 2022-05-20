from random import getrandbits
import pygame
from pygame.locals import *
import math

var_escape = False
global stretchColor
g = 10
scale = 50

pygame.init()
window = pygame.display.set_mode((600, 600))
window.fill((255, 255, 0))

def clamp(n, smallest, largest):
    return max(smallest, min(n, largest))


def drawPendulums(theta1, theta2, l1, l2, hinge, scale):
    #Drawing arms along with scaling factor
    pygame.draw.line(window, (0,0,0), [hinge[0], hinge[1]], [hinge[0]+math.sin(theta1)*l1*scale, hinge[1]+math.cos(theta1)*l1*scale])
    pygame.draw.line(window, (0,0,0), [hinge[0]+math.sin(theta1)*l1*scale, hinge[1]+math.cos(theta1)*l1*scale], [hinge[0]+math.sin(theta1)*l1*scale + math.sin(theta2)*l2*scale, hinge[1]+math.cos(theta1)*l1*scale + math.cos(theta2)*l2*scale])

    #Drawing balls at ends of arms
    pygame.draw.circle(window, (0,0,0), [hinge[0]+math.sin(theta1)*l1*scale, hinge[1]+math.cos(theta1)*l1*scale], 3)
    pygame.draw.circle(window, (0,0,0), [hinge[0]+math.sin(theta1)*l1*scale + math.sin(theta2)*l2*scale, hinge[1]+math.cos(theta1)*l1*scale + math.cos(theta2)*l2*scale], 3)


def getTheta1Accel(m1, m2, l1, l2, theta1, theta2, dtheta1, dtheta2, g):
    theta1Accel = (-m2*math.cos(theta1-theta2)*l1*(dtheta1**2)*math.sin(theta1-theta2)+m2*math.cos(theta1-theta2)*g*math.sin(theta2)-m2*l2*(dtheta2**2)*math.sin(theta1-theta2)-(m1+m2)*g*math.sin(theta1))/(l1*(m1+m2)-m2*(math.cos(theta1-theta2))**2)
    return theta1Accel

def getTheta2Accel(m1, m2, l1, l2, theta1, theta2, dtheta1, dtheta2, g):
    theta2Accel = ((m1+m2)*(l1*(dtheta1**2)*math.sin(theta1-theta2)+(((dtheta2**2)*math.sin(theta1-theta2)*math.cos(theta1-theta2)*m2*l2)/(m1+m2))+math.cos(theta1-theta2)*g*math.sin(theta1)-g*math.sin(theta2)))    /   (l2*(m1+m2*(math.sin(theta1-theta1))**2))
    return theta2Accel

def main_game(m1, m2, l1, l2, initialTheta1, initialTheta2, initialDTheta1, initialDTheta2):
    

    """angularSpeed = idt
    rSpeed = idr
    theta = it
    r = ir"""

    theta1 = initialTheta1
    theta2 = initialTheta2
    dTheta1 = initialDTheta1
    dTheta2 = initialDTheta2

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

        dTheta1 = dTheta1 + (timetick)*getTheta1Accel(m1, m2, l1, l2, theta1, theta2, dTheta1, dTheta2, g)
        dTheta2 = dTheta2 + (timetick)*getTheta2Accel(m1, m2, l1, l2, theta1, theta2, dTheta1, dTheta2, g)
        theta1 = theta1 + (timetick)*dTheta1
        theta2 = theta2 + (timetick)*dTheta2
        

        window.fill((255,255,255))
        drawPendulums(theta1, theta2, l1, l2, (300,300), scale)
        pygame.display.update()



while True:
    main_game(1, 1, 0.75, 1, math.pi/2, math.pi, 0, -2)