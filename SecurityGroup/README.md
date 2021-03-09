# Security Group list to Excel
This script make excel file(.xlsx) about your AWS account's security groups. 
There will be 5 sheets. 

- SG_simplelist
- SG_inbound_policy 
- SG_outbound_policy
- SG_ENI_Relation
- SG_EC2_Relation

## Install requirements

```
python -m venv ./ 
pip install requirements 
```
## usage
```
python main.py \
--aws-access-key-id {your-aceess-key} \
--aws-secret-access-key {your-secret-key} \
--region {your-target-region(ex:ap-northeast-2)}
--name {output file name}
```
