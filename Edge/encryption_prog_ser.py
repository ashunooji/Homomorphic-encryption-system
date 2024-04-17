import os
import shutil
import utils
from deepface import DeepFace
import tenseal as ts
from tqdm import tqdm

image_folder = "rc"
enc_img_folder = "Encrypted_images"

if os.path.exists(enc_img_folder):
    shutil.rmtree(enc_img_folder)

os.makedirs(image_folder, exist_ok=True)
os.makedirs(enc_img_folder,exist_ok=True)


for image_filename in tqdm(os.listdir("rc")):
    context = ts.context_from(utils.read_data('keys\secret.txt'))
    try:
        image_embedding = DeepFace.represent(f'rc/{image_filename}',model_name='Facenet')[0]['embedding']
    except ValueError:
        continue
    #print(f"{image_filename} Embedding taken")
    encrypted = ts.ckks_vector(context,image_embedding)
    #print(f"{image_filename} Encrypted")
    utils.write_data(f'Encrypted_images\{image_filename[:-4]}.txt',encrypted.serialize())
    #print("Encrypted file saved")

