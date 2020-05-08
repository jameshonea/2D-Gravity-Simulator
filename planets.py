import math
import time
import pygame
import numpy as np
import random


class planet:
    def __init__(self, xcoord, ycoord, xvel, yvel, mass):
        self.xcoord = xcoord
        self.ycoord = ycoord
        self.xvel = xvel
        self.yvel = yvel
        self.mass = mass

        self.color = (np.random.randint(0,255),np.random.randint(0,255),np.random.randint(0,255))

        if self.mass < .1:
            self.radius = 3
        elif self.mass >= .1 and self.mass < 3:
            self.radius = 4
        elif self.mass >= 1 and self.mass < 6:
            self.radius = 5
        elif self.mass >= 6 and self.mass < 20:
            self.radius = 6
        else:
            self.radius = 7
        

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
                if e.ycoord - i.ycoord > 0:
                    theta = math.pi / 2
                else:
                    theta = (3/2) * math.pi
            
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

''' the next function is a separate coordinate updating function that will
update coords in such a way that the object with the largest mass will be placed
in the center of the screen. an option exists to toggle between the two functions.
this is to prevent a solar system from drifting off screen'
'''

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

def collision_merge(plist):
    collision_dist = 5
    planet_list  = plist

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
                    # use conservation of momentum to calculate new x and y velocities.
                    # pi = pf --> m1v1 + m2v2 = (m1+m2)vf

                    x_vel_final = ((e.mass * e.xvel) + (i.mass * i.xvel))/(e.mass + i.mass)
                    y_vel_final = ((e.mass * e.yvel) + (i.mass * i.yvel))/(e.mass + i.mass)
                    

                    planet_list.append(planet(e.xcoord, e.ycoord, x_vel_final, y_vel_final, e.mass + i.mass))
                    del planet_list[planet_list.index(e)]
                    del planet_list[planet_list.index(i)]
                    break

    return planet_list
                    
''' below is code for random generation of planets. plan is for this to become sophisticated enough to only generate
planets with masses below a large central object, as well as allow for completely random generation of objects
'''

star = planet(0,0,0,0,500)
l = [] # initialize list of planet objects
l.append(star)

n = 1000 # number of planets to generate

for _ in range(n):
    temp_xcoord = random.uniform(.1,750)
    temp_ycoord = .1 #random.randint(-750,750)
    temp_xvel = .1 #random.randint(100,500)
    temp_yvel = random.uniform(700,1000)
    temp_mass = random.uniform(0.1,1)

    temp_planet = planet(temp_xcoord, temp_ycoord, temp_xvel, temp_yvel, temp_mass)
    l.append(temp_planet)

'''

x = planet(12,0,0,500,.1)
y = planet(0,0,0,0,200)
z = planet(-50,0,0,-350,.25)
c = planet(350,0,0,350,1)
d = planet(-400,0,0,-150,100)
e = planet(0,250,-200,30,10)
f = planet(0,-250,200,0,2)



l = []
l.append(y)
l.append(x)
l.append(z)
l.append(d)

l.append(c)
l.append(e)
l.append(f)
'''


fixed_planet = 1 # set to 1 to fix the center to the most massive planet


pygame.init()

display_width = 1280
display_height = 1000

black = (0,0,0)

# setup the display
screen = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Solar System 2D')

clock = pygame.time.Clock()
crashed = False

def place_fixed(plist):

    mass_index = 0
    largest_mass = 0

    for planet in plist:
        if planet.mass > largest_mass:
            largest_mass = planet.mass
            mass_index = plist.index(planet)

    x_pos_zero = plist[mass_index].xcoord
    y_pos_zero = plist[mass_index].ycoord
    
    for e in plist:
        xpos = round(e.xcoord - x_pos_zero + 640)
        ypos = round((-1)*(e.ycoord - y_pos_zero) + 500)
        pygame.draw.circle(screen, e.color, (xpos, ypos), e.radius)

''' below conditional block is the game loop to run if fixed_planet = 1 i.e. if we want
to fix to the planet with the largest mass. this will recaculate to the largest planet
each pass-through, so if a new planet suddenly becomes largest it will fix on that planet.
'''

if fixed_planet == 1:
    while not crashed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True

        x_acceleration, y_acceleration = a(l)
        update_coords(l, x_acceleration, y_acceleration)
        l = collision_merge(l)

        screen.fill(black)
        place_fixed(l)


        pygame.display.update()
        clock.tick(60)

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
    l = collision_merge(l)

    screen.fill(black)
    place(l)


    pygame.display.update()
    clock.tick(60)



