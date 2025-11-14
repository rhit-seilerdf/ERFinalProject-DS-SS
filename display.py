import matplotlib.pyplot as plt
import numpy as np

sensor1 = np.load("sensor1.npy")
sensor2 = np.load("sensor2.npy")
sensor3 = np.load("sensor3.npy")

duration = 1000
x = np.linspace(0, duration, duration)

plt.plot(x, sensor1)
plt.plot(x, sensor2)
plt.plot(x, sensor3)
plt.legend(["sensor1", "sensor2", "sensor3"])
plt.show()