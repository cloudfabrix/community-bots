import requests
import logging
import boto3
import pandas as pd

# API: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/ec2-example-managing-instances.html
# API to stop instance: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/stop_instances.html#
# API for credentials: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html

logger = logging.getLogger(__name__)

class AwsInstanceManagerBot(object):
    
    def __init__(self, **kwargs):
        # kwargs will contain a reference to config object
        # config object may also contain credentials provided by the user (if any)
        self.__config = kwargs.get("config")
        self.instanceID = config.get('instanceID')
        self.region = config.get('region')
        self.access_key = config.get('access_key')
        self.secret_key = config.get('secret_key')


        self.ec2 = boto3.resource('ec2', aws_access_key_id= self.access_key, aws_secret_access_key= self.secret_key, region_name='region')

        logger.info("Initializing AWS Instance Manager Bot")

    def shutdown(self):
        # Shutdown hook may be called before shutting down the bot code.
        # any cleanup can be performed.
        logger.info("Shutdown hook called")

    # for bot stop, expected method name for implementation is bot_stop
    def bot_stop(self):

        query_params = kwargs.get("query_params", {})

        instances = ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
        for instance in instances:
            id=instance.id
            if (self.instanceID == "All" or id == self.instanceID):
                ec2.instances.filter(InstanceIds=[id]).stop()
        return (instanceID + " instance(s) now stopped.")
    
    # for bot start, expected method name for implementation is bot_start
    def bot_start(self):

        query_params = kwargs.get("query_params", {})

        instances = ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['stopped']}])
        for instance in instances:
            id=instance.id
            if (self.instanceID == "All" or id = self.instanceID):
                ec2.instances.filter(InstanceIds=[id]).start()
        return (instanceID + " instance(s) now running.")
    
    #for bot terminate, expected method name for implementation is bot_terminate
    def bot_terminate(self):

        query_params = kwargs.get("query_params", {})

        instances = ec2.instances.filter()
        for instance in instances:
            id=instance.id
            if (self.instanceID == "All" or id == self.instanceID):
                ec2.instances.filter(InstanceIds=[id]).terminate()
        return (instanceID + " instance(s) now terminated.")