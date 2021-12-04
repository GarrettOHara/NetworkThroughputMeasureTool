# Garrett O'Hara
# REDID: 822936303
# CS 578: Wireless Networks
# Dr. Wang

import os
import sys
import csv
import time
import json
import socket
import threading
import traceback
from graph import scatter_plot


# FIND PORT TO CLEAR WITH:
# sudo netstat -plnt | grep { PORT NUMBER }


BUFFER = 0
DEFAULT = True
THROUGHPUT = []
TERMINATE = False
PACKET_SIZE = 1024
SERVER_SOCKET = None
DISCONNECT = "!DISCONNECT"


def save_results(time, throughput):
    header = ["TIME", "THROUGHPUT"]
    rows = zip(time, throughput)
    with open("data.csv", 'w', newline='')as csvfile:
        write = csv.writer(csvfile)
        write.writerow(header)
        for row in rows:
            write.writerow(row)
    print("SAVED DATA TO FILE")


def write_connection_data(host, port):
    dic = {
        "host":host,
        "port":port,
        "packet_size": PACKET_SIZE
    }
    with open('data.json','w', encoding='utf-8') as f:
        json.dump(dic, f, ensure_ascii=False, indent=2)


def client():
    global BUFFER

    if DEFAULT: 
        conn, addr = SERVER_SOCKET.accept()
        conn.settimeout(1)
        print("[NEW CONNECTION] {} connected.".format(addr))
        while not TERMINATE:
            data = conn.recv(PACKET_SIZE)
            if not data:
                break

            BUFFER += len(data)
            
        conn.close()
    else:
        while not TERMINATE:
            data, addr = SERVER_SOCKET.recvfrom(PACKET_SIZE)
            if not data:
                    break
            
            BUFFER += len(data)


def measure_bandwidth():
    global BUFFER
    global THROUGHPUT

    while not TERMINATE:
        BUFFER = 0
        time.sleep(1)

        # ASSUME EXACTLY 1 SECOND
        # CONVERT BYTES TO BITS
        throughput = BUFFER * 8
        THROUGHPUT.append(throughput)


def timer():
    threading.Thread(target=measure_bandwidth,args=()).start()


def start():
    if DEFAULT:
        SERVER_SOCKET.listen()
    print("RUNNING ON: {}".format(SERVER_SOCKET))
    threading.Thread(target=client, args=()).start()
    print("ACTIVE CONNECTIONS: {}".format(threading.activeCount() -1))


def main():
    global SERVER_SOCKET
    global PACKET_SIZE
    global TERMINATE
    global DEFAULT

    # SELECT TCP OR UDP PROTOCOL
    tmp = "DEFAULT protocol is TCP, would you like to change to UDP? [Y/N]: "
    if "y" in input(tmp).lower():
        print("USING UDP")
        DEFAULT = False
        socket_protocol = socket.SOCK_DGRAM
    else:
        print("USING TCP")
        socket_protocol = socket.SOCK_STREAM
    
    # CONFIGURE SOCKET
    SERVER_SOCKET = socket.socket(socket.AF_INET, socket_protocol)

    # SETUP HOSTING DATA
    local = socket.gethostbyname(socket.gethostname())
    print("DEFAULT LOCAL IP ADDRESS IS: {}".format(local))
    host = local
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
    
    tmp = input("Please specify desired packet size"+
        "[ENTER NOTHING FOR DEFUALT 1024]: "
    )
    if tmp != "":
        PACKET_SIZE = int(tmp)

    

    # PRINT AND SAVE CONNECTION DATA
    print("YOU'RE CONFIGURED WITH\nHOST: {}\nPORT: {}".format(host, port))
    write_connection_data(host,port)

    # BIND SERVER TO PORT
    SERVER_SOCKET.bind((host,port))

    # OPEN SOCKET AND START TIMER
    start()
    timer()

    # KEEP SOCKET AND TIMER RUNNING UNTIL COMMAND
    while input() != "stop":
        pass
    
    # STOP THREADS
    print("TERMINATED")
    TERMINATE = True
    
    # GRAPH RESULTS
    TIME = [x for x in range(len(THROUGHPUT))]
    print("\n\nTHROUGHPUT LENGTH: {}".format(len(THROUGHPUT)))
    print("TIME LENGTH: {}\n\n".format(len(TIME)))
    save_results(TIME, THROUGHPUT)
    threading.Thread(target=scatter_plot, args=(TIME, THROUGHPUT)).start()


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