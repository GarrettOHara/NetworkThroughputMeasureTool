import psutil
import time
import os

while(True):
    interval = 1
    t0 = time.time()
    upload0 = psutil.net_io_counters().bytes_sent
    download0 = psutil.net_io_counters().bytes_recv
    time.sleep(interval)

    t1 = time.time()
    upload1 = psutil.net_io_counters().bytes_sent
    download1 = psutil.net_io_counters().bytes_recv

    upload = (upload1 - upload0) / (t1 - t0)
    download = (download1 - download0) / (t1 - t0)

    print('Upload (Mbps): ', round(upload/1000000, 3))
    print('Download (Mbps): ', round(download/1000000, 3))
    time.sleep(1)
