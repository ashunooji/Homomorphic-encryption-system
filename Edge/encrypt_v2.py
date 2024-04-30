import os
import shutil
import utils
from deepface import DeepFace
import tenseal as ts
from tqdm import tqdm
import multiprocessing
import time

context = ts.context_from(utils.read_data('keys\secret.txt'))

def encrypt(file_list):
    for i in (file_list):
        try:
            image_embedding = DeepFace.represent(f"rc/{i}",model_name="Facenet")[0]['embedding']
        except ValueError:
            continue
        encrypted = ts.ckks_vector(context,image_embedding)
        utils.write_data(f"encrypted_images/{i[:-4]}.txt",encrypted.serialize())

def encrypt_normal(image_folder):
    for image_filename in tqdm(os.listdir(image_folder)):
        try:
            image_embedding = DeepFace.represent(f'{image_folder}/{image_filename}',model_name='Facenet')[0]['embedding']
        except ValueError:
            continue
        #print(f"{image_filename} Embedding taken")
        encrypted = ts.ckks_vector(context,image_embedding)
        #print(f"{image_filename} Encrypted")
        utils.write_data(f'Encrypted_images\{image_filename[:-4]}.txt',encrypted.serialize())
        #print("Encrypted file saved")
    print("Encryption done using normal processing")

def encrypt_parallel(image_folder):

    filenames = [file for file in os.listdir(image_folder)]
    part_length = len(filenames)//3
    f1 = filenames[:part_length]
    f2 = filenames[part_length:2*part_length]
    f3 = filenames[2*part_length:]

    p1 = multiprocessing.Process(target=encrypt,args=(f1,))
    p2 = multiprocessing.Process(target=encrypt,args=(f2,))
    p3 = multiprocessing.Process(target=encrypt,args=(f3,))

    p1.start()
    p2.start()
    p3.start()

    p1.join()
    p2.join()
    p3.join()

    print("Encryption done using Parallel processing")
    return

if __name__ == "__main__":

    image_folder = "rc"
    enc_img_folder = "Encrypted_images"

    if os.path.exists(enc_img_folder):
        shutil.rmtree(enc_img_folder)

    os.makedirs(image_folder, exist_ok=True)
    os.makedirs(enc_img_folder,exist_ok=True)

    length = len(os.listdir(image_folder))
    s = time.time()
    if length <= 40:
        encrypt_normal(image_folder)
    else:
        encrypt_parallel(image_folder)
    e = time.time()
    print(f"Time taken is {e-s} seconds")
