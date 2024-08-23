from utils.user import User
from utils.handler import parse_data
from utils.user import UserTracker
import serial
# import traceback 

user_count = 5
current_platform = 'b1'
previous_node = 'LIFT'
current_node = 'GANTRY 1'
destination_node = 'EXIT B'

ser = serial.Serial('/dev/cu.usbmodem2102', 115200)  

user = User(id=1,
            current_platform=current_platform,
            previous_node=previous_node,
            current_node=current_node,
            destination=destination_node)

tracker = UserTracker()

tracker.track_user(user)

print("Backend server is now live")

while True:
    if ser.in_waiting:
        data = ser.readline().decode('utf-8').rstrip() 
        print(f"received data: {data}")
        received_values = parse_data(data)
        if received_values:
            tracker.update(user, received_values[1], received_values[2], received_values[3])
     

