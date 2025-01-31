from coppeliasim_zmqremoteapi_client import RemoteAPIClient
import numpy as np
import json
import pickle

def add_target(data, sim):
    # if not isinstance(data, np.ndarray):
    #     raise TypeError("Input must be a numpy array")
    
    sim.setIntProperty(sim.handle_scene, 'signal.my_defIntSignal', data)

client = RemoteAPIClient()
sim = client.require('sim')

sim.setStepping(True)

# Test simple int data
sim.setIntProperty(sim.handle_scene, 'signal.myIntSignal', 7)
add_target(23, sim)

# Test array data
my_array = np.round(np.random.randn(6)*10, 2)
print("my_array: ", my_array)
sim.setFloatArrayProperty(sim.handle_scene, 'signal.my_arraySignal', my_array.tolist())

# Test bool data
my_bool = True
print("my_bool: ", my_bool)
sim.setBoolProperty(sim.handle_scene, 'signal.my_boolSignal', my_bool)

# Test buffer data 
my_buffer = [
    [[1.0, 2.0, 3.0], True],
    [[4.0, 5.0, 6.0], False],
    [[7.0, 8.0, 9.0], True]
]
print("my_buffer: ")
for lst in my_buffer:
    print(lst)
# buffer_str = json.dumps(my_buffer)
buffer_str = pickle.dumps(my_buffer)
sim.setBufferProperty(sim.handle_scene, 'signal.my_bufferSignal', buffer_str)

sim.startSimulation()
while (t := sim.getSimulationTime()) < 40:
    # print(f'Simulation time: {t:.2f} [s]')
    sim.step()

sim.stopSimulation()


