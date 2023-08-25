#!/usr/bin/env python3

import signal
import boto3
import os
import subprocess
import argparse

class EC2InstanceManager:
    def __init__(self, ec2_client):
        self.ec2_client = ec2_client

    def list_instances(self, filter=None):
        response = self.ec2_client.describe_instances()
        instances_list = []

        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                instance_id = instance['InstanceId']
                instance_name = 'N/A'
                if 'Tags' in instance:
                    for tag in instance['Tags']:
                        if tag['Key'] == 'Name':
                            instance_name = tag['Value']
                            break

                if filter is None or filter.lower() in instance_name.lower():
                    instances_list.append({
                        'Name': instance_name,
                        'Instance ID': instance_id
                    })

        return instances_list

class ConnectionManager:
    @staticmethod
    def ignore_signal(signum, frame):
        pass

    def connect_to_instance_via_ssm(self, instance_id):
        original_handler = signal.signal(signal.SIGINT, self.ignore_signal)
        process = subprocess.Popen(["aws", "ssm", "start-session", "--target", instance_id])
        try:
            process.wait()
        except Exception as e:
            print(f"Unexpected error: {e}")
        signal.signal(signal.SIGINT, original_handler)
        if process.returncode != 0:
            print(f"Failed to start session with return code: {process.returncode}")

class MainApp:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='Filter EC2 instances by name.')
        self.parser.add_argument('-f', '--filter', help='Filter instances by name', required=False)
        args = self.parser.parse_args()

        aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
        aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
        aws_session_token = os.environ.get('AWS_SESSION_TOKEN') 

        session = boto3.Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            aws_session_token=aws_session_token
        )

        self.ec2_client = session.client('ec2')
        self.ec2_manager = EC2InstanceManager(self.ec2_client)
        self.connection_manager = ConnectionManager()

    def run(self):
        instances = self.ec2_manager.list_instances(self.parser.parse_args().filter)

        if not instances:
            print("No EC2 instances found!")
            return

        for idx, instance in enumerate(instances, 1):
            print(f"{idx}. ID: {instance['Instance ID']}   Name: {instance['Name']}")

        choice = input("Enter the number of the EC2 instance you want to connect to: ")

        try:
            chosen_instance = instances[int(choice) - 1]
            self.connection_manager.connect_to_instance_via_ssm(chosen_instance['Instance ID'])
        except (ValueError, IndexError):
            print("Invalid choice!")

def main():
    app = MainApp()
    app.run()

if __name__ == '__main__':
    main()