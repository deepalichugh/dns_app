## Code for the Fibonacci Server
from flask import Flask, request
import socket

app = Flask(__name__)

@app.route('/register', methods=['PUT'])
def register():
    fs_ip = request.json.get("ip")
    as_ip = request.json.get("as_ip")
    as_port = request.json.get("as_port")
    hostname = request.json.get("hostname")
    print("REGISTERING")
    # Need to query AS first
    data = "TYPE=A\nNAME="+hostname+"\nVALUE="+fs_ip+"\nTTL=10"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(bytes(data, "utf-8"), (as_ip, as_port))
    status, addr = sock.recvfrom(1024)
    sock.close()
    print(status.decode())
    if status.decode()=='201':
        return "Success",201
    else:
        return "Bad Request",400

@app.route('/fibonacci', methods=['GET'])
def get_fibo():
    sequence_number = request.args.get("number")
    not_int = False
    try:
        sequence_number = int(sequence_number)
    except:
        not_int = True
    
    if not_int:
        return "Sequence number not an integer", 400
    
    elif isinstance(sequence_number, int) and sequence_number >0:
        print("Valid seq num")
        ans = fibonacci(sequence_number)
        print("ANS "+str(ans))
        return str(ans), 200
    else:
        return "Invalid Sequence number", 400

def fibonacci(n):
    if n==1:
        return 0
    if n==2:
        return 1
    return fibonacci(n-1)+fibonacci(n-2)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port='9090')