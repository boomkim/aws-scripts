# node 당 shard 사용 개수
# 각 node의 disk 사용량 disk 사용 percentage
# 클러스터의 unassigned 된 shard 개수

import json
import os
import boto3
from elasticsearch import Elasticsearch

client = boto3.client('cloudwatch')

endpoint = os.environ['ESEndpoint']
es = Elasticsearch(endpoint)

def lambda_handler(event, context):
    nodes = es.cat.nodes(format='json',h=['r','disk.used','disk.used_percent','id'],full_id=True)
    for node in nodes:
        node_metrics = []
        node_id = node['id']
        node_role = node['r']
        metric_dim = [
            {'Name':'NodeId','Value':node_id},
            {'Name':'Role', 'Value': node_role}
        ]
        
        #노드 당 디스크 사용량
        disk_used_str = node['disk.used']
        disk_used = float(disk_used_str[:-2])
        used_unit = 'Gigabytes'
        if disk_used_str[-2:] == 'kb':
            used_unit = 'Kilobytes'
        elif disk_used_str[-2:] == 'gb':
            pass
        node_metrics.append({
            'MetricName': 'disk_used',
            'Dimensions': metric_dim,
            'Value': disk_used,
            'Unit': used_unit
        })
        
        #노드 당 디스크 사용률
        disk_percentage = float(node['disk.used_percent'])
        node_metrics.append({
            'MetricName': 'disk_percentage',
            'Dimensions': metric_dim,
            'Value': disk_percentage,
            'Unit': 'Percent'
        })
        
        #노드 당 샤드 수 
        if node_role== 'di':
            shards_per_node = int(es.cat.allocation(node_id=node_id,h=['shards'],format='json')[0]['shards'])
            node_metrics.append({
                'MetricName': 'shards',
                'Dimensions': metric_dim,
                'Value': shards_per_node
            })
        response = client.put_metric_data(
            Namespace='elasticsearch',
            MetricData = node_metrics
        )
        print("node metric sent:",node_id)
        print(response)
        
        
    metrics = []
    # UNASSIGNED 샤드 수 측정 
    shards = es.cat.shards(format='json')
    num_unassigned = 0
    for shard in shards:
        if shard['state'] == 'UNASSIGNED':
            num_unassigned =+ 1
        
    # UNASSIGNED 샤드 수 metric에 추가
    metrics.append(
        {
            'MetricName': 'UNASSIGNED shards',
            'Value': num_unassigned
        })
    
    response = client.put_metric_data(
        Namespace='elasticsearch',
        MetricData = metrics
        )
    print("unassigned shards sent:", num_unassigned)
    print(response)

    return {'message': 'ES metric sent'}
