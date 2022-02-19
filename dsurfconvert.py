import json
import os
import glob
import numpy as np
from pathlib import Path
from PIL import Image
import sys
from sys import stdout
import shutil

cwd = os.getcwd()
select_dir = ['mars-yard']
mars_dir = [s for s in os.listdir() if any(xs in s for xs in select_dir)][0]

yard_dir = [s for s in os.listdir(mars_dir) if any(xs in s for xs in select_dir)][0]
mars_yard_dir = os.path.join(mars_dir,yard_dir)

if not os.path.exists('converted'):
    os.mkdir('converted')
    print("converted/ directory created")
else:
    print("converted/ directory exists already.")

conv_dir = 'converted'

json_dir_size = len(glob.glob(os.path.join(mars_yard_dir, 'frame_*.json')))
jpg_dir_size = len(glob.glob(os.path.join(mars_yard_dir, 'frame_*.jpg')))
conf_dir_size = len(glob.glob(os.path.join(mars_yard_dir, 'conf_*.png')))
depth_dir_size = len(glob.glob(os.path.join(mars_yard_dir, 'depth_*.png')))

# convert JSONs
def json_to_json():
    enum = 0
    for filename in glob.glob(os.path.join(mars_yard_dir, 'frame_*.json')):
        f = Path(filename).name
        i = f.split('.')[0]
        j = i.split('_')[1]
        json_name = str(int(j)) + '_params.json'
        json_dir = os.path.join(conv_dir,json_name)
        converted = {}
        with open(filename, encoding='utf-8', mode='r') as currentFile:
            data=currentFile.read().replace('\n', '')
            intrinsics = json.loads(data)["intrinsics"]
            cameraPoseARFrame = json.loads(data)["cameraPoseARFrame"]
            projectionMatrix = json.loads(data)["projectionMatrix"]
            converted["K"] = np.reshape(intrinsics,(3, 3)).tolist()
            converted["RT"] = np.reshape(cameraPoseARFrame,(4, 4)).tolist()
            converted["P"] = np.reshape(projectionMatrix[:-4],(3,4)).tolist()
            data = json.dumps(converted)
            # enum = enum + 1
            # print("{}/{} JSON files converted.".format(enum1,json_dir_size),sep=' ',end='\r')
        with open(json_dir, 'w') as outfile:
            try:
                outfile.write(data)
                enum = enum + 1
                print("{}/{} JSON files converted to DeepSurfels parameters.".format(enum,json_dir_size),sep=' ',end='\r')
            except:
                print("{} JSON conversion failed.".format(f))
    print(f"\n")
    print("JSON conversion finished.")
    print(f"\n")

# convert JPGs
def jpg_to_png():
    enum =0
    for filename in glob.glob(os.path.join(mars_yard_dir, 'frame_*.jpg')):
        f = Path(filename).name
        i = f.split('.')[0]
        j = i.split('_')[1]
        jpg_dir = str(i) + '.jpg'
        png_dir = str(int(j)) + '_img.png'
        jpg_full_dir = os.path.join(mars_yard_dir,jpg_dir)
        png_full_dir = os.path.join(conv_dir,png_dir)

        try:
            img = Image.open(jpg_full_dir)
            try:
                img.save(png_full_dir)
                enum = enum + 1
                print("{}/{} JPG files converted to PNG.".format(enum,jpg_dir_size),sep=' ',end='\r')
            except:
                print("{} image conversion failed.".format(jpg_full_dir))
        except:
            print("{} image opening failed.".format(f))
    print(f"\n")
    print("JPG to PNG conversion finished.")
    print(f"\n")

# conf to exr
def conf_png_to_exr():
    enum = 0
    for filename in glob.glob(os.path.join(mars_yard_dir, 'conf_*.png')):
        f = Path(filename).name
        i = f.split('.')[0]
        j = i.split('_')[1]
        exr_dir = str(int(j)) + '_img.exr'
        png_full_dir = os.path.join(mars_yard_dir,f)
        exr_full_dir = os.path.join(conv_dir, exr_dir)
        try:
            shutil.copy(png_full_dir, exr_full_dir)
            enum = enum + 1
            print("{}/{} Conf PNG files converted to PNG.".format(enum,conf_dir_size),sep=' ',end='\r')
        except:
            print("{} conversion failed.".format(f))
    print(f"\n")
    print("Conf PNG to EXR conversion finished.")
    print(f"\n")

# depth to exr
def depth_png_to_exr():
    enum = 0
    for filename in glob.glob(os.path.join(mars_yard_dir, 'depth_*.png')):
        f = Path(filename).name
        i = f.split('.')[0]
        j = i.split('_')[1]
        exr_dir = str(int(j)) + '_depth.exr'
        png_full_dir = os.path.join(mars_yard_dir,f)
        exr_full_dir = os.path.join(conv_dir, exr_dir)
        try:
            shutil.copy(png_full_dir, exr_full_dir)
            enum = enum + 1
            print("{}/{} Depth PNG files converted to PNG.".format(enum,depth_dir_size),sep=' ',end='\r')
        except:
            print("{} conversion failed.".format(f))
    print(f"\n")
    print("Depth PNG to EXR conversion finished.")
    print(f"\n")

json_to_json()
jpg_to_png()
conf_png_to_exr()
depth_png_to_exr()

print(f"\n")

print("deepsurfels conversion script finished.")
