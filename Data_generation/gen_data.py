import socket
import cv2
import numpy as np
import keyboard

host = '127.0.0.1'  
port = 5555

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))

cap = cv2.VideoCapture(0)

while True:
    if keyboard.is_pressed('enter'):  
        ret, frame = cap.read()
        _, img_encoded = cv2.imencode('.jpg', frame)

        size = len(img_encoded).to_bytes(4, byteorder='big')

        client_socket.sendall(size)

        client_socket.sendall(img_encoded.tobytes())
        print("Image sent successfully!")
    elif keyboard.is_pressed('esc'):
        print("Program stopped.")
        break

cap.release()
client_socket.close()
