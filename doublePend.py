import pygame
from pygame.locals import *
import math

var_escape = False

#Setting constants
g = 10
scale = 50
timescale = 1
trailLength = 100
trailDropoff = 0.9

#Creating pygame window
pygame.init()
window = pygame.display.set_mode((600, 600))
window.fill((255, 255, 255))

#Creating double pendulum class with constants and variables
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
        
        #Initial accelerations not arguments to init, but are changed later on
        self.theta1Accel = 0
        self.theta2Accel = 0

        #Set up last n points list for trail
        self.lastNPts = []

    #Function to calculate coordinates of both arms' end points using lagrangian equations
    #These functions rely on small incrementations in steps so are therefore akin to an euler approximation of the motion of the pendulum
    #This can result in net energy gains and losses over time, however observedly tends more to net loss, why idk
    def calculatePts(self, timestep):

        #Finding accelerationso of both thetas using lagrangian equations along with variables form previous timestep
        self.theta1Accel = (-self.m2*math.cos(self.theta1-self.theta2)*self.l1*(self.dTheta1**2)*math.sin(self.theta1-self.theta2)+self.m2*math.cos(self.theta1-self.theta2)*g*math.sin(self.theta2)-self.m2*self.l2*(self.dTheta2**2)*math.sin(self.theta1-self.theta2)-(self.m1+self.m2)*g*math.sin(self.theta1))/(self.l1*(self.m1+self.m2)-self.m2*(math.cos(self.theta1-self.theta2))**2)
        self.theta2Accel = ((self.m1+self.m2)*(self.l1*(self.dTheta1**2)*math.sin(self.theta1-self.theta2)+(((self.dTheta2**2)*math.sin(self.theta1-self.theta2)*math.cos(self.theta1-self.theta2)*self.m2*self.l2)/(self.m1+self.m2))+math.cos(self.theta1-self.theta2)*g*math.sin(self.theta1)-g*math.sin(self.theta2)))    /   (self.l2*(self.m1+self.m2*(math.sin(self.theta1-self.theta2))**2))

        #Multiplying newfound angular accelerations by time difference from last frame and adding it to angular speed from last time step
        self.dTheta1 = self.dTheta1 + self.theta1Accel * timestep
        self.dTheta2 = self.dTheta2 + self.theta2Accel * timestep

        #Multipling those angular speeds by time difference from last frame and adding those new theta differences to thetas from previous
        #frame to get approximate values for current theta
        self.theta1 = self.theta1 + self.dTheta1 * timestep
        self.theta2 = self.theta2 + self.dTheta2 * timestep

        #Calculating locations of both arm points using new thetas and constant lengths along with trigonometric functions
        self.firstPt = [self.origin[0]+math.sin(self.theta1)*self.l1*scale, self.origin[1]+math.cos(self.theta1)*self.l1*scale]
        self.secondPt = [self.firstPt[0] + math.sin(self.theta2)*self.l1*scale, self.firstPt[1] + math.cos(self.theta2)*self.l2*scale]
        
        #Appending coordinates of tip of second arm to list of last n points to use later for trail drawing
        if len(self.lastNPts) < trailLength:

            #Until the amount of points is below the amount wanted for trail length, keep adding points
            self.lastNPts.append(self.secondPt)
        elif len(self.lastNPts) == trailLength:

            #Once amount of points in list equals desired trail length, pop first value in list and append new value   
            #This is to keep the trail a a constant length and so the oldest drawn point is removed every frame
            self.lastNPts.pop(0)
            self.lastNPts.append(self.secondPt)

#Function to draw both arms of double pendulum on screen
def drawPendulums(pendulum):

    #Drawing arms of pendulum
    pygame.draw.line(window, (0,0,0), pendulum.origin, pendulum.firstPt)
    pygame.draw.line(window, (0,0,0), pendulum.firstPt, pendulum.secondPt)

    #Drawing joints of pendulum
    pygame.draw.circle(window, (0,0,0), pendulum.firstPt, 4)
    pygame.draw.circle(window, (0,0,0), pendulum.secondPt, 4)

#Function to draw trail of tip of second arm of double pendulum
def drawTrail(pendulum):
    #index = 0

    #Loop through every value in list of last n points of second arm head
    for i in pendulum.lastNPts:
        """index+=1
        #opacity = 255-255/(len(pendulum.lastNPts)/(pendulum.lastNPts.index(i)+1))
        if index >= round((1-trailDropoff)*len(pendulum.lastNPts)):
            opacity = 1.0
        else:
            opacity = (index/(len(pendulum.lastNPts)*(1-trailDropoff)))"""

        #Not sure why this worked but, I think it means
        #If currently on any point but the last one, draw a line between current point, and next point in list
        #Else, continue and will restart from beginning of list again
        #I think checking if being on last points prevents list index error from being out of range when "pendulum.lastNPts[pendulum.lastNPts.index(i)+1]" is called
        if pendulum.lastNPts.index(i) < len(pendulum.lastNPts)-1:
            #pygame.draw.line(window, (255,255-opacity*255,255-opacity*255), i, pendulum.lastNPts[pendulum.lastNPts.index(i)+1], 2)
            pygame.draw.line(window, (255,0,0), i, pendulum.lastNPts[pendulum.lastNPts.index(i)+1], 2)      
        else:
            continue

#Main game function
def main_game():  
    
    #Instancing a pendulum 
    firstPend = doublePendulum((300,300), 1, 1, 5, 1, math.pi/2, math.pi, 0, 0)

    #Setting desired FPS cap/goal not sure which
    FPS = 60

    #Setting up game clock, also not sure what this does
    clock = pygame.time.Clock()

    #Main game loop
    run = True
    while run:

        #Not sure why this is here but program would not work without it so I put it here
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()  
        
        #Moving game clock forward one tick I think
        clock.tick(FPS)

        #first 5 frames of window always return 0 for clock.get_fps() so I put an exception in the cases in which it would try to
        #divide by 0
        try:
            timetick = 1/clock.get_fps()
        except:
            timetick = 0

        #Debug for checking current game fps
        #print(clock.get_fps())
        
        #Calculate coordinates of tips of both arms of double pendulum
        firstPend.calculatePts(timetick)
        
        #Draw trail of past n points of tip of second arm, including current one
        drawTrail(firstPend)

        #Draw current pendulum state
        drawPendulums(firstPend)
       
        #Update pygame display
        pygame.display.update()

        #Clear screen
        window.fill((255,255,255))

        #Note: important to draw evethign in this order or things get funky, not sure why but I found this through trial and
        #Either one thing was invisible or both were so I just played around with the order of drawing and clearing and updating



main_game()