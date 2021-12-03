import threading
import time

def test(msg):
  try:
    while True:
      print(msg)
      time.sleep(0.1)
  except KeyboardInterrupt:
    print("INTURRPT")
  
A = "RUNNING"
B = "FASTER"
threadA = threading.Thread(target=test,args=(A,))
threadB = threading.Thread(target=test,args=(B,))

threadA.start()
