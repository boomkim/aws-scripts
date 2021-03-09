import boto3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def get_sg_outbound_table(client):
    # client = boto3.client('ec2', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

    res=client.describe_security_groups()
    sginfo=res['SecurityGroups']
    sg_outbound_table = pd.DataFrame()

    for sglist in sginfo:
        name_value = None
        target = None
        Port_Range = 'All'
        IpProtocol = 'All'
        if 'Tags' in sglist:
            Tags=sglist['Tags']
            for Tag in Tags:
                if Tag['Key'] == 'Name':
                    name_value = Tag['Value']
        for outbound in sglist['IpPermissionsEgress']:
            if 'FromPort' in outbound:
                Port_Range = outbound['FromPort']
            if outbound['IpProtocol'] != '-1':
                IpProtocol = outbound['IpProtocol']
            for CidrIp in outbound['IpRanges']:
                if 'CidrIp' in CidrIp:
                    target=CidrIp['CidrIp']
                add = pd.DataFrame({
                'SGID':[sglist['GroupId']],
                'Security Group Name':[sglist['GroupName']],
                'IpProtocol':[IpProtocol],
                'Port Range':[Port_Range],
                'target':[target],
                'Description':[sglist['Description']]
                })
                sg_outbound_table=sg_outbound_table.append(add,ignore_index = True)
    return sg_outbound_table