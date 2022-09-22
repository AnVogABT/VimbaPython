"""
This file is used to acquire frames using vimba cameras mono and colored.
"""


import os
import cv2
from datetime import datetime
from vimba import *


##############
# user inputs
##############

folder_path_out = r"Path of the output folder of the frames"
settings_file = r"full path of the camera settings file"
# Timeout in milliseconds of frame acquisition
# decrease this value to record faster
timeout_ms = 150
# The number of images the generator shall acquire. If limit is None,
# the generator will produce an unlimited amount of images and must be
# stopped by the user supplied code.
limit = 100000
# define the extenction of the frames
image_extension = 'bmp' # 'bmp', 'jpg'
# place the resize factor of your real time frame viewer
resize_factor_view = 5

###############
# functionality
###############

with Vimba.get_instance() as vimba:
    cams = vimba.get_all_cameras()
    with cams[0] as cam:

        # Load camera settings from file.
        cam.load_settings(settings_file, PersistType.All)

        # Aquire single frame synchronously
        frame = cam.get_frame()

        # Aquire n frames synchronously
        for frame in cam.get_frame_generator(limit=limit, timeout_ms=timeout_ms):
            frame.convert_pixel_format(PixelFormat.Mono8) # or Bgr8 for color camera

            now = datetime.now()
            timestampt = now.strftime("%Y%m%d_%H%M%S.%f")[:-3]

            output_file = os.path.join(folder_path_out, '{}.{}'.format(timestampt,image_extension))

            image = frame.as_opencv_image()
            illustrated_image = cv2.resize(image, (int(image.shape[1]/resize_factor_view), int(image.shape[0]/resize_factor_view)))
            cv2.imshow('img', illustrated_image)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
            cv2.imwrite(output_file, image)
            pass

