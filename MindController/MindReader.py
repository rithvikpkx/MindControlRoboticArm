import socket  #for communication to the ThingGear connector
import json
import time
import serial  #for communication to the Arduino hand controller
from collections import deque


# Define the COM port and baud rate
HAND_CONTROLLER_COM_PORT = 'COM5'  # Change this to the appropriate COM port
BAUD_RATE = 9600

# Open the serial port
ser = serial.Serial(HAND_CONTROLLER_COM_PORT, BAUD_RATE)


BLINK_STREANGTH_GREATER_THAN = 80
blink_count = 0
blink_start_time = time.time()
blink_interval = 10  # 2-second interval for counting blinks
blink_window = deque(maxlen=10)  # Window size for storing blink data

ATTENTION_STREANGTH_GREATER_THAN = 40
ATTENTION_COUNT_GREATER_THAN = 3
attention_start_time = time.time()
attention_count = 0
attention_interval = 5  # 5-second interval for counting attention data
attention_window = deque(maxlen=10)  # Window size for storing attention data



# Building command to enable JSON output from ThinkGear Connector (TGC)
my_write_buffer = b'{"enableRawOutput": true, "format": "Json"}'

def parse_json(data):
    global blink_start_time
    global attention_start_time
    try:
        json_data = json.loads(data)
         # Do whatever you want with the JSON data here
        if 'eSense' in json_data:
            if json_data['eSense']['attention'] > ATTENTION_STREANGTH_GREATER_THAN :
                attention_window.append(1)
                print(json_data['eSense'])

        if time.time() - attention_start_time >= attention_interval:
            attention_count = sum(attention_window)  # Sum of 1's in the window
            print(f"Attention strength greater than {ATTENTION_STREANGTH_GREATER_THAN} count in {attention_interval} seconds: {attention_count}")
            if attention_count > ATTENTION_COUNT_GREATER_THAN : 
                ser.write(str(99).encode())
                time.sleep(10)
            attention_start_time = time.time()  # Reset the start time
            attention_window.clear()  # Clear the window for the next interval


        if 'blinkStrength' in json_data:
            if json_data['blinkStrength'] > BLINK_STREANGTH_GREATER_THAN : 
                blink_window.append(1)  # Append a '1' to the window if blink is detected
                print(json_data)

        if time.time() - blink_start_time >= blink_interval:
            blink_count = sum(blink_window)  # Sum of 1's in the window
            print(f"Blink strength greater than {BLINK_STREANGTH_GREATER_THAN} count in {blink_interval} seconds: {blink_count}")
            if blink_count > 0 : 
                if blink_count > 5 : 
                    blink_count = 5
                ser.write(str(blink_count).encode())
                time.sleep(5)
            blink_start_time = time.time()  # Reset the start time
            blink_window.clear()  # Clear the window for the next interval

    except json.JSONDecodeError as e:
        #print("Error decoding JSON:", e)
        #ser.close()
        pass



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
            parse_json(packet.strip())
    time.sleep(5)
    client.close()
except socket.error as se:
    pass
