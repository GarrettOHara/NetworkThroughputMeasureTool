# Garrett O'Hara
# REDID: 822936303
# CS 578: Wireless Networks
# Dr. Wang

from io import RawIOBase
import os
import sys
import time
import json
import socket
import traceback

server_socket = None
HOST_ref = None

def get_connection_data():
    data = {}
    with open('data.json') as r:
        data = json.load(r)
    return data['host'], data['port']

def main():
    
    # CONFIGURE SOCKET
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);

    # GET CONNECTION DATA
    host, port = get_connection_data()
    HOST_ref = host
    print("USING CONNECTION\nHOST: {}\nPORT: {}".format(host,port))

    # CONNECT TO SERVER
    server_socket.connect((host,port))
    # stream = StreamSocket(server_socket,Raw)

    # SEND DATA TO SERVER
    while(True):
        data = "TEST DATA"
        arr = bytes(data,'utf-8')
        server_socket.send(data.encode())
        print("\nSENT.\nRAW: {}\nENCODED:".format(data))
        for byte in arr:
            print(byte, end=' ')
        print()
        time.sleep(0.2)
    

if __name__ == "__main__":
    try:
        main()
    except BrokenPipeError:
        print('[DEBUG] addr:', HOST_ref, 'Connection closed by client?')

    except KeyboardInterrupt:
        try:
            print('\n\nKeyboard Interrupt')
            print("Exiting Program...")
            sys.exit(0)
        except SystemExit:
            os._exit(0)
    except:
        try:
            print("\nERROR:\n")
            traceback.print_exc()
            print("----------------------------------------------------------")
            sys.exit(0)
        except SystemExit:
            os._exit(0)
    finally:
        server_socket.close()