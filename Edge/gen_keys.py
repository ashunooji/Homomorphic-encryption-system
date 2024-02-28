import tenseal as ts
import utils
import os

context = ts.context(ts.SCHEME_TYPE.CKKS, poly_modulus_degree = 8192, coeff_mod_bit_sizes = [60, 40, 40, 60])
context.generate_galois_keys()
context.global_scale = 2**40
print("Keys Generated")

print(os.getcwd())  
path = os.path.join(os.getcwd(),"keys")
os.mkdir(path)

secret_context = context.serialize(save_secret_key = True)
utils.write_data("keys\secret.txt", secret_context)
print("Secret key stored successfully in the folder keys")
 
context.make_context_public() #drop the secret_key from the context
public_context = context.serialize()
utils.write_data("keys\public.txt", public_context)
print("Public key stored successully in the folder keys")