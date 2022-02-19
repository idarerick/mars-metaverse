purpose of dsurfconvert script - to take mars mini yard files and convert them into the appropriate extensions and parameters for deepsurfels
purpose of dsurfmovefiles script - to take the converted files from the above script, and move them into appropriate directories for deepsurfels

~~~ how to use the dsurf scripts ~~~
1. download mars mini yard zip from google drive
2. extract the data folder (mars-yard-mini-2021_10_21_14_59_38-20220203T233426Z-001)
3. move the scripts and the data folder into the same directory together (AKA do not put the scripts IN the mars data folder)
4. in terminal, run `python dsurfconvert.py`, it will tell you the status of the script in terminal
5. in terminal, run `python dsurfmovefiles.py`, it will ask you for % of data to use for testing (aka if using 80/20 train test split, input 20). after, it will tell you the status of the script in terminal

purpose of wget script - to pull NAVCAM SOLs from JPL's website
~~~ how to use wget script ~~~
1. in terminal, run `python wgetscript.py` in whichever directory you want the files to be dumped
2. it will ask for input: (1) or (2) for navcam, or (3) for helicam
3. it will output the min SOL and max SOL number for that server. input the lower and upper bound of the SOLs you want. can only pull 5 SOLs at a time.


~~~ deepsurfels windows installation issues ~~~

>>>>follow deep_surfels readme where you can<<<<

after activating deep_surfels env and attempting to run deterministic fusion, had to do some installs before it worked

conda install configargparse
conda install -c pytorch pytorch
pip install trimesh
pip install opencv-python
pip install tensorboard

conda env config vars set OPENCV_IO_ENABLE_OPENEXR=1
conda deactivate
conda activate deep_surfels
conda install -c anaconda cudatoolkit (?)

to process new data - follow readme in data_prep folder:
pip install connected-components-3d
conda install Cython
pip install git+https://github.com/markomih/distance-transform
```bash
mkdir external
cd external && git clone https://github.com/markomih/voxel_fusion && cd voxel_fusion
mkdir build && cd build
cmake ..
make 

then run from_depth_frames.py in (data_prep folder I think?)

when running fusion/training,
change --max-iterations if you don't want this to run for literal years
