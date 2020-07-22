#!/usr/bin/python
#
#Copyright 2017-2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
#Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file 
#except in compliance with the License. A copy of the License is located at
#
#    http://aws.amazon.com/apache2.0/
#
#or in the "license" file accompanying this file. This file is distributed on an "AS IS" 
#BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the 
#License for the specific language governing permissions and limitations under the License.

#It works EMR 5.30.0 and above. If your cluster is using EMR 5.29 and below, use older script 

import sys, subprocess

is_master = subprocess.check_output(['cat /emr/instance-controller/lib/info/instance.json | jq .isMaster'], shell=True).strip()

if is_master == "true":
    private_ip = str(sys.argv[1])
    res_interface_id = str(sys.argv[2]) 
    instance_id = subprocess.check_output(['/usr/bin/curl -s http://169.254.169.254/latest/meta-data/instance-id'], shell=True)
    interface_id = subprocess.check_output(['aws ec2 describe-instances --instance-ids %s | jq .Reservations[].Instances[].NetworkInterfaces[].NetworkInterfaceId' % instance_id], shell=True).strip().strip('"')
    
    #UnAssign Private IP from Reserved ENI 
    subprocess.check_call(['aws ec2 unassign-private-ip-addresses --network-interface-id %s --private-ip-addresses %s' % (res_interface_id, private_ip)], shell=True)

    #Assign private IP to the master instance:
    subprocess.check_call(['aws ec2 assign-private-ip-addresses --network-interface-id %s --private-ip-addresses %s' % (interface_id, private_ip)], shell=True)

    subnet_id = subprocess.check_output(['aws ec2 describe-instances --instance-ids %s | jq .Reservations[].Instances[].NetworkInterfaces[].SubnetId' % instance_id], shell=True).strip().strip('"').strip().strip('"')
        
    subnet_cidr = subprocess.check_output(['aws ec2 describe-subnets --subnet-ids %s | jq .Subnets[].CidrBlock' % subnet_id], shell=True).strip().strip('"')
    cidr_prefix = subnet_cidr.split("/")[1]

    #Add the private IP address to the default network interface:
    subprocess.check_call(['sudo ip addr add dev eth0 %s/%s' % (private_ip, cidr_prefix)], shell=True)

    #Configure iptablles rules such that traffic is redirected from the secondary to the primary IP address:
    primary_ip = subprocess.check_output(['/sbin/ifconfig eth0 | grep \'inet\' '], shell=True).strip().split()[1] # new
    # primary_ip = subprocess.check_output(['/sbin/ifconfig eth0 | grep \'inet addr:\' | cut -d: -f2 | awk \'{ print $1}\''], shell=True).strip() # old
    subprocess.check_call(['sudo iptables -t nat -A PREROUTING -d %s -j DNAT --to-destination %s' % (private_ip, primary_ip)], shell=True)

    #make shutdown script 
    subprocess.check_call(['mkdir -p /mnt/var/lib/instance-controller/public/shutdown-actions'], shell=True)
    f = open("/mnt/var/lib/instance-controller/public/shutdown-actions/return_ip.sh",'w')
    f.write('#!/bin/bash\n')
    f.write('aws ec2 unassign-private-ip-addresses --network-interface-id %s --private-ip-addresses %s\n' % (interface_id,private_ip))
    f.write('aws ec2 assign-private-ip-addresses --network-interface-id %s --private-ip-addresses %s' % (res_interface_id,private_ip))
    f.close()
else:
    print "Not the master node"
