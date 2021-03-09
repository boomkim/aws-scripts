import boto3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def get_sg_simplelist_table(client):
    # client = boto3.client('ec2', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

    res=client.describe_security_groups()
    sginfo=res['SecurityGroups']
    sg_simplelist_table = pd.DataFrame()
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
        add = pd.DataFrame({
        'SGID':[sglist['GroupId']],
        'Security Group Name':[sglist['GroupName']],
        'Description':[sglist['Description']]
        })
        sg_simplelist_table=sg_simplelist_table.append(add,ignore_index = True)
    return sg_simplelist_table
