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

from Receiver import DEFAULT

FORMAT = "utf-8"
PACKET_SIZE = 1024
SERVER_SOCKET = None
DISCONNECT = "!DISCONNECT"


def get_connection_data():
    data = {}
    with open('data.json') as r:
        data = json.load(r)
    return data['host'], data['port']

def start(host, port):
    if DEFAULT:
        print("RUNNING TCP")
        threading.Thread(target=send_TCP,
            args=(host, port)
        ).start()
        
    else:
        print("RUNNING UDP")
        threading.Thread(target=send_UDP,
            args=(host, port)
        ).start()

def send_UDP(host,port):
    # CREATE BYTE ARRAY
    arr = bytearray(PACKET_SIZE)

    # SEND DATA
    try:
        while True:
            print(arr)
            SERVER_SOCKET.sendto(arr,(host,port))

    except socket.error as e:
        print("SOCKET ERROR: {}".format(e))
    except IOError as e:
        print("ERROR: {}".format(e))
    finally:
        SERVER_SOCKET.close()
    

def send_TCP(host, port):
    # CONNECT TO SERVER
    SERVER_SOCKET.connect((host,port))

    # CREATE DATA ARRAY
    arr = bytearray(PACKET_SIZE)
    try:
        while True:
            SERVER_SOCKET.send(arr)
            print("DATA SENT")
    except socket.error as e:
        print("SOCKET ERROR: {}".format(e))
    except IOError as e:
        print("ERROR: {}".format(e))
    finally:
        SERVER_SOCKET.close()

def main():
    global SERVER_SOCKET
    global PACKET_SIZE
    global DEFAULT

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
    
    tmp = input("Please specify desired packet size"+
        "[ENTER NOTHING FOR DEFUALT 1024]: "
    )
    if tmp != "":
        PACKET_SIZE = int(tmp)
    
    # CONFIGURE SOCKET
    SERVER_SOCKET = socket.socket(socket.AF_INET, socket_protocol);

    # GET CONNECTION DATA
    host, port = get_connection_data()
    print("\nHOST: {}\nPORT: {}".format(host,port))

    # SEND DATA TO SERVER
    start(host, port)
        
    while input() != "stop":
        pass

if __name__ == "__main__":
    try:
        main()

    except BrokenPipeError:
        print("Server Closed, Shutting down...")
        sys.exit(0)
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