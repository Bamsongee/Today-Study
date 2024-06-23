import numpy as np
from PIL import Image
import os

def one_hot(i):
    a = np.zeros(3, 'uint8')
    a[i] = 1
    return a

data_dir = "D:\\project\\study-crolling\\data\\images\\"
nb_classes = 3 # 가지, 당근, 참외 3개의 클래스

# 데이터 개수 736개
# 사진 사이즈 100x100
result_arr = np.empty((736, 30003))

idx_start = 0

for cls, food_name in enumerate(os.listdir(data_dir)):
    image_dir = data_dir + food_name + '\\'
    file_list = os.listdir(image_dir)

    for idx, f in enumerate(file_list):
        im = Image.open(image_dir + f)
        pix = np.array(im)
        arr = pix.reshape(1, 30000)
        result_arr[idx_start + idx] = np.append(arr, one_hot(cls))
    idx_start += len((file_list))

np.save('result.npy', result_arr)