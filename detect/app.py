from chalice import Chalice
import boto3

app = Chalice(app_name='detect')

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
    else:
        print("NOT belongs")
        return False
    return ip_network == prefix_network

def get_blocks():
    db = boto3.client("dynamodb")
    table = "accord-blocks"
    response = db.scan(TableName=table)
    raw = response["Items"]
    blocks = []
    for r in raw:
        subn = {"block": r['block_value']['S'],"campus": r['block_campus']['S']}
        blocks.append(subn)
    return blocks

# def check_blocks(user_ip):
#     blocks = get_blocks()
#     print(blocks)
#     for block['block'] in blocks:
#         if ip_in_prefix(user_ip, block):
#             print("We have a match")
#             return True

def check_blocks(user_ip):
    blocks = get_blocks()
    for block in blocks:
        if ip_in_prefix(user_ip, block['block']):
            # return {"status":"true","campus": block["campus"]}
            return True

# -------- api begins --------- #
@app.route('/')
def index():
    return {'hello': 'world'}

@app.route('/validate/{ip}', methods=['GET'], cors=True)
def validate_ip(ip):
   verify = check_blocks(ip)
   if (verify == True):
       return {'message': "{} is a valid IP address".format(ip), "status":"true","institution":""}
   else:
       return {'message': "{} is an invalid IP address".format(ip), "status":"false"}
