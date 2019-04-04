import math
import time
import pygame
import numpy as np

colors = [(255,255,255),(255,0,0),(0,128,0),(0,139,139),(0,255,255),(255,192,203),
          (255,127,80),(0,0,255), (0,0,128), (135,206,235), (95,158,160),
          (224,255,255), (60,179,133), (144,238,144), (75,0,130)]

class planet:
    def __init__(self, xcoord, ycoord, xvel, yvel, mass):
        self.xcoord = xcoord
        self.ycoord = ycoord
        self.xvel = xvel
        self.yvel = yvel
        self.mass = mass

        i = np.random.randint(0, high=len(colors))
        self.color = colors[i]
        print(self.color)

        if self.mass < 3:
            self.radius = 4
        elif self.mass >= 3 and self.mass < 10:
            self.radius = 5
        else:
            self.radius = 6
        

''' next is a function that takes in a list of planet objects and uses
their properties to calculate the net force on each planet. it then uses these
forces to calculate the net acceleration (one list for x and one for y)
on each planet and appends this to a list of accelerations '''

def a(plist):
    ax_list = []
    ay_list = []
    temp_list = plist
    for e in plist:
        # create a new list populated with all objects except the current one

        index = temp_list.index(e)
        del temp_list[index]

        x_accel = 0
        y_accel = 0

        for i in temp_list:
            # here we use newton's law of gravitation to calculate a.
            #  we iterate through
            # each of the OTHER planets and calculate a for each and sum
            # them up. if the planet in question is to the left of the planet
            # we're summing the acceleration for, we change a to negative.

            # note: we skip calculating the net force because
            # F = m1a --> a = F/m1 = ((m1*m2)/(x1-x2)^2) / m1 = m2/((x1-x2)^2).

            a_net =  1000*((i.mass)/(math.sqrt(((e.xcoord - i.xcoord)**2)+(e.ycoord - i.ycoord)**2)))  

            try:
                theta = abs(math.atan((e.ycoord - i.ycoord)/(e.xcoord - i.xcoord)))
            except:
                theta = math.pi / 2
            
            ax = a_net * math.cos(theta)
            ay = a_net * math.sin(theta)
                              
            if e.xcoord - i.xcoord > 0:
                ax = (-1)*ax
            x_accel += ax

            if e.ycoord - i.ycoord > 0:
                ay = (-1)*ay
            y_accel += ay
                
        ax_list.append(x_accel)
        ay_list.append(y_accel)


        # add back to list. this happens at the end of each iteration.
        temp_list.insert(index, e)

    return ax_list, ay_list

''' the next function takes in the found accelerations as a list and one by one
uses kinematics to move the planets over a small time interval assuming constant
acceleration. the time interval must be small as the acceleration is not actually
constant and will introduce some error. '''

def update_coords(plist, ax_list, ay_list):
    # for each planet, first solve vf = vi + at, and then d = (vf + vi)t/2 for
    # both components. then update the final velocity to the initial velocity
    # and add d to the position of the planet. the time interval is something
    # to be adjusted and can be changed using the variable immediately below.
    interval = .0025 # seconds

    for e in plist:
        index = plist.index(e)

        ax = ax_list[index]
        vf = e.xvel + (ax * interval)
        
        d = ((vf + e.xvel) * interval) / 2

        e.xvel = vf
        e.xcoord = e.xcoord + d
        

        ay = ay_list[index]
        vf = e.yvel + (ay * interval)
        d = ((vf + e.yvel) * interval) / 2

        e.yvel = vf
        e.ycoord = e.ycoord + d
        

def collision_detect(plist):
    # checks the distance (magnitude of the distance) between each object in plist
    # destroys them if they are within a set distance of each other, to simulate
    # collisions. as above, the distance can be modifed from following variable.
    collision_dist = 3.5
    planet_list = plist
    
    for e in planet_list:

        
        for i in planet_list:
            # first calculate the magnitude of the distance between the two objects.
            magnitude = math.sqrt(((e.xcoord - i.xcoord)**2) + ((e.ycoord - i.ycoord)**2))

            # first make sure we're not dealing with the same planet as e. if we
            # didn't skip this one, we'd end up destroying every planet on the first
            # pass as it would calculate the distance to be zero. trying to find a
            # more efficient way of handling this at the moment.
            if magnitude > .00001:

                if magnitude < collision_dist:
                    # we remove any planets that are considered 'collided' from
                    # the planet list. to prevent errors, we will break here
                    # and only consider the first planet to meet this condition
                    # to have collided with planet being considered.

                    del planet_list[planet_list.index(e)]
                    del planet_list[planet_list.index(i)]
                    break

    return planet_list
                    
                    



x = planet(300,0,0,150,.5)
y = planet(0,0,0,0,100)
z = planet(50,150,0,300,.2)
c = planet(550,0,0,600,2)
d = planet(10,0,0,300,.7)
e = planet(30,600,200,0,3)
r = planet(-300,-200,-300,20,10)
o = planet(500,200,-100,0,200)
m = planet(200,400,55,100,7)
p = planet(200,-300,234,-30,.5)
w = planet(100,575,0,200,3)
b = planet(1000,0,-400,320,30)
q = planet(275,-275,0,305,.5)
it = planet(-300,300,-100,-100,10)
big = planet(100,-100,-50,-50,200)
otherbig = planet(500,300,-70,20,5000)

l = []
l.append(x)
l.append(y)
l.append(z)
l.append(c)
l.append(d)
l.append(e)
l.append(r)
l.append(o)
l.append(m)
l.append(p)
l.append(w)
l.append(b)
l.append(q)
l.append(it)
l.append(big)
l.append(otherbig)


pygame.init()

display_width = 1280
display_height = 1000

black = (0,0,0)
planet_color = (255,255,255)

# setup the display
screen = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Solar System 2D')

clock = pygame.time.Clock()
crashed = False

''' the next function is the placement function, which places all of the planets in their
correct positions on a pygame.surface object for each frame. that is, it runs once
per loop '''

def place(plist):

    for e in plist:

        xpos = round(e.xcoord + 640)
        ypos = round((-1)* e.ycoord + 500)
        pygame.draw.circle(screen, e.color, (xpos, ypos), e.radius)

while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

    x_acceleration, y_acceleration = a(l)
    update_coords(l, x_acceleration, y_acceleration)
    l = collision_detect(l)

    screen.fill(black)
    place(l)


    pygame.display.update()
    clock.tick(60)



