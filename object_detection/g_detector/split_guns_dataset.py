import re
import os
import glob
import shutil
import random

image_path = '/mnt/dl/data/guns/gun_images/'
annon_path = '/mnt/dl/data/guns/gun_labels/'

image_fls = os.listdir(image_path)
annon_fls = os.listdir(image_path)

def remove_ext(fls):
    return [re.sub(".jpg|.xml", "", s) for s in fls]

print(set(remove_ext(image_fls)) - set(remove_ext(annon_fls)))
print(set(remove_ext(annon_fls)) - set(remove_ext(image_fls)))

print("Images: {}, Annotations: {}".format(len(image_fls), len(annon_fls)))

def shuffle_list(*ls):
  l = list(zip(*ls))
  random.shuffle(l)
  return zip(*l)

image_fls, annon_fls = shuffle_list(image_fls, annon_fls)

path = '/mnt/dl/data/guns/'

for i,f in enumerate(remove_ext(image_fls)):
    if i <= 800:
        dataset = 'train'
    else:
        dataset = 'test'
    shutil.copyfile(os.path.join(path, "gun_images", f + '.jpg'), os.path.join(path, dataset, f + '.jpg'))
    shutil.copyfile(os.path.join(path, "gun_labels", f + '.xml'), os.path.join(path, dataset, f + '.xml'))
