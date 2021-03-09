import boto3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def get_sg_ec2_table(client):
    # client = boto3.client('ec2', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

    res=client.describe_instances()
    reservations = res['Reservations']
    sglist_EC2_table = pd.DataFrame()

    for reservation in reservations:
        name_value = None
        instance = reservation['Instances'][0]
        securitygroups = instance['SecurityGroups']
        if 'Tags' in instance:
            Tags = instance['Tags']
            for Tag in Tags:
                if Tag['Key'] == 'Name':
                    name_value = Tag['Value']
        for securitygroup in securitygroups:
            add = pd.DataFrame({
                'SGID':[securitygroup['GroupId']],
                'Security Group Name':[securitygroup['GroupName']],
                'Linked EC2 id':[instance['InstanceId']],
                'Linked EC2 Name': [name_value],
                'Linked EC2 Status': [instance['State']['Name']]
            })
            sglist_EC2_table = sglist_EC2_table.append(add,ignore_index=True)

    sglist_EC2_table = sglist_EC2_table.sort_values(by=['SGID'])
    return sglist_EC2_table
