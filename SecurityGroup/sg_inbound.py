import boto3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def get_sg_inbound_table(client):
    # client = boto3.client('ec2', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

    res=client.describe_security_groups()
    sginfo=res['SecurityGroups']
    sg_inbound_table = pd.DataFrame()

    for sglist in sginfo:
        name_value = None
        source = None
        Port_Range = 'All'
        IpProtocol = 'All'
        if 'Tags' in sglist:
            Tags=sglist['Tags']
            for Tag in Tags:
                if Tag['Key'] == 'Name':
                    name_value = Tag['Value']
        for sgip in sglist['IpPermissions']:
            if 'FromPort' in sgip:
                Port_Range = sgip['FromPort']
            if sgip['IpProtocol'] != '-1':
                IpProtocol = sgip['IpProtocol']
            else:
                Port_Range = 'All'

            for CidrIp in sgip['IpRanges']:
                if 'CidrIp' in CidrIp:
                    source=CidrIp['CidrIp']
                add = pd.DataFrame({
                'SGID':[sglist['GroupId']],
                'Security Group Name':[sglist['GroupName']],
                'IpProtocol':[sgip['IpProtocol']],
                'Port Range':[Port_Range],
                'source':[source],
                'Description':[sglist['Description']]
                })
                sg_inbound_table=sg_inbound_table.append(add,ignore_index = True)
            for GroupId in sgip['UserIdGroupPairs']:
                if 'GroupId' in GroupId:
                    source=GroupId['GroupId']
                add = pd.DataFrame({
                'SGID':[sglist['GroupId']],
                'Security Group Name':[sglist['GroupName']],
                'IpProtocol':[IpProtocol],
                'Port Range':[Port_Range],
                'source':[source],
                'Description':[sglist['Description']]
                })
                sg_inbound_table=sg_inbound_table.append(add,ignore_index = True)
    return sg_inbound_table
