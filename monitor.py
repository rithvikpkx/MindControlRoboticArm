import socket
import json
import time

ENABLE_BLINK = False
ENABLE_ATTENTION = not ENABLE_BLINK

def parse(data):
    try:

        json_data = json.loads(data)

        if ENABLE_ATTENTION:
            if 'eSense' in json_data:
                print("Attention value: " + str(json_data['eSense']['attention']))
                print()

        if ENABLE_BLINK:
            if('blinkStrength' in json_data):
                print("Blink value: " + str(json_data['blinkStrength']))           
                print()


    except:
        pass


my_write_buffer = b'{"enableRawOutput": true, "format": "Json"}'

try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 13854))
    client.send(my_write_buffer)
    while True:
        data = client.recv(2048)
        if not data:
            break
        packets = data.decode('utf-8').split('\r')
        for packet in packets:
            parse(packet.strip())
    time.sleep(5)
    client.close()
except socket.error as se:
    print("Error:", se)