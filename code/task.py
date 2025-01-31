from coppeliasim_zmqremoteapi_client import RemoteAPIClient
import pickle

def set_task(task, sim):
    # Check
    if not isinstance(task, dict):
        raise TypeError("Expected dictionary for the tasks, but got ", type(task))
    for key, value in task.items():
        if not isinstance(value, list):
            raise TypeError(f"[task: {key}] Expected list for the single task, but got {type(value)}")
        for idx, item in enumerate(value):
            if not isinstance(item[0], list):
                raise TypeError(f"[subtask {idx}] The robot's joints values (subtask {idx}) must be put into a list, but got {type(item[0])}")
            if len(item[0]) != 6:
                raise ValueError(f"[subtask {idx}] Expected 6 joint values, but got {len(item[0])}")
            if not isinstance(item[1], bool):
                raise TypeError("The command for the gripper to open/close must be a boolean (True to open, False to close)")
    
    # Send signals to simulation
    task_buffer = pickle.dumps(task)
    sim.setBufferProperty(sim.handle_scene, 'signal.task', task_buffer)



# Below is the task code block. Put there your code to make the robot help the surgeon during the procedure.
#
# REQUIREMENTS:
# - The targets for the robot to reach must be lists, while the gripper commands must be of boolean type.
# Usage (e.g. using gripper_command as variable):
#       gripper_command = True --> command to open the gripper
#       gripper_command = False --> command to close the gripper
#
# - Targets for the robot to reach and gripper commands have to be organized in a nested list fashion. For each subtask (target + gripper command), 
#   put first the target for the robot and then the gripper command
# Example: 
#       YOUR_TASK = [[YOUR_TARGET1, gripper_command1], [YOUR_TARGET1, gripper_command2], ...]
#
# - The task sequence must be a dictionary (YOUR_DICT = {"KEY_NAME1": YOUR_TASK1, "KEY_NAME2": YOUR_TASK2, ...})
#
# - The last thing you should do before running the simulation is to set the number of tasks that should be executed and assign your taskS to "tasks"
#   to the variable "tasks"
# Usage:
#       #num_tasks = NUMBER_OF_TASKS
#       tasks = YOUR_DICT
#
# Have fun coding, fellas! :D

# -------- TEST --------
task = "fake task"






# YOUR_TASKS = single_task
# -------- TEST --------

# ! ------------------------------------ Task code start ------------------------------------ ! #

#single_task = {"single_task": [[[1.65,-0.4,-1.61,0.95,1.5,1.5], False]]}



# ! ------------------------------------ Task code end ------------------------------------ ! #

# UPDATE TASK NUMBER AND ASSIGN TASK
tasks = task


if __name__ == '__main__':
    client = RemoteAPIClient()
    sim = client.require('sim')
    set_task(tasks, sim)

    sim.setStepping(True)
    sim.startSimulation()
    print("Simulation started.")

    while (task_over := sim.getBoolProperty(sim.handle_scene, "signal.tasks_over")) != True:
        sim.step()

    sim.stopSimulation()
    print("Simulation stopped.")

