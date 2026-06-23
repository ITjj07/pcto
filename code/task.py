"""Send a task dictionary to CoppeliaSim 4.10 via the ZeroMQ remote API.

Run this script while CoppeliaSim is open with the matching scene loaded and the
Python code from ``script.txt`` pasted into a scene/script object.  CoppeliaSim
4.10 no longer supports relying on the old legacy remote API; the supported
Python client is ``coppeliasim-zmqremoteapi-client``.
"""

from __future__ import annotations

import pickle
import time
from numbers import Real
from typing import Any

from coppeliasim_zmqremoteapi_client import RemoteAPIClient

TASK_SIGNAL = "signal.task"
TASKS_OVER_SIGNAL = "signal.tasks_over"


def _validate_task(task: dict[str, list[list[Any]]]) -> None:
    """Validate the task payload before it is sent to the simulator."""
    if not isinstance(task, dict):
        raise TypeError(f"Expected task to be a dictionary, got {type(task).__name__}")

    for key, value in task.items():
        if not isinstance(key, str):
            raise TypeError(f"Expected task names to be strings, got {type(key).__name__}")
        if not isinstance(value, list):
            raise TypeError(f"[task: {key}] Expected a list, got {type(value).__name__}")

        for idx, item in enumerate(value):
            if not isinstance(item, (list, tuple)) or len(item) != 2:
                raise TypeError(
                    f"[task: {key}, subtask: {idx}] Expected [joint_values, gripper_open]"
                )

            joints, gripper_open = item
            if not isinstance(joints, list):
                raise TypeError(
                    f"[task: {key}, subtask: {idx}] Joint values must be a list, "
                    f"got {type(joints).__name__}"
                )
            if len(joints) != 6:
                raise ValueError(
                    f"[task: {key}, subtask: {idx}] Expected 6 joint values, got {len(joints)}"
                )
            if not all(isinstance(joint, Real) and not isinstance(joint, bool) for joint in joints):
                raise TypeError(
                    f"[task: {key}, subtask: {idx}] Joint values must be int/float radians"
                )
            if not isinstance(gripper_open, bool):
                raise TypeError(
                    f"[task: {key}, subtask: {idx}] Gripper command must be a bool "
                    "(True=open, False=close)"
                )


def set_task(task: dict[str, list[list[Any]]], sim: Any) -> None:
    """Serialize and publish the task with the CoppeliaSim 4.10 property API."""
    _validate_task(task)
    sim.setBufferProperty(sim.handle_scene, TASK_SIGNAL, pickle.dumps(task))
    sim.setBoolProperty(sim.handle_scene, TASKS_OVER_SIGNAL, False)


# Below is the task code block. Put your code here to make the robot help the
# surgeon during the procedure.
#
# REQUIREMENTS:
# - The targets for the robot to reach must be lists, while the gripper commands
#   must be booleans.
#       gripper_command = True   # open gripper
#       gripper_command = False  # close gripper
#
# - Targets and gripper commands have to be organized in a nested-list fashion.
#   For each subtask, put first the target and then the gripper command.
#
# - The robot target must be given in radians. The robot has 6 joints, so each
#   target must contain 6 numeric values.
#       YOUR_TARGET = [joint1, joint2, joint3, joint4, joint5, joint6]
#       YOUR_TASK = [[YOUR_TARGET1, gripper_command1], [YOUR_TARGET2, gripper_command2]]
#
# - The task sequence must be a dictionary:
#       YOUR_DICT = {"KEY_NAME1": YOUR_TASK1, "KEY_NAME2": YOUR_TASK2}
#
# - The last thing you should do before running the simulation is assign your
#   command dictionary to a variable called "tasks".

# ! ------------------------------------ Task code start ------------------------------------ ! #

# WRITE YOUR CODE HERE
# Example placeholder: replace this with your real task dictionary.
tasks = {
    "example": [
        [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0], True],
    ]
}

# ! ------------------------------------ Task code end ------------------------------------ ! #


def main() -> None:
    client = RemoteAPIClient()
    sim = client.require("sim")

    set_task(tasks, sim)

    sim.setStepping(True)
    sim.startSimulation()
    print("Simulation started.")

    try:
        while not sim.getBoolProperty(sim.handle_scene, TASKS_OVER_SIGNAL):
            sim.step()
            time.sleep(0.001)
    finally:
        sim.stopSimulation()
        print("Simulation stopped.")


if __name__ == "__main__":
    main()
