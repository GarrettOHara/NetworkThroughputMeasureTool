# Garrett O'Hara
# REDID: 822936303
# CS 578: Wireless Networks
# Dr. Wang

import os
import sys
import time
import json
import socket
import datetime
import threading
import traceback
import matplotlib.pyplot as plt

# FIND PORT TO CLEAR WITH:
# sudo netstat -plnt | grep { PORT NUMBER }

HEADER = 64
FORMAT = "utf-8"
DISCONNECT = "!DISCONNECT"
BUFFER = 0

def write_connection_data(host, port):
    dic = {
        "host":host,
        "port":port
    }
    with open('data.json','w', encoding='utf-8') as f:
        json.dump(dic, f, ensure_ascii=False, indent=2)

def client(conn, addr):

    print("NEW CONNECTION: {}".format(addr))
    connected = True
    while(connected):
        # conn.recv() is a block, this is why it needs to be
        # in a new thread
        message = conn.recv(HEADER).decode(FORMAT)
        if message:
            message = int(message)
            msg = conn.recv(message).decode(FORMAT)

            if msg == DISCONNECT:
                connected = False

            print("ADDR: {} SENT {}".format(addr, msg))
        
    conn.close()


def start(server):
    server.listen()
    print("RUNNING ON: {}".format(server))

    while True:
        # server.accept() is a block line of code
        conn, addr = server.accept()
        threading.Thread(target=client, args=(conn, addr)).start()
        print("ACTIVE CONNECTIONS: {}".format(threading.activeCount() -1))
    
def bandwidth():
    pass


def main():

    # SETUP HOSTING DATA
    print("YOU'RE LOCAL IP ADDRESS IS: {}".format(socket.gethostbyname(
        socket.gethostname()))
    )
    host = "192.168.1.212"
    port = 8000

    # GET CUSTOM DATA
    tmp = input("Please specify host IP address [ENTER NOTHING FOR DEFAULT]: ")
    if tmp != "":
        host = tmp

    tmp = input("Please specify what port to send data on "+
        "[ENTER NOTHING FOR DEFAULT PORT]: "
    )
    if tmp != "": 
        port = int(tmp)

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

    # SOLUTION FOR "[Error 89] Address already in use". Use before bind()
    # s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1);

    # PRINT AND SAVE CONNECTION DATA
    print("YOU'RE CONFIGURED WITH\nHOST: {}\nPORT: {}".format(host, port))
    write_connection_data(host,port)

    # BIND SERVER TO PORT
    server_socket.bind((host,port))
    # if DEFAULT:
    #     server_socket.listen()

    
    start(server_socket)

    # (clientConnected, clientAddress) = server_socket.accept();
    # print("NEW CONNECTION FROM ADDR: {}".format(clientAddress))


    # # INITIALIZE MEASUREMENT VARIABLES
    # COUNT = 0
    # start_time = datetime.datetime.now()
    # bandwidth = []
    # timeframe = []

    """
    after you wait a second, record calculations, reset the bytes

    total bytes in second * 8  / delta / 1e6 for megabits
    """

    # while(COUNT < 5000):
    #     # SLEEP
    #     time.sleep(1)

    #     # COUNT DATA BYTES
    #     data = clientConnected.recv(1024)
    #     if (data):
    #         COUNT += len(data)

    #         # MEASURE ELAPSED TIME
    #         mid_time = datetime.datetime.now()
    #         mid = mid_time - start_time
    #         mid = mid.seconds + mid.microseconds / 1000000.0
    #         tmp = COUNT / 1024. / mid

    #         print("BYTES: {}".format(COUNT))
    #         print("TIME: {}".format(mid))
    #         print("BANDWIDTH: {}".format(tmp))
    #         # RECORD DATA
    #         timeframe.append(mid)
    #         bandwidth.append(tmp)

    #     else:
    #         break
    
    # end_time = datetime.datetime.now()
    # delta = end_time-start_time
    # delta = delta.seconds + delta.microseconds / 1000000.0
    # print("\n\n------------------------------------------------\n\n")
    # print("TOTAL ELLAPSED TIME: {}".format(delta))
    # print("AVERAGE MB/S: {}".format(COUNT / 1024 / delta))

    # plt.scatter(timeframe,bandwidth)
    # plt.xlabel("Time (seconds)")
    # plt.ylabel("Brandwidth (Mb/s)")
    # plt.show()
    
    # t = threading.Thread(target=handle_client, args=(clientConnected, clientAddress))
    # t.start()
    
if __name__ == '__main__':
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
          print("\nERROR:\n\n")
          traceback.print_exc()
          sys.exit(0)
      except SystemExit:
          os._exit(0)