#!/usr/bin/env python3

import os
import boto3


def ip_to_binary(ip):
    octet_list_int = ip.split(".")
    octet_list_bin = [format(int(i), '08b') for i in octet_list_int]
    binary = ("").join(octet_list_bin)
    return binary

def get_addr_network(address, net_size):
    ip_bin = ip_to_binary(address)
    network = ip_bin[0:32-(32-net_size)] 
    return network

def ip_in_prefix(ip_address, prefix):
    [prefix_address, net_size] = prefix.split("/")
    net_size = int(net_size)
    prefix_network = get_addr_network(prefix_address, net_size)
    ip_network = get_addr_network(ip_address, net_size)
    if (ip_network == prefix_network):
        print("YES belongs")
        return True
    # else:
    #     print("NOT belongs")
    #     return False
    # return ip_network == prefix_network

# blocks = [
#     "192.168.1.0/24",
#     "192.168.2.0/24",
#     "192.168.3.0/24",
#     "192.168.5.0/24"
# ]

blocks = [{'block': '216.126.0.0/16', 'campus': 'UVA - nem2p Office'}, {'block': '128.143.0.0/16', 'campus': 'UVA'}, {'block': '199.111.0.0/16', 'campus': 'UVA'}]

# def get_blocks():
#     db = boto3.client("dynamodb")
#     table = "accord-blocks"
#     response = db.scan(TableName=table)
#     raw = response["Items"]
#     blocks = []
#     for r in raw:
#         subn = r['block_value']['S']
#         blocks.append(subn)
#     return blocks

def check_blocks(user_ip):
    # blocks = get_blocks()
    for block in blocks:
        if ip_in_prefix(user_ip, block['block']):
            return {"status":"true","campus": block["campus"]}
            # return True
        else:
            return {"status":"false"}

check_blocks("128.144.1.1")