# Garrett O'Hara
# REDID: 822936303
# CS 578: Wireless Networks
# Dr. Wang

import os
import sys
import json
import socket
import traceback
import threading

HEADER = 64
BUFFSIZE = 1024
FORMAT = "utf-8"
DISCONNECT = "!DISCONNECT"

def get_connection_data():
    data = {}
    with open('data.json') as r:
        data = json.load(r)
    return data['host'], data['port']

def send_UDP(msg,sender,host,port):
    while True:
        message = msg.encode(FORMAT)
        # SEND BYTE ARRAY
        sender.sendto(bytes(message),(host,port))
    

def send_TCP(msg, sender):
    while True:
        message = msg.encode(FORMAT)
        length = len(message)
        send_length = str(length).encode(FORMAT)
        send_length += b' '* (HEADER - length)
        sender.send(send_length)
        sender.send(message)
        print(send_length)
        print(message)

def main():

    # SELECT TCP OR UDP PROTOCOL
    DEFAULT = True
    tmp = "DEFAULT protocol is TCP, would you like to change to UDP? [Y/N]: "
    if "y" in input(tmp).lower():
        print("USING UDP")
        DEFAULT = False
        socket_protocol = socket.SOCK_DGRAM
    else:
        print("USING TCP")
        socket_protocol = socket.SOCK_STREAM
    
    # CONFIGURE SOCKET
    server_socket = socket.socket(socket.AF_INET, socket_protocol);

    # GET CONNECTION DATA
    host, port = get_connection_data()
    print("\nHOST: {}\nPORT: {}".format(host,port))

    # CONNECT TO SERVER
    server_socket.connect((host,port))

    # SEND DATA TO SERVER
    if DEFAULT:
        print("RUNNING TCP")
        threading.Thread(target=send_TCP,
            args=("TEST DATA", server_socket)
        ).start()
        # send_TCP("TEST DATA", server_socket)
    else:
        print("RUNNING UDP")
        threading.Thread(target=send_UDP,
            args=("TEST DATA", server_socket, host, port)
        ).start()
        # send_UDP("TEST DATA", server_socket, host, port)

    # DISSCONECT
    if DEFAULT:
        send_TCP(DISCONNECT, server_socket)
    else:
        send_UDP(DISCONNECT, server_socket, host, port)
 
if __name__ == "__main__":
    try:
        main()

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
            sys.exit(0)
        except SystemExit:
            os._exit(0)