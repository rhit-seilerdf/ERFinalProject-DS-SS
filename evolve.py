import eas
import ctrnn
import pyrosim.pyrosim as pyrosim
import pybullet as p
import pybullet_data
import numpy as np
import time
import generate

# physicsClient = p.connect(p.GUI) 
physicsClient = p.connect(p.DIRECT) # NEW
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.configureDebugVisualizer(p.COV_ENABLE_GUI,0)
p.setGravity(0,0,-9.8)

planeId = p.loadURDF("plane.urdf")
robotId = p.loadURDF("arm.urdf")
boxId = p.loadURDF('box.urdf')
pyrosim.Prepare_To_Simulate(robotId)

transient = 1000
duration = 4000                 

nnsize = 5
sensor_inputs = 4
motor_outputs = 3

dt = 0.01
TimeConstMin = 1.0
TimeConstMax = 2.0
WeightRange = 10.0
BiasRange = 10.0

t = np.linspace(0,1,num=duration)
x = 10
tp1 = np.zeros(duration)
tp2 = np.zeros(duration)

nn = ctrnn.CTRNN(nnsize,sensor_inputs,motor_outputs)

# EA Params
popsize = 10
genesize = nnsize*nnsize + 2*nnsize + sensor_inputs*nnsize + motor_outputs*nnsize 
recombProb = 0.5
mutatProb = 0.01
demeSize = 2
generations = 5

def reset_robot(robotId, base_pos=[0,0,1], base_orn=[0,0,0,1]):
    # Reset base position and orientation
    p.resetBasePositionAndOrientation(robotId, base_pos, base_orn)

    # zero out velocity
    p.resetBaseVelocity(robotId, [0,0,0], [0,0,0])

    # Reset all joint angles and velocities
    num_joints = p.getNumJoints(robotId)
    for j in range(num_joints):
        p.resetJointState(robotId, j, targetValue=0.0, targetVelocity=0.0)

def fitnessFunction(genotype):
    reset_robot(robotId)

    nn = ctrnn.CTRNN(nnsize,sensor_inputs,motor_outputs)
    nn.setParameters(genotype,WeightRange,BiasRange,TimeConstMin,TimeConstMax)
    nn.initializeState(np.zeros(nnsize))

    for i in range(transient):
        nn.step(dt,[0,0,0,0])
        p.stepSimulation()

    output = np.zeros((duration,nnsize))
    motorout = np.zeros((duration,motor_outputs))
    
    sensor1= np.zeros(duration)
    sensor2= np.zeros(duration)
    sensor3= np.zeros(duration)


    linkState = p.getLinkState(robotId,2)
    posx_start = linkState[0][0]
    posy_start = linkState[0][1]

    box_x, box_y, box_z = p.getBasePositionAndOrientation(boxId)[0]

    # Test period
    # Get starting position (after the transient)
    linkState = p.getLinkState(robotId,2)
    posx_start = linkState[0][0]
    posy_start = linkState[0][1]
    posx_current = linkState[0][0]
    posy_current = linkState[0][1]
    posz_current = linkState[0][2]   

    from_box = (((posz_current-box_x)**2) + ((posy_current-box_y)**2))**(1/2)
    distance_traveled = 0.0 # distance traveled in the x-y plane at each step, to be maximized
    distance_jumped = 0.0 # amount of movement up and down, to be minimized

    for i in range(duration):
        sensor1[i] = pyrosim.Get_Angle_Of_Joint(robotId, "1")
        sensor2[i] = pyrosim.Get_Angle_Of_Joint(robotId, "2")
        sensor3[i] = pyrosim.Get_Angle_Of_Joint(robotId, "3")
        for ttt in range(10):
            nn.step(dt,[sensor1[i], sensor2[i], sensor3[i], from_box])
        output[i] = nn.Output
        motorout[i] = nn.out()
        motoroutput = nn.out()
        p.stepSimulation()
        # print(motoroutput)

        # tp1[i] = np.sin(x * t[i]*2*np.pi) * np.pi/4  
        # tp2[i] = np.cos(x * t[i]*2*np.pi) * np.pi/8

        
        pyrosim.Set_Motor_For_Joint(bodyIndex= robotId, 
                                    jointName="1", 
                                    controlMode = p.POSITION_CONTROL,
                                    targetPosition = motoroutput[0],
                                    maxForce = 500
                            )
        pyrosim.Set_Motor_For_Joint(bodyIndex= robotId, 
                                    jointName="2", 
                                    controlMode = p.POSITION_CONTROL,
                                    targetPosition = motoroutput[1],
                                    maxForce = 500
                            )
        pyrosim.Set_Motor_For_Joint(bodyIndex= robotId, 
                                    jointName="3", 
                                    controlMode = p.POSITION_CONTROL,
                                    targetPosition = motoroutput[2],
                                    maxForce = 500
                            )
        
        time.sleep(1/1000) # NEW 
        
        posx_past = posx_current
        posy_past = posy_current
        posz_past = posz_current   
        linkState = p.getLinkState(robotId,2) #hand link
        posx_current = linkState[0][0]
        posy_current = linkState[0][1]
        posz_current = linkState[0][2]    
        distance_traveled += np.sqrt((posx_current - posx_past)**2 + (posy_current - posy_past)**2)
        distance_jumped += np.sqrt((posz_current - posz_past)**2)

        from_box = (((posz_current-box_x)**2) + ((posy_current-box_y)**2) + ((posz_current-box_z)**2))**(1/2)
        

    linkState = p.getLinkState(robotId,2)
    posx_end = linkState[0][0]
    posy_end = linkState[0][1]

    distance_final = np.sqrt((posx_start - posx_end)**2 + (posy_start - posy_end)**2)

    print(from_box)

    return 1/abs(from_box), distance_final + distance_traveled - distance_jumped, output, motorout, sensor1, sensor2, sensor3



# Evolve and visualize fitness over generations
runs = 1
bestByRun = np.zeros([runs, generations])
# for i in range(runs):
# generate.box()
ga = eas.Microbial(fitnessFunction, popsize, genesize, recombProb, mutatProb, demeSize, generations)
ga.run()
# bestByRun[i] = ga.showFitness()
af,bf,bi = ga.fitStats()    
# Save 
np.save("bestgenotype.npy",bi)
# Get best evolved network

p.disconnect() 