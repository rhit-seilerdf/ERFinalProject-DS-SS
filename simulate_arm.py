import pybullet as p  
import time   
import pyrosim.pyrosim as pyrosim
import numpy as np
import pybullet_data
import ctrnn

physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath(), 0)

p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0)
p.setGravity(0,0, -9.8)

planeId = p.loadURDF("plane.urdf")
robotId = p.loadURDF("arm.urdf")
boxId = p.loadURDF("box.urdf")



pyrosim.Prepare_To_Simulate(robotId)

duration = 1000
t = np.linspace(0,1,num=duration)
x = 10
tp1 = np.zeros(duration)
tp2 = np.zeros(duration)

sensor1= np.zeros(duration)
sensor2= np.zeros(duration)
sensor3= np.zeros(duration)

genotype = np.load("bestgenotype.npy")
nnsize = 5
sensor_inputs = 3
motor_outputs = 3

dt = 0.01
TimeConstMin = 1.0
TimeConstMax = 2.0
WeightRange = 10.0
BiasRange = 10.0

transient = 10


nn = ctrnn.CTRNN(nnsize,sensor_inputs,motor_outputs)
nn.setParameters(genotype,WeightRange,BiasRange,TimeConstMin,TimeConstMax)
nn.initializeState(np.zeros(nnsize))

for i in range(duration):
    for i in range(transient):
        nn.step(dt,[0,0,0])
        p.stepSimulation()
    p.stepSimulation()
    motoroutput = nn.out()
    p.stepSimulation()



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
        
    time.sleep(1/60)

np.save("sensor1.npy", sensor1)
np.save("sensor2.npy", sensor2)
np.save("sensor3.npy", sensor3)
p.stepSimulation()
p.disconnect() 