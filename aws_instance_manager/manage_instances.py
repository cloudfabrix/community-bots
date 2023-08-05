import json
import boto3
import time

##-- This program is meant to be ran on a personal terminal for demo and testing purposes --##


# Configure AWS Access-Key/Secret Access-Key on host computer through AWS CLI

# Configure region below
region = "us-east-2"

ec2 = boto3.resource('ec2', region_name= region)

def managing_instances(command, ec2, instanceID):
    
    # Initialize list of instances #
    if command == "stop":
        instances = ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    elif command == "start":
        instances = ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['stopped']}])
    elif command == "terminate":
        instances = ec2.instances.filter()
    
    # Stop, Start or Terminate specific or all instances #
    for instance in instances:
        id=instance.id
        if instanceID == "All" or id == instanceID:
            if command == "stop":
                ec2.instances.filter(InstanceIds=[id]).stop()
            elif command == "start":
                ec2.instances.filter(InstanceIds=[id]).start()
            elif command == "terminate":
                ec2.instances.filter(InstanceIds=[id]).terminate()

    # Live updates to user through terminal #

    # Formatting 
    print(" ")
    if command == "stop":
        print("Stopping...")
    elif command == "start":
        print("Starting...")
    elif command == "terminate":
        print("Terminating...")
    time.sleep(2)
    print(" ")
    print("#", " ", "State", " ", " ", "Instance ID")
    print(" ")

    # Initialize instance list with all instances
    instances = ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running', "pending", "stopped", "stopping"]}])

    # Updates if All instances must be updated #
    if instanceID == "All":
        boolean = False # To check whether desired state is achieved 
        bool2 = False # To check if there's a change in state

        # Storing all instance states
        states = []
        for instance in instances:
            states.append("TempState")
        
        while(boolean == False and instanceID == "All"):
            count = 1 # Iterator for "states" list to print state
            count2 = 0 # Iterator for "states" list to check for updates
            boolean = True # Assumes desired state is reached
            for instance in instances:
                # Checks if desired state is reached
                state = instance.state['Name']
                if command == "stop" and state != "stopped":
                    boolean = False
                elif command == "start" and state != "running":
                    boolean = False
                elif command == "terminate" and state != "terminated":
                    boolean = False
                
                # Checks for updates in state
                if state != states[count2]:
                    states[count2] = state
                    bool2 = True
                count2 += 1
            
            # Prints new state if there is one
            if bool2:
                for instance in instances:
                    print(count, " ", states[count-1], " ", instance)
                    count += 1
                print(" ")
                bool2 = False


    # Updates if One instance must be updated #
    else:
        #initialize ourInstance to None value
        ourInstance = None

        # Find the instance and store it
        for instance in instances:
            if instance.id == instanceID:
                ourInstance = instance

        # Store the state of the instance
        singleState = ourInstance.state['Name']
        print("1", singleState, " ", ourInstance)
        print(" ")

        # Update when there's a change to the state 
        while(instanceID != "All"):
            # Find the instance and store it
            for instance in instances:
                if instance.id == instanceID:
                    ourInstance = instance

            tempState = ourInstance.state['Name'] # Get current state

            # Print new state if there's a change
            if singleState != tempState:
                print("1", " ", tempState, " ", ourInstance)
                print(" ")
                singleState = tempState
            
            # Break if desired state is achieved 
            if command == "stop" and tempState == "stopped":
                break
            elif command == "start" and tempState == "running":
                break
            elif command == "terminate" and tempState == "terminated":
                break
    
    #Print the final state of the instances #
    if command == "stop":
        print(instanceID + " instance(s) now stopped.")
    elif command == "start":
        print(instanceID + " instance(s) now running.")
    elif command == "terminate":
        print(instanceID + " instance(s) now terminated.")


if __name__ == "__main__":
    while(True):
        command = input("Start, Stop, or Terminate: ")
        if command == "Start":
            instanceID = input("All or InstanceID: ")
            managing_instances("start", ec2, instanceID)
            break
        elif command == "Stop":
            instanceID = input("All or InstanceID: ")
            managing_instances("stop", ec2, instanceID)
            break
        elif command == "Terminate":
            instanceID = input("All or InstanceID: ")
            managing_instances("terminate", ec2, instanceID)
            break
        else:
            print("Invalid Command")