# ---------------------------------------------------------
    # print("NEW CONNECTION: {}".format(addr))
    # connected = True
    # while(connected):
    #     # conn.recv() is a block, this is why it needs to be
    #     # in a new thread
    #     message_length = conn.recv(HEADER).decode(FORMAT)
    #     if message_length:

    #         message_length = int(message_length)
    #         msg = conn.recv(message_length).decode(FORMAT)

    #         if msg == DISCONNECT:
    #             connected = False

    #         print("ADDR: {} SENT {}".format(addr, msg))
        
    # conn.close()
    # ---------------------------------------------------------




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