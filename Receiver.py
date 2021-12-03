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

server_socket = None

def write_data(host, port):
    dic = {
        "host":host,
        "port":port
    }
    with open('data.json','w', encoding='utf-8') as f:
        json.dump(dic, f, ensure_ascii=False, indent=2)

def handle_client(conn,addr):
    try:
      global COUNT
      COUNT = 0
      while True:
          data = conn.recv(1024)
          print('\nrecv:', data)
          data = str(datetime.datetime.now())
          if data:
              COUNT += len(data)
          print("BUFFER:" + str(COUNT))
          print('------------------------------------')
          time.sleep(0.5)

    except BrokenPipeError:
        print('[DEBUG] addr:', addr, 'Connection closed by client?')
    except Exception as ex:
        print('[DEBUG] addr:', addr, 'Exception:', ex, )
    finally:
        print("BUFFER:" + COUNT)
        conn.close()

def main():

  # CONFIGURE SOCKET
  server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
  # SOLUTION FOR "[Error 89] Address already in use". Use before bind()
  # s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1);

  # SETUP HOSTING DATA
  host = "0.0.0.0"
  port = 8000

  # GET CUSTOM DATA
  tmp = input("Please specify host IP address [ENTER NOTHING FOR DEFAULT]: ")
  if tmp != "":
      host = tmp

  tmp = input("Please specify what port to send data on [ENTER NOTHING FOR DEFAULT PORT]: ")
  if tmp != "": 
      port = tmp
  
  # PRINT AND SAVE CONNECTION DATA
  print("YOU'RE CONFIGURED WITH\nHOST: {}\nPORT: {}".format(host, port))
  write_data(host,port)

  # BIND SERVER TO PORT
  server_socket.bind((host,port))
  server_socket.listen()
  
  
  (clientConnected, clientAddress) = server_socket.accept();

  # INITIALIZE MEASUREMENT VARIABLES
  COUNT = 0
  start_time = datetime.datetime.now()
  bandwidth = []
  timeframe = []

  while(COUNT < 10000):
    # SLEEP
    time.sleep(1)

    # MEASURE ELAPSED TIME
    mid_time = datetime.datetime.now()
    mid = mid_time - start_time
    mid = mid.seconds + mid.microseconds / 1000000.0
    tmp = COUNT / 1024 / 1024 / mid

    print("BYTES: {}".format(COUNT))
    print("TIME: {}".format(mid))
    print("BANDWIDTH: {}".format(tmp))
    # RECORD DATA
    timeframe.append(mid)
    bandwidth.append(tmp)

    # COUNT DATA BYTES
    data = clientConnected.recv(512)
    if (data):
      COUNT += len(data)
      print(data)
      print()

    else:
        break
    
  end_time = datetime.datetime.now()
  delta = end_time-start_time
  delta = delta.seconds + delta.microseconds / 1000000.0
  print("\n\n------------------------------------------------\n\n")
  print("TOTAL ELLAPSED TIME: {}".format(delta))
  print("AVERAGE MB/S: {}".format(COUNT / 1024 / 1024 / delta))

  plt.scatter(timeframe,bandwidth)
  plt.show()
    
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