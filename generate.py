import pyrosim.pyrosim as pyrosim

def World(n,xnum,ynum):
    pyrosim.Start_SDF("boxes.sdf")
    for x in range(xnum):
        for y in range(ynum):
            for i in range(n):
                s = 1 - i/n
                pyrosim.Send_Cube(name="Box", pos=[x,y,0.5 + i] , size=[s,s,s])
    pyrosim.End()

def Robot():
    pyrosim.Start_URDF("robot.urdf")

    h = 0.3
    w = 0.1

    # Main Body
    pyrosim.Send_Cube(name="0", pos=[0,0,(h + h/6)], size=[h, h, h])

    # Right Leg
    pyrosim.Send_Joint(name="0_1",type="revolute", position=[0,0,0], parent="0", child="1")
    pyrosim.Send_Cube(name="1", pos=[0, h/2 + (w/2), (2*h)/3], size=[w, w, h/2])   
    pyrosim.Send_Joint(name="1_2", type="revolute", position=[0,w/2, 0], parent="1", child="2")
    pyrosim.Send_Cube(name="2", pos=[0, h/2, h/6], size=[w, w, h/2])


    # Left Leg
    pyrosim.Send_Joint(name="0_3",type="revolute", position=[0,0,0], parent="0", child="3")
    pyrosim.Send_Cube(name="3", pos=[0, -h/2 - (w/2), (2*h)/3], size=[w, w, h/2])
    pyrosim.Send_Joint(name="3_4", type="revolute", position=[0,-w/2, 0], parent="3", child="4")
    pyrosim.Send_Cube(name="4", pos=[0, -h/2, h/6], size=[w, w, h/2])

    # Front Leg
    pyrosim.Send_Joint(name="0_5",type="fixed", position=[0,0,0], parent="0", child="5")
    pyrosim.Send_Cube(name="5", pos=[-h/2 - (w/2), 0, (2*h)/3], size=[w, w, h/2])
    pyrosim.Send_Joint(name="5_6", type="revolute", position=[-w/2,0, 0], parent="5", child="6")
    pyrosim.Send_Cube(name="6", pos=[-h/2, 0, h/6], size=[w, w, h/2])

    # Front Leg
    pyrosim.Send_Joint(name="0_7",type="fixed", position=[0,0,0], parent="0", child="7")
    pyrosim.Send_Cube(name="7", pos=[h/2 + (w/2), 0, (2*h)/3], size=[w, w, h/2])
    pyrosim.Send_Joint(name="7_8", type="revolute", position=[w/2,0, 0], parent="7", child="8")
    pyrosim.Send_Cube(name="8", pos=[h/2, 0, h/6], size=[w, w, h/2])

    # pyrosim.Send_Cube(name="0", pos=[0,0,0.5] , size=[1,1,1]) ## Cannot 
    # pyrosim.Send_Joint(name="0_1", parent="0", child="1", type = "revolute", position=[0.5,0,1])
    # pyrosim.Send_Cube(name="1", pos=[0.5,0,0.5] , size=[1,1,1])
    # pyrosim.Send_Joint(name="1_2", parent="1", child="2", type = "revolute", position=[1,0,0])
    # pyrosim.Send_Cube(name="2", pos=[0.5,0,-0.5] , size=[1,1,1])
    pyrosim.End()

Robot()

#World(10,5,5)
