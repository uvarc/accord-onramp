#!/usr/bin/env python3

import boto3

db = boto3.client("dynamodb")
table = "accord-blocks"
response = db.scan(TableName=table)
blocks = response["Items"]
bls = []
for block in blocks:
    subn = block['block_value']['S']
    bls.append(subn)

print(bls)