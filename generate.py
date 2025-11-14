import pyrosim.pyrosim as pyrosim
import random

def World(n, xnum, ynum):
    pyrosim.Start_SDF("box.sdf")
    for x in range(xnum):
        for y in range(ynum):
            for i in range(n):
                s = 1-1/(i+1)
                pyrosim.Send_Cube(name="Box1", pos=[x,y,0.5 + i] , size=[s, s, s])

    pyrosim.End()

def Arm():
   import pyrosim.pyrosim as pyrosim


def Robot():
    h = 0.3
    w = 0.1
    pyrosim.Start_URDF("robot.urdf")

    # Main Body
    pyrosim.Send_Cube(name="0", pos=[0,0,(h + h/6)], size=[h, h, h])

    # Front Leg
    pyrosim.Send_Joint(name="0-1",type="fixed", position=[0,0,0], parent="0", child="1")
    pyrosim.Send_Cube(name="1", pos=[0, h/2 + (w/2), (2*h)/3], size=[w, w, h/2])
    pyrosim.Send_Joint(name="1-2", type="revolute", position=[0,w/2, 0], parent="1", child="2")
    pyrosim.Send_Cube(name="2", pos=[0, h/2, h/6], size=[w, w, h/2])


    # Front Leg
    pyrosim.Send_Joint(name="0-3",type="fixed", position=[0,0,0], parent="0", child="3")
    pyrosim.Send_Cube(name="3", pos=[0, -h/2 - (w/2), (2*h)/3], size=[w, w, h/2])
    pyrosim.Send_Joint(name="3-4", type="revolute", position=[0,-w/2, 0], parent="3", child="4")
    pyrosim.Send_Cube(name="4", pos=[0, -h/2, h/6], size=[w, w, h/2])

    # Front Leg
    pyrosim.Send_Joint(name="0-5",type="fixed", position=[0,0,0], parent="0", child="5")
    pyrosim.Send_Cube(name="5", pos=[-h/2 - (w/2), 0, (2*h)/3], size=[w, w, h/2])
    pyrosim.Send_Joint(name="5-6", type="revolute", position=[-w/2,0, 0], parent="5", child="6")
    pyrosim.Send_Cube(name="6", pos=[-h/2, 0, h/6], size=[w, w, h/2])

    # Front Leg
    pyrosim.Send_Joint(name="0-7",type="fixed", position=[0,0,0], parent="0", child="7")
    pyrosim.Send_Cube(name="7", pos=[h/2 + (w/2), 0, (2*h)/3], size=[w, w, h/2])
    pyrosim.Send_Joint(name="7-8", type="revolute", position=[w/2,0, 0], parent="7", child="8")
    pyrosim.Send_Cube(name="8", pos=[h/2, 0, h/6], size=[w, w, h/2])
  
    pyrosim.End()

def Arm():
    pyrosim.Start_URDF("arm.urdf")

    #Base
    pyrosim.Send_Cube(name="base", pos=[0,0,0.25], size=[1, 1, 0.5], mass = 10)

    # shoulder
    pyrosim.Send_Cube(name="shoulder", pos=[0.6, 2, 0], size=[0.2, 2, 0.2])
    pyrosim.Send_Joint(name="1",type="revolute", position=[0,-1,0], parent="base", child="shoulder", axis=[0, 0, 1], upper = "0")

    
    # forearm
    pyrosim.Send_Cube(name="forearm", pos=[0.6 - 0.2, 0.75 + 2 + 2, 0], size=[0.2, 2, 0.2])
    pyrosim.Send_Joint(name="2",type="revolute", position=[0,-1,0], parent="shoulder", child="forearm", axis=[0, 0, 1], upper = "0")

    # "hand"
    pyrosim.Send_Cube(name="hand", pos=[0.6-0.2-0.2, 0.75 + 2 + 2 + 1, 0], size=[0.2, 0.2, 0.2])
    pyrosim.Send_Joint(name="3",type="revolute", position=[0,-0.1,0], parent="forearm", child="hand")

    pyrosim.End()

def new_arm():
    pyrosim.Start_URDF("arm.urdf")

    #Base
    pyrosim.Send_Cube(name="base", pos=[0,0,0.1], size=[1, 1, 0.5], mass = 100)
    max = 3.14159*3/4
    min = -3.14159*3/4
    # shoulder
    pyrosim.Send_Joint(name="1",type="revolute", position=[0.5, 0 ,0], parent="base", child="shoulder", axis=[0, 0, 1],  upper= max, lower=min)
    pyrosim.Send_Cube(name="shoulder", pos=[0.1, 1, 0], size=[0.2, 2, 0.2])

    
    # forearm
    pyrosim.Send_Joint(name="2",type="revolute", position=[0,2,0], parent="shoulder", child="forearm", axis=[0, 0, 1], upper=max, lower=min)
    pyrosim.Send_Cube(name="forearm", pos=[0.1, 1, 0], size=[0.2, 2, 0.2])

    # "hand"
    pyrosim.Send_Joint(name="3",type="revolute", position=[0,2,0], parent="forearm", child="hand", axis=[0,0,1],  upper=max, lower=min)
    pyrosim.Send_Cube(name="hand", pos=[0.1, 0.1, 0], size=[0.2, 0.2, 0.2])

    pyrosim.End()

def box():
    xpos = (random.random() + 1)
    pyrosim.Start_URDF('box.urdf')
    pyrosim.Send_Cube('cube', [-xpos, xpos, 0.1], [0.2, 0.2, 0.2])
    pyrosim.End()

# new_arm()
box()