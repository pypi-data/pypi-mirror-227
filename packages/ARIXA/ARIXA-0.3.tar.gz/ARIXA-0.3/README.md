ARIXA Library
Overview
The ARIXA library provides a Python interface for controlling a robotic arm. It offers various functionalities such as initializing the arm, moving it in joint space or Cartesian coordinates, recording actions, and more.

Installation
To install the ARIXA library, run the following command:


pip install ARIXA

Setting API Key
Before using the library, you must set the API key. You can do this using the set_api_key function.

import ARIXA

ARIXA.set_api_key("your-api-key-here")

Usage
Initializing the Robotic Arm
To initialize the robotic arm, use the init function.

response = ARIXA.init()


Moving in Joint Space
To move the robotic arm in joint space, use the move_joint_space function.

response = ARIXA.move_joint_space(j1=0, j2=0, j3=0, j4=0, j5=0, j6=0, speed=100, acc=100)


Moving in Cartesian Coordinates
To move the robotic arm in Cartesian coordinates, use the move_cartesian function.

response = ARIXA.move_cartesian(x=0, y=0, z=0, rx=0, ry=0, rz=0, speed=100, acc=100)


Getting Status
To get the status of the robotic arm, use the get_status function.

status = ARIXA.get_status()


Emergency Stop
To activate the emergency stop, use the emergency_stop function.

response = ARIXA.emergency_stop()


Shutdown
To shut down the robotic arm, use the shutdown function.

response = ARIXA.shutdown()


Recording Actions
Joint Space
To start recording actions in joint space, use the start_recording_joint_space function.

response = ARIXA.start_recording_joint_space()

To stop recording and save the actions to a file, use the stop_recording_joint_space function.

response = ARIXA.stop_recording_joint_space("filename")

Cartesian Space
To start recording actions in Cartesian space, use the start_recording_cartesian function.

response = ARIXA.start_recording_cartesian()

To stop recording and save the actions to a file, use the stop_recording_cartesian function.

response = ARIXA.stop_recording_cartesian("filename")


Working with Files
To save actions to a file or retrieve them, you can use the following functions:

save_action_joint_space
save_action_cartesian
get_saved_action_joint_space
get_saved_action_cartesian
Example:

# Save action in joint space
ARIXA.save_action_joint_space("filename", action_data)

# Retrieve saved action in joint space
saved_action = ARIXA.get_saved_action_joint_space("filename")
License
This project is licensed under the MIT License. See the LICENSE file for details.