"""
code to capture photos with the vimba camera

update the following parameters: 
    timeout_ms
    limit
    test_name
    folder_path
    
"""

# impost sys
# folder_subroutine = r'C:\Users\a.vogiatzis\Repositories\VimbaPython\vimba'
# sys.path.append(folder_subroutine)
import os
import time
import cv2
from datetime import datetime
from vimba import *

def check_folder_exists(folder_path):
    """ 
    check if folder exists and if not create it
    """

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
            
# Timeout in milliseconds of frame acquisition
# decrease this value to record faster
timeout_ms = 200

# The number of images the generator shall acquire. If limit is None,
# the generator will produce an unlimited amount of images and must be
# stopped by the user supplied code.
limit = 20

# a folder with this name will be created in the folder_path
test_name = '1145_mm_200ms_2nd_run'
# path where the frames will be stored
folder_path = r'C:\Users\a.vogiatzis\Repositories\VimbaPython\output'

#############################################################
#
#############################################################

# define the folder path where the files will be stored
folder_path_out = '{}{}/'.format(folder_path, test_name)

#check if folder exists and if not create it
check_folder_exists(folder_path_out)
            
# Synchronous grab
from vimba import *

with Vimba.get_instance() as vimba:
    cams = vimba.get_all_cameras()
    with cams[0] as cam:
        # Aquire single frame synchronously
        frame = cam.get_frame()

        # # Aquire 10 frames synchronously
        # for frame in cam.get_frame_generator(limit=10):
            
        # Aquire n frames synchronously
        # ii=0
        for frame in cam.get_frame_generator(limit=limit, timeout_ms=timeout_ms):
            frame.convert_pixel_format(PixelFormat.Mono8)
                
            now=datetime.now()
            timestampt = now.strftime("%Y%m%d_%H%M%S.%f'")[:-3]
            
            output_file = '{}frame_{}.jpg'.format(folder_path_out, timestampt)
            # output_file = '{}frame_timestampt.jpg/'.format(folder_path_out, ii)

            print(f'frame name -> {frame}')
            print(f'output file -> {output_file}')
            # visualization of the frame
            # image = frame.as_opencv_image()
            # img = cv2.resize(image, (1066, 800))
            # cv2.imshow('img', img)
            # cv2.waitKey(1000)

            cv2.imwrite(output_file, frame.as_opencv_image())
            # ii+=1
            
            pass