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

sensor1= np.zeros(duration)
sensor2= np.zeros(duration)
sensor3= np.zeros(duration)

for i in range(duration):
    p.stepSimulation()
    if (i > 10):
        tp1[i] = np.sin(x * t[i]*2*np.pi) * np.pi/4  
        tp2[i] = np.cos(x * t[i]*2*np.pi) * np.pi/8
        sensor1[i] = pyrosim.Get_Angle_Of_Joint(robotId, "1")
        sensor2[i] = pyrosim.Get_Angle_Of_Joint(robotId, "2")
        sensor3[i] = pyrosim.Get_Angle_Of_Joint(robotId, "3")



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

np.save("sensor1.npy", sensor1)
np.save("sensor2.npy", sensor2)
np.save("sensor3.npy", sensor3)
p.stepSimulation()
p.disconnect() 