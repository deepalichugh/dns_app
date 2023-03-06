## Code for the User Server
from flask import Flask, request
import requests
import socket

app = Flask(__name__)

@app.route('/fibonacci', methods=['GET'])
def get_fibonacci():
    args = request.args
    hostname = args.get("hostname")
    fs_port = args.get("fs_port")
    number = args.get("number")
    as_ip = args.get("as_ip")
    as_port = args.get("as_port")
    if hostname is None or fs_port is None or number is None or as_ip is None or as_port is None:
        return "Parameters missing. Invalid request", 400
    else:
        print("Valid request")
        # Need to query AS first
        data = "TYPE=A\nNAME="+hostname
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(bytes(data, "utf-8"), (as_ip, int(as_port)))
        resp,addr = sock.recvfrom(1024)
        sock.close()

        response_body = resp.decode()
        print("Resp\n")
        print(response_body)
        response_body_split = response_body.split("\n")
        print(len(response_body_split))
        fs_ip = response_body_split[2][6:]
        print("Printing fs_ip\n")
        print(fs_ip)
        # After querying need to make rest call to FS
        url = "http://"+fs_ip+":"+fs_port+"/fibonacci?number="+number
        response = requests.get(url)
        if response.status_code == 400:
            return "Invalid Sequence number", 400
        else:
            return response.text, 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port='8080')