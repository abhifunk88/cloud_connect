import boto3
import re
import os
import sys
import paramiko


class CloudMgmt:

    def __init__(self, env):
        self.env = env
        if self.env == 'prod':
            self.botoClient = boto3.client('ec2')
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())


    def launch_vm(self):
        config_items = self.read_config_file("ec2_config.txt")
        imageId = config_items[0]
        instanceType = config_items[1]
        minCount = config_items[2]
        maxCount = config_items[3]
        keyName = config_items[4]
        if self.env == 'prod':
            response=self.botoClient.run_instances(
                ImageId=imageId, InstanceType=instanceType, MinCount=minCount, MaxCount=maxCount, KeyName=keyName)
            for i in response['Instances']:
                print("Instance ID Created is :{} Instance Type Created is : {}" .format(i['InstanceId'],i['InstanceType']))
        elif self.env == 'stub':
            print("The required instances are up and running!!")


    def stop_vm(self, instanceIds):
        if self.env == 'prod':
            response =self.botoClient.stop_instances(
                InstanceIds=instanceIds,
                Hibernate=True,
                DryRun=False,
                Force=False
            )
            for i in response['Instances']:
                print("Stopped Instance ID is :{}" .format(i['InstanceId']))
        elif self.env == 'stub':
            for i in instanceIds:
                print("Instance with ID - {} is stopped!!".format(i))


    def terminate_vm(self, instanceIds):
        if self.env == 'prod':
            response = self.botoClient.terminate_instances(InstanceIds=instanceIds)
            for i in response['Instances']:
                print("Terminated Instance ID is :{}" .format(i['InstanceId']))
        elif self.env == 'stub':
            for i in instanceIds:
                print("Instance with ID - {} is terminated!!".format(i))


    def start_vm(self, instanceIds):
        if self.env == 'prod':
            response =self.botoClient.start_instances(
                InstanceIds=instanceIds,
                DryRun=False
            )
            for i in response['Instances']:
                print("Started Instance ID is :{}" .format(i['InstanceId']))
        elif self.env == 'stub':
            for i in instanceIds:
                print("Instance with ID - {} is started!!".format(i))


    def list_vm(self):
        if self.env == 'prod':
            response =self.botoClient.describe_instances()
            for reservation in response['Reservations']:
                for instance in reservation['Instances']:
                    print("Running Instance Image ID: {} Running instance Instance Type: {} Running Instance Keyname {}"
                        .format(instance['InstanceId'],instance['InstanceType'],instance['KeyName']))
        elif self.env == 'stub':
            print("Running instances are X, Y and Z")

    
    def connect_vm(self, ip_address):
        if self.env == 'prod':
            privateKey = paramiko.RSAKey.from_private_key_file('./config/mykey.pem')
            try:
                print('SSH into the instance: {}'.format(ip_address))
                self.ssh.connect(hostname=ip_address,
                        username='ubuntu', pkey=privateKey)
                return True
            except Exception as e:
                print(e)
        elif self.env == 'stub':
            print("Successfully connected to IP - {}".format(ip_address))


    def read_config_file(self, filename):
        config_file = open(os.path.join(sys.path[0], filename), "r")
        config_text = config_file.read()
        config_file.close()
        imageId = re.findall(r'ImageId=(\w.+)', config_text)
        instanceType = re.findall(r'InstanceType=(\w.+)', config_text)
        minCount = re.findall(r'MinCount=(\w.+)', config_text)
        maxCount = re.findall(r'MaxCount=(\w.+)', config_text)
        keyName = re.findall(r'KeyName=(\w.+)', config_text)
        return imageId, instanceType, minCount, maxCount, keyName


    def launch_db(self, ip_address):
        if self.env == 'prod':
            self.connect_vm(ip_address)
            commands = "sudo apt install mariadb-server"
            stdin, stdout, stderr = self.ssh.exec_command(commands)
            print('stdout:', stdin.read())
            print('stdout:', stdout.read())
            print('stderr:', stderr.read())
        elif self.env == 'stub':
            print("Successfully Launched Maria DB")
