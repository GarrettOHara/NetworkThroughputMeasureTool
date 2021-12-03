import socket
import sys
import threading
import time
import datetime

# --- constants ---

HOST = ''   
PORT = 8000

# --- functions ---

def handle_client(conn, addr):
    try:

        while True:
            data = conn.recv(1024)
            print('recv:', data)

            data = str(datetime.datetime.now()).encode()
            conn.send(data)
            print('send:', data)

            print('--- sleep ---')

            time.sleep(1)

    except BrokenPipeError:
        print('[DEBUG] addr:', addr, 'Connection closed by client?')
    except Exception as ex:
        print('[DEBUG] addr:', addr, 'Exception:', ex, )
    finally:
        conn.close()

# --- main ---

try:
    print('[DEBUG] create socket')    
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print('[DEBUG] bind:', (HOST, PORT))
    s.bind((HOST, PORT))
    print('[DEBUG] listen')
    s.listen(1)

    while True:
        print('[DEBUG] accept ... waiting')
        conn, addr = s.accept()
        print('[DEBUG] addr:', addr)
        t = threading.Thread(target=handle_client, args=(conn, addr))
        t.start()

except Exception as ex:
    print(ex)
except KeyboardInterrupt as ex:
    print(ex)
except:
    print(sys.exc_info())
finally:
    print('[DEBUG] close socket')
    s.close()