import socket
import cv2
import numpy as np
import os
import shutil
import utils
from deepface import DeepFace
import tenseal as ts

host = '0.0.0.0'
port = 5555
image_folder = "rc"
enc_img_folder = "Encrypted_images"

if os.path.exists(image_folder):
    shutil.rmtree(image_folder)
if os.path.exists(enc_img_folder):
    shutil.rmtree(enc_img_folder)

os.makedirs(image_folder, exist_ok=True)
os.makedirs(enc_img_folder,exist_ok=True)


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(1)  

print(f"Server listening on {host}:{port}")

client_socket, client_address = server_socket.accept()
print(f"Connection from {client_address}")

while True:
    size = int.from_bytes(client_socket.recv(4), byteorder='big')
    if size == 0:
        continue
    image_data = b""
    while len(image_data) < size:
        image_data += client_socket.recv(4096)

    image_array = np.frombuffer(image_data, dtype=np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    image_filename = f"rc_{len(os.listdir(image_folder)) + 1}.jpg"

    cv2.imwrite(os.path.join(image_folder, image_filename), image)

    print(f"Image saved: {image_filename}")

    context = ts.context_from(utils.read_data('keys\secret.txt'))
    image_embedding = DeepFace.represent(f'rc/{image_filename}',model_name='Facenet')[0]['embedding']
    print(f"{image_filename} Embedding taken")
    encrypted = ts.ckks_vector(context,image_embedding)
    print(f"{image_filename} Encrypted")
    utils.write_data(f'Encrypted_images\{image_filename[:-4]}.txt',encrypted.serialize())
    print("Encrypted file saved")

