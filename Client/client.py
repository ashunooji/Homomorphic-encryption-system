import os
import utils
import tenseal as ts
from deepface import DeepFace
import shutil
from tqdm import tqdm

def compute(enc_imgs,context):
    sample_image = 'input.jpg'
    img_proto = DeepFace.represent(sample_image,model_name='Facenet')[0]['embedding']
    img_ts = ts.plain_tensor(img_proto)

    for file in tqdm(os.listdir(enc_imgs)):
        enc_img_proto = utils.read_data(f"{enc_imgs}/{file}")
        enc_v = ts.lazy_ckks_vector_from(enc_img_proto)
        enc_v.link_context(context)
        euclidean_squard = img_ts - enc_v
        euclidean_squard = euclidean_squard.dot(euclidean_squard)
        utils.write_data(f"Result_files\{file[:-4]}.txt",euclidean_squard.serialize())
    print("Computation Done")


if __name__  == "__main__":   
    enc_imgs = r"D:\Major project\Virtual environment\Project\Edge\Encrypted_images"
    context = ts.context_from(utils.read_data(r"D:\Major project\Virtual environment\Project\Edge\keys\public.txt"))
    if os.path.exists("Result_files"):
        shutil.rmtree("Result_files")

    os.makedirs("Result_files")
    compute(enc_imgs,context)