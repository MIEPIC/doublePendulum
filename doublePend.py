import pygame
from pygame.locals import *
import math

var_escape = False
g = 10
scale = 50
timescale = 1
trailLength = 100
trailDropoff = 0.9


pygame.init()
window = pygame.display.set_mode((600, 600))
window.fill((255, 255, 255))

class doublePendulum:



    def __init__(self, origin, l1, l2, m1, m2, initialTheta1, initialTheta2, initialDTheta1, initialDTheta2):
        self.origin = origin
        self.l1 = l1
        self.l2 = l2
        self.m1 = m1
        self.m2 = m2
        self.theta1 = initialTheta1
        self.theta2 = initialTheta2
        self.dTheta1 = initialDTheta1
        self.dTheta2 = initialDTheta2
        self.theta1Accel = 0
        self.theta2Accel = 0
        self.lastNPts = []

    def calculatePts(self, timestep):
        self.theta1Accel = (-self.m2*math.cos(self.theta1-self.theta2)*self.l1*(self.dTheta1**2)*math.sin(self.theta1-self.theta2)+self.m2*math.cos(self.theta1-self.theta2)*g*math.sin(self.theta2)-self.m2*self.l2*(self.dTheta2**2)*math.sin(self.theta1-self.theta2)-(self.m1+self.m2)*g*math.sin(self.theta1))/(self.l1*(self.m1+self.m2)-self.m2*(math.cos(self.theta1-self.theta2))**2)
        self.theta2Accel = ((self.m1+self.m2)*(self.l1*(self.dTheta1**2)*math.sin(self.theta1-self.theta2)+(((self.dTheta2**2)*math.sin(self.theta1-self.theta2)*math.cos(self.theta1-self.theta2)*self.m2*self.l2)/(self.m1+self.m2))+math.cos(self.theta1-self.theta2)*g*math.sin(self.theta1)-g*math.sin(self.theta2)))    /   (self.l2*(self.m1+self.m2*(math.sin(self.theta1-self.theta2))**2))

        self.dTheta1 = self.dTheta1 + self.theta1Accel * timestep
        self.dTheta2 = self.dTheta2 + self.theta2Accel * timestep

        self.theta1 = self.theta1 + self.dTheta1 * timestep
        self.theta2 = self.theta2 + self.dTheta2 * timestep

        self.firstPt = [self.origin[0]+math.sin(self.theta1)*self.l1*scale, self.origin[1]+math.cos(self.theta1)*self.l1*scale]
        self.secondPt = [self.firstPt[0] + math.sin(self.theta2)*self.l1*scale, self.firstPt[1] + math.cos(self.theta2)*self.l2*scale]
        
        if len(self.lastNPts) < trailLength:
            self.lastNPts.append(self.secondPt)
        elif len(self.lastNPts) == trailLength:
            self.lastNPts.pop(0)
            self.lastNPts.append(self.secondPt)


def drawPendulums(pendulum):
    pygame.draw.line(window, (0,0,0), pendulum.origin, pendulum.firstPt)
    pygame.draw.line(window, (0,0,0), pendulum.firstPt, pendulum.secondPt)

    pygame.draw.circle(window, (0,0,0), pendulum.firstPt, 4)
    pygame.draw.circle(window, (0,0,0), pendulum.secondPt, 4)


def drawTrail(pendulum):
    #index = 0

    for i in pendulum.lastNPts:
        """index+=1
        #opacity = 255-255/(len(pendulum.lastNPts)/(pendulum.lastNPts.index(i)+1))
        if index >= round((1-trailDropoff)*len(pendulum.lastNPts)):
            opacity = 1.0
        else:
            opacity = (index/(len(pendulum.lastNPts)*(1-trailDropoff)))"""

        
        if pendulum.lastNPts.index(i) < len(pendulum.lastNPts)-1:
            #pygame.draw.line(window, (255,255-opacity*255,255-opacity*255), i, pendulum.lastNPts[pendulum.lastNPts.index(i)+1], 2)
            pygame.draw.line(window, (255,0,0), i, pendulum.lastNPts[pendulum.lastNPts.index(i)+1], 2)      
        else:
            continue


def main_game():  

    firstPend = doublePendulum((300,300), 1, 1, 5, 1, math.pi/2, math.pi, 0, 0)

    FPS = 62
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

        #print(clock.get_fps())
        
        firstPend.calculatePts(timetick)
        drawTrail(firstPend)
        drawPendulums(firstPend)
       
        pygame.display.update()
        window.fill((255,255,255))



main_game()