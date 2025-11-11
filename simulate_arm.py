import pybullet as p  
import time   
import pyrosim.pyrosim as pyrosim
import numpy as np
import pybullet_data

physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath(), 0)

p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0)
p.setGravity(0,0, -9.8)

planeId = p.loadURDF("plane.urdf")
robotId = p.loadURDF("arm.urdf")


pyrosim.Prepare_To_Simulate(robotId)

duration = 1000
t = np.linspace(0,1,num=duration)
x = 10
tp1 = np.zeros(duration)
tp2 = np.zeros(duration)

for i in range(duration):
    p.stepSimulation()
    if (i > 10):
        tp1[i] = np.sin(x * t[i]*2*np.pi) * np.pi/4  
        tp2[i] = np.cos(x * t[i]*2*np.pi) * np.pi/8

        pyrosim.Set_Motor_For_Joint(bodyIndex= robotId, 
                                    jointName="1", 
                                    controlMode = p.POSITION_CONTROL,
                                    targetPosition = tp1[i],
                                    maxForce = 500
                            )
        pyrosim.Set_Motor_For_Joint(bodyIndex= robotId, 
                                    jointName="2", 
                                    controlMode = p.POSITION_CONTROL,
                                    targetPosition = tp1[i],
                                    maxForce = 500
                            )
        pyrosim.Set_Motor_For_Joint(bodyIndex= robotId, 
                                    jointName="3", 
                                    controlMode = p.POSITION_CONTROL,
                                    targetPosition = tp1[i],
                                    maxForce = 500
                            )
    time.sleep(1/60)
p.stepSimulation()
p.disconnect() 