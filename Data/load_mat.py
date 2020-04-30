import scipy.io as scio
import os

path = '/home/night/Datasets/face/300W/AFLW2000-3D/AFLW2000'
file_list = os.listdir(path)
mat_file_list = []
for file in file_list:
    if file.endswith('.mat'):
        mat_file_list.append(file)

for file in mat_file_list:
    data = scio.loadmat(os.path.join(path, file))
    print(data.keys)
