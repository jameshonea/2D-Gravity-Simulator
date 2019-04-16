import math
import time
import pygame
import numpy as np


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
                    



x = planet(12,0,0,500,.1)
y = planet(0,0,0,0,200)
z = planet(-50,0,0,-350,.25)
c = planet(350,0,0,350,1)
d = planet(-450,0,0,-350,.002)
e = planet(-150,0,0,-400,1.2)
r = planet(0,100,-550,0,.5)
o = planet(0,300,-650,0,3)
m = planet(0,-400,650,0,.3)
p = planet(250,0,0,350,.5)
w = planet(500,0,0,300,.05)
b = planet(1000,0,100,470,.3)
q = planet(300,0,0,450,5)
it = planet(-400,0,0,-650,0.001)
bg = planet(-100,55,75,-30,.005)
qw = planet(350,350,-300,300,.25)
we = planet(-200,-200,-150,-400,.05)
otherbig = planet(300,450,-120,50,3)
er = planet(-300,400,430,-280,.5)
rt = planet(405,303,383,29,.01)
tt = planet(304,100,88,200,.001)
ty = planet(20,300,-880,202,.005)
yu = planet(300,400,-100,-75,5)
ui = planet(-222,0,0,-300,2)
op = planet(504,0,0,350,.5)
pa = planet(0,504,-350,0,.25)
ad = planet(0,-504,376,0,.75)
df = planet(0,525,-500,0,2)
fg = planet(0,550,-460,0,1.2)
gg = planet(0,575,-430,0,.4)
gh = planet(0,602,-400,0,.2)
hj = planet(0,616,-390,0,.09)
kl = planet(525,0,0,500,2)
lk = planet(550,0,0,460,1.2)
zx = planet(575,0,0,430,.4)
zz = planet(602,0,0,400,.2)
zv = planet(616,0,0,390,.09)
jj = planet(0,416,-420,0,.09)
ku = planet(376,0,0,525,2)
mn = planet(389,0,0,502,1.2)
mm = planet(402,0,0,476,.4)
nm = planet(414,0,0,469,.2)
nn = planet(426,0,0,430,.09)
xx = planet(15,0,0,600,.15)
x1 = planet(-376,0,0,-525,2)
x2 = planet(-389,0,0,-502,1.2)
x3 = planet(-402,0,0,-476,.4)
x4 = planet(-414,0,0,-469,.2)
x5 = planet(-426,0,0,-430,.09)
x6 = planet(-15,0,0,-600,.15)
y1 = planet(-176,0,0,-525,2)
y2 = planet(-189,0,0,-502,1.2)
y3 = planet(-102,0,0,-476,.4)
y4 = planet(-114,0,0,-469,.2)
y5 = planet(-126,0,0,-430,.09)
y6 = planet(-135,0,0,-600,.15)
z1 = planet(0,-176,525,0,2)
z2 = planet(0,-189,502,0,1.2)
z3 = planet(0,-102,476,0,.4)
z4 = planet(0,-114,469,0,.2)
z5 = planet(0,-126,430,0,.09)
z6 = planet(0,-130,600,0,.15)


l = []
l.append(y)
l.append(x)
l.append(z)
'''
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

l.append(bg)
l.append(otherbig)
l.append(qw)
l.append(we)
l.append(er)
l.append(rt)
l.append(tt)
l.append(ty)
l.append(yu)
l.append(ui)
l.append(op)
l.append(pa)
l.append(ad)
l.append(df)
l.append(fg)
l.append(gg)
l.append(gh)
l.append(hj)
l.append(zv)
l.append(zz)
l.append(zx)
l.append(lk)
l.append(kl)
l.append(nn)
l.append(nm)
l.append(mm)
l.append(mn)
l.append(ku)
l.append(jj)
l.append(xx)
l.append(x1)
l.append(x2)
l.append(x3)
l.append(x4)
l.append(x5)
l.append(x6)
l.append(y1)
l.append(y2)
l.append(y3)
l.append(y4)
l.append(y5)
l.append(y6)
l.append(z1)
l.append(z2)
l.append(z3)
l.append(z4)
l.append(z5)
l.append(z6)
'''

fixed_planet = 1 # set to 1 to fix the center to the most massive planet

''' below conditional block is the game loop to run if fixed_planet = 1 i.e. if we want
to fix to the planet with the largest mass. this will recaculate to the largest planet
each pass-through, so if a new planet suddenly becomes largest it will fix on that planet.
'''

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



