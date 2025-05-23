#! /usr/bin/env python3

###
# KINOVA (R) KORTEX (TM)
#
# Copyright (c) 2018 Kinova inc. All rights reserved.
#
# This software may be modified and distributed
# under the terms of the BSD 3-Clause license.
#
# Refer to the LICENSE file for details.
#



#TEST UM WINKEL ZU MESSEN
###

import sys
from sys import exit
import os
import time
from kortex_api.autogen.client_stubs.BaseClientRpc import BaseClient
global test

from kortex_api.autogen.messages import Base_pb2
from kortex_api.Exceptions.KServerException import KServerException


SPEED = 20.0

#
#
# Example core functions
#

def example_forward_kinematics(base):
    # Current arm's joint angles (in home position)
    try:
        print("Getting Angles for every joint...")
        input_joint_angles = base.GetMeasuredJointAngles()
    except KServerException as ex:
        print("Unable to get joint angles")
        print("Error_code:{} , Sub_error_code:{} ".format(ex.get_error_code(), ex.get_error_sub_code()))
        print("Caught expected error: {}".format(ex))
        return False
    test_liste=[]
    print("Joint ID : Joint Angle")
    for joint_angle in input_joint_angles.joint_angles:
        print(joint_angle.joint_identifier, " : ", joint_angle.value)
        test_liste.append((joint_angle.joint_identifier,joint_angle.value))
    print()
    
    #return True
    return test_liste

def example_send_joint_speeds(base):

    joint_speeds = Base_pb2.JointSpeeds()

    actuator_count = base.GetActuatorCount().count
    # The 7DOF robot will spin in the same direction for 10 seconds
    if actuator_count == 7:
        speeds = [SPEED, 0, SPEED, 0, 0, 0, 0]
        
        i = 0
        for speed in speeds:
            joint_speed = joint_speeds.joint_speeds.add()
            joint_speed.joint_identifier = i 
            joint_speed.value = speed
            joint_speed.duration = 0
            i = i + 1
            
        
        print ("Sending the joint speeds for 10 seconds...")
        base.SendJointSpeedsCommand(joint_speeds)
        time.sleep(10)
        
    print ("Stopping the robot")
    base.Stop()

    return True



def example_inverse_kinematics(base):
    # get robot's pose (by using forward kinematics)
    try:
        input_joint_angles = base.GetMeasuredJointAngles()
        pose = base.ComputeForwardKinematics(input_joint_angles)
    except KServerException as ex:
        print("Unable to get current robot pose")
        print("Error_code:{} , Sub_error_code:{} ".format(ex.get_error_code(), ex.get_error_sub_code()))
        print("Caught expected error: {}".format(ex))
        return False

    # Object containing cartesian coordinates and Angle Guess
    input_IkData = Base_pb2.IKData()
    
    # Fill the IKData Object with the cartesian coordinates that need to be converted
    input_IkData.cartesian_pose.x = pose.x
    input_IkData.cartesian_pose.y = pose.y
    input_IkData.cartesian_pose.z = pose.z
    input_IkData.cartesian_pose.theta_x = pose.theta_x
    input_IkData.cartesian_pose.theta_y = pose.theta_y
    input_IkData.cartesian_pose.theta_z = pose.theta_z

    # Fill the IKData Object with the guessed joint angles
    for joint_angle in input_joint_angles.joint_angles :
        jAngle = input_IkData.guess.joint_angles.add()
        # '- 1' to generate an actual "guess" for current joint angles
        jAngle.value = joint_angle.value - 1
    
    try:
        print("Computing Inverse Kinematics using joint angles and pose...")
        computed_joint_angles = base.ComputeInverseKinematics(input_IkData)
    except KServerException as ex:
        print("Unable to compute inverse kinematics")
        print("Error_code:{} , Sub_error_code:{} ".format(ex.get_error_code(), ex.get_error_sub_code()))
        print("Caught expected error: {}".format(ex))
        return False

    print("Joint ID : Joint Angle")
    joint_identifier = 0
    for joint_angle in computed_joint_angles.joint_angles :
        print(joint_identifier, " : ", joint_angle.value)
        joint_identifier += 1

    return True
global test

def main():
    # Import the utilities helper module
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
    import utilities
    global test
    # Parse arguments
    args = utilities.parseConnectionArguments()
    
    # Create connection to the device and get the router
    with utilities.DeviceConnection.createTcpConnection(args) as router:

        # Create required services
        base = BaseClient(router)

        # Example core
        success = True
        for g in range(0,1):
            #success &= example_forward_kinematics(base)
            test=example_forward_kinematics(base)
            
            actuator_count = base.GetActuatorCount().count
            print(actuator_count)
            #
            
            
            
            
            
        
            joint_speeds = Base_pb2.JointSpeeds()

            
            joint_speeds.joint_speeds.add()
            print(joint_speeds)
            #base.SendJointSpeedsCommand(joint_speeds)
            example_send_joint_speeds(base)
            
            
            
            #time.sleep(0.01)
        #success &= example_inverse_kinematics(base)
        
        return 0 if success else 1

if __name__ == "__main__":
    exit(main())
global test

