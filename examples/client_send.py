import socket
import sys
import threading
import time

# --- constants ---

HOST = ''
PORT = 8000

# --- functions ---

def sender(s):
    print('sender')  

    while True:
        s.send(data)
        print('send:', data)
        print('--- sleep ---')
        time.sleep(3)

# --- main ---

data = b''

try:
    s = socket.socket()
    s.connect((HOST, PORT))
    text = 'Hello World of Sockets in Python'
    data = text.encode('utf-8')

    threading.Thread(target=sender, args=(s,)).start()

    print('receiver')  
    while True:
        temp = s.recv(1024)
        if temp:
            data = temp
            print('recv:', data)

except Exception as ex:
    print(ex)
except KeyboardInterrupt as ex:
    print(ex)
except:
    print(sys.exc_info())
finally:
    print('[DEBUG] close socket')
    s.close()
