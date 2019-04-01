import math
import time

class planet:
    def __init__(self, xcoord, ycoord, xvel, yvel, mass):
        self.xcoord = xcoord
        self.ycoord = ycoord
        self.xvel = xvel
        self.yvel = yvel
        self.mass = mass

''' next is a function that takes in a list of planet objects and uses
their properties to calculate the net force on each planet. it then uses these
forces to calculate the net acceleration (one list for x and one for y)
on each planet and appends this to a list of accelerations '''

def calculate_a(plist):
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
            # here we use newton's law of gravitation to calculate a in
            # the x direction (same process for y direction). we iterate through
            # each of the OTHER planets and calculate a for each and sum
            # them up. if the planet in question is to the left of the planet
            # we're summing the acceleration for, we change a to negative.

            # note: we skip calculating the net force because
            # F = m1a --> a = F/m1 = ((m1*m2)/(x1-x2)^2) / m1 = m2/((x1-x2)^2).
            try:
                ax = 10000*((i.mass)/((e.xcoord - i.xcoord)**2))
            except:
                ax = 0
                
            if e.xcoord - i.xcoord > 0:
                ax = (-1)*ax
            x_accel += ax

            try:
                ay = 10000*((i.mass)/((e.ycoord - i.ycoord)**2))
            except:
                ay = 0

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
    interval = .01 # seconds

    for e in plist:
        index = plist.index(e)

        ax = ax_list[index]
        #print('1 x acceleration:' + str(ax))
        vf = e.xvel + (ax * interval)
        #print('1 x vel:' + str(vf))
        d = ((vf + e.xvel) * interval) / 2
        #print('1 distance traveled' + str(d))

        e.xvel = vf
        #print('updated x vel' + str(e.xvel))
        e.xcoord = e.xcoord + d
        print('new x coord: ' + str(e.xcoord))

        ay = ay_list[index]
        vf = e.yvel + (ay * interval)
        d = ((vf + e.yvel) * interval) / 2

        e.yvel = vf
        e.ycoord = e.ycoord + d
        print('new y coord: ' + str(e.ycoord))

def collision_detect(plist):
    # checks the distance (magnitude of the distance) between each object in plist
    # destroys them if they are within a set distance of each other, to simulate
    # collisions. as above, the distance can be modifed from following variable.
    collision_dist = 1
    planet_list = plist
    
    for e in planet_list:

        
        for i in planet_list:
            # first calculate the magnitude of the distance between the two objects.
            magnitude = math.sqrt(((e.xcoord - i.xcoord)**2) + ((e.ycoord - i.ycoord)**2))
            print(magnitude)

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
                    
                    

x = planet(1,0,0,.1,.005)
y = planet(-1,0,0,-.1,.005)
z = planet(-4,100,3,4,5)

l = []
l.append(x)
l.append(y)
# l.append(z)

r = 0

while r == 0:
    g = x.xcoord - y.xcoord
    x_acceleration, y_acceleration = calculate_a(l)
    update_coords(l, x_acceleration, y_acceleration)
    #l = collision_detect(l)
    
    #print(x.xcoord)
    #print(y.xcoord)
   # print(y.xvel)
    print(' ')

    time.sleep(.1)


