import os
import glob
import shutil
import sys
from pathlib import Path
import random

os.mkdir('data_samples/')
os.mkdir('data_samples/synthetic')
os.mkdir('data_samples/synthetic/mars')
os.mkdir('data_samples/synthetic/mars/train/')
os.mkdir('data_samples/synthetic/mars/test/')
os.mkdir('data_samples/synthetic/mars/val/')
print('deep_surfels directories created')

ds_dir = [s for s in os.listdir() if 'data_samples' in s][0]
syn_dir = os.path.join(ds_dir,[s for s in os.listdir(ds_dir) if 'synthetic' in s][0])
mars_dir = os.path.join(syn_dir,[s for s in os.listdir(syn_dir) if 'mars' in s][0])
train_dir = os.path.join(mars_dir,[s for s in os.listdir(mars_dir) if 'train' in s][0])
test_dir = os.path.join(mars_dir,[s for s in os.listdir(mars_dir) if 'test' in s][0])
val_dir = os.path.join(mars_dir,[s for s in os.listdir(mars_dir) if 'val' in s][0])

def set_staging():
    param_sets = {}
    for filename in glob.glob(os.path.join('converted', '*_params.json')):
        p = Path(filename)
        f = Path(filename).name
        i = f.split('_')[0]
        param_sets[i] = []
        param_sets[i].append(str(p))

    for filename in glob.glob(os.path.join('converted', '*_img.png')):
        p = Path(filename)
        f = Path(filename).name
        i = f.split('_')[0]
        param_sets[i].append(str(p))

    for filename in glob.glob(os.path.join('converted', '*_img.exr')):
        p = Path(filename)
        f = Path(filename).name
        i = f.split('_')[0]
        param_sets[i].append(str(p))

    for filename in glob.glob(os.path.join('converted', '*_depth.exr')):
        p = Path(filename)
        f = Path(filename).name
        i = f.split('_')[0]
        param_sets[i].append(str(p))
    print("{} sets in directory.".format(len(param_sets)))
    return(param_sets)

def set_creation(param_sets):
    kept_sets = {}
    for (key, value) in param_sets.items():
        if len(value) == 4:
            kept_sets[key] = value
    print("{} sets have all component files.".format(len(kept_sets)))
    return kept_sets

def train_test_split(kept_sets,ratio):
    keys = list(kept_sets.keys())
    train_test_split = int(ratio*len(kept_sets))
    test = keys[0:train_test_split]
    train = keys[train_test_split:]

    for i in test:
        test_objs = kept_sets[i]
        for j in test_objs:
            relative_path = 'converted'
            file_name = os.path.relpath(j,relative_path)
            shutil.move(j, os.path.join(test_dir,file_name))
    print("Test split created.")

    for i in train:
        train_objs = kept_sets[i]
        for j in train_objs:
            relative_path = 'converted'
            file_name = os.path.relpath(j,relative_path)
            shutil.move(j, os.path.join(train_dir,file_name))
    print("Train split created.")

while True:
    try:
        number1 = int(input('Input percent of data for testing: '))
        if number1 < 1 or number1 > 30:
            raise ValueError
        break
    except ValueError:
        print("Invalid. Input from 1-30.")

sets = set_staging()
sets = set_creation(sets)
train_test_split(sets,number1/100)
