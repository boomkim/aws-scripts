import boto3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def get_sg_eni_table(client):
    # client = boto3.client('ec2', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

    res = client.describe_network_interfaces()
    networkInterfaces = res['NetworkInterfaces']
    print(len(networkInterfaces))
    sg_eni_table = pd.DataFrame()

    for interface in networkInterfaces:
        name_value = None
        eni_id = interface['NetworkInterfaceId']
        securitygroups = interface['Groups']
        if 'TagSet' in interface:
            Tags = interface['TagSet']
            for Tag in Tags:
                if Tag['Key'] == 'Name':
                    name_value = Tag['Value']
        for securitygroup in securitygroups:
            add = pd.DataFrame({
                'SGID':[securitygroup['GroupId']],
                'Security Group Name':[securitygroup['GroupName']],
                'Linked ENI ID': [eni_id],
                'Linked ENI Name': [name_value],
                'Description': interface['Description']
            })
            sg_eni_table = sg_eni_table.append(add,ignore_index=True)
            
    print(sg_eni_table)
    # sg_eni_table = sg_eni_table.sort_values(by=['SGID'])
    return sg_eni_table
    
    
