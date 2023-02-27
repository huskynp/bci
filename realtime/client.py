import socket
import json
import time
import threading
import ai
import preprocess
import graph
import pandas as pd
import numpy as np


ADDR = ("169.254.109.74", 33223)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(ADDR)
print("Connected to server")

oldt = 0
FS = 75


def detection(data):
    global oldt, conn
    # print("Running...")
    #print("Data", data)
    new = {"ch1": list(data['ch1']), "ch2": list(data['ch2']), "ch3": list(
        data['ch3'])}
    preprocessed = preprocess.preprocess(pd.DataFrame(new))
    new['preprocessed'] = preprocessed
    is_blink = ai.run_ai(preprocessed)
    # print(is_blink)
    newt = data['time']
    new['time'] = list(np.arange(oldt, newt, 1/FS))
    #print("Updating", new)
    graph.update_data(new, is_blink)
    oldt = newt


def event_loop():
    while True:
        b = b''
        b += s.recv(65536)
        print(b)
        data = json.loads(b.decode("utf-8"))
        print("recieved")
        detection(data)


t = 0


def test():
    import random
    global t
    while True:
        test_data = {"ch1": [0], "ch2": [0], "ch3": [
            0], "preprocessed": [1], "time": [t]}
        t += 0.5
        graph.update_data(test_data, random.choice([True, False]))
        time.sleep(0.5)


loop = threading.Thread(target=event_loop, daemon=True)
loop.start()
#testloop = threading.Thread(target=test, daemon=True)
# testloop.start()
graph.run_server()
