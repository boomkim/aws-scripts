import boto3
import pandas as pd
import numpy as np
from datetime import date
import matplotlib.pyplot as plt
import sys
import argparse

import sg_simple_list as simplelist
import sg_inbound as inbound
import sg_outbound as outbound
import sg_ec2 as ec2
import sg_eni as eni

parser = argparse.ArgumentParser()
parser.add_argument('--aws-access-key-id',dest='aws_access_key_id')
parser.add_argument('--aws-secret-access-key',dest='aws_secret_access_key')
parser.add_argument('--region',dest='aws_region',default='ap-northeast-2')
parser.add_argument('--name',default='',dest='name')
args = parser.parse_args()

name = args.name
today = date.today().isoformat()

aws_access_key_id = args.aws_access_key_id
aws_secret_access_key = args.aws_secret_access_key
aws_region = args.aws_region

filename = f'securitygroup_list_{name}-{today}-{aws_region}.xlsx'

client = boto3.client('ec2', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=aws_region)

sg_simplelist_table = simplelist.get_sg_simplelist_table(client)
sg_simplelist_table = simplelist.get_sg_simplelist_table(client)
sg_inbound_table = inbound.get_sg_inbound_table(client)
sg_outbound_table = outbound.get_sg_outbound_table(client)
sg_eni_table = eni.get_sg_eni_table(client)
sg_ec2_table = ec2.get_sg_ec2_table(client)



with pd.ExcelWriter(filename) as writer:  
    sg_simplelist_table.to_excel(writer, sheet_name='SG_simplelist', index=False)
    sg_inbound_table.to_excel(writer, sheet_name='SG_inbound_policy', index=False)
    sg_outbound_table.to_excel(writer, sheet_name='SG_outbound_policy', index=False)
    sg_eni_table.to_excel(writer, sheet_name='SG_ENI_Relation', index=False)
    sg_ec2_table.to_excel(writer, sheet_name='SG_EC2_Relation', index=False)
