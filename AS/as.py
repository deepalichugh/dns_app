import json
import socket

udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server = ''
port = 53533
file = "dns_registry.txt"

udp_sock.bind((server, port))

while True:
    res_data, addr = udp_sock.recvfrom(1024)
    decoded_res = res_data.decode('utf-8')
    # if decoded_res == "TYPE=A\nNAME=fibonacci.com":
    if "VALUE=" not in decoded_res and "TTL=" not in decoded_res:
        decoded_res = decoded_res.split('\n')
        type = decoded_res[0][-1]
        name = decoded_res[1][5:]
        with open(file,'r') as dns_file: #lookup
            dns_entries = dns_file.readlines()
            for entry in dns_entries:
                line = json.loads(entry)
                if type == line['TYPE'] and name == line['NAME']:
                    resp = "TYPE="+type+"\nNAME="+name+"\nVALUE="+line['VALUE']+"\nTTL="+line['TTL']
        udp_sock.sendto(str.encode(resp), addr)
    else:
        decoded_res = decoded_res.split('\n')
        type = decoded_res[0][-1]
        name = decoded_res[1][5:]
        value = decoded_res[2][6:]
        ttl = decoded_res[3][4:]
        json_obj = { "TYPE":type, "NAME":name, "VALUE":value, "TTL":ttl}
        with open(file, 'a') as dns_file: #update
            dns_file.write(json.dumps(json_obj)+"\n")
        udp_sock.sendto(str.encode("201"), addr)
