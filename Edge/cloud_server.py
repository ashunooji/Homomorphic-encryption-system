import os
import tenseal as ts
import utils


def search_res(res):
    result = []
    for keys,value in res.items():
        if value > -110 and value < 110:
            result.append(keys)
    return result


def decrypt_results():
    context = ts.context_from(utils.read_data('keys\secret.txt'))
    res = {}
    res_files = r"D:\Major project\Virtual environment\Project\Client\Result_files"
    for i in os.listdir(res_files):
        v = utils.read_data(os.path.join(res_files,i))
        v = ts.lazy_ckks_vector_from(v)
        v.link_context(context)
        res[i] = v.decrypt()[0]
    result = search_res(res)
    print("Results decrypted")
    print()
    return result



if __name__ == "__main__":
    res = decrypt_results()
    if res is None:
        print("No faces detected")
    else:
        print("Face is found in the database, Below are the names of the searched faces : ")
        for i in res:
            print(i)

    
