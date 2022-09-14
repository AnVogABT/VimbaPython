"""
code to capture photos with the vimba camera
update the following parameters:
    timeout_ms
    limit
    test_name
    folder_path

"""

import os
import time
import cv2
from datetime import datetime
from vimba import *
import shutil

def check_folder_exists(folder_path):
    """
    check if folder exists and if not create it
    """

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

# Timeout in milliseconds of frame acquisition
# decrease this value to record faster
timeout_ms = 400 # 150 -> binary, 400 -> colored

# The number of images the generator shall acquire. If limit is None,
# the generator will produce an unlimited amount of images and must be
# stopped by the user supplied code.
limit = 1000000

# # a folder with this name will be created in the folder_path
# test_name = '2022-03-31 test22'
# path where the frames will be stored
folder_path = r"C:\Users\a.vogiatzis\Desktop\2022-07-26 DC2 Fokker Park\mono"

settings_file = r"C:\Users\a.vogiatzis\Desktop\2022-07-26 DC2 Fokker Park\2022-07-11 new_camera_settings_binary.xml"
# settings_file = r"C:\Users\a.vogiatzis\Desktop\2022-07-26 DC2 Fokker Park\2022-07-11 new camera settings color.xml"
# settings_file = r"C:\Users\a.vogiatzis\Desktop\2022-07-26 DC2 Fokker Park\2022-07-25 camera settings color.xml"

image_extension = 'bmp' # 'bmp', 'jpg'

# for visualization of the acquisitions on the fly
resize_factor = 5
#############################################################
#
#############################################################

# Synchronous grab
with Vimba.get_instance() as vimba:
    cams = vimba.get_all_cameras()
    with cams[0] as cam:

        # Load camera settings from file.
        cam.load_settings(settings_file, PersistType.All)

        # Aquire single frame synchronously
        frame = cam.get_frame()

        exposure_time = cam.ExposureTime.get()
        print('cam.GainAuto', cam.GainAuto)

        gain_value = cam.Gain.get()

        start_time = datetime.now()
        start_time_formatted = start_time.strftime("%Y%m%d_%H%M%S")

        # define the folder path where the files will be stored
        folder_path_out = os.path.join(folder_path, start_time_formatted)

        #check if folder exists and if not create it
        check_folder_exists(folder_path_out)

        # copy the camera settings file to the output folder where the images will be stored
        shutil.copyfile(settings_file, os.path.join(folder_path_out, os.path.basename(settings_file)))

        # Aquire n frames synchronously
        ii=0
        for frame in cam.get_frame_generator(limit=limit, timeout_ms=timeout_ms):
            frame.convert_pixel_format(PixelFormat.Mono8)
            # frame.convert_pixel_format(PixelFormat.Bgr8)

            if ii > 0:
                dt = datetime.now() - now
                # print(f"Photo: {ii+1}/{limit} - Recording speed: {1/dt.total_seconds():.2f} photos/s - Gain value: {gain_value} [dB] - Exposure time: {exposure_time} [μs]")

            now=datetime.now()
            timestampt = now.strftime("%Y%m%d_%H%M%S.%f")[:-3]

            output_file = os.path.join(folder_path_out, '{}_EXP_{}_GAIN_{}.{}'.format(timestampt, exposure_time, gain_value, image_extension))
            # output_file = '{}frame_timestampt.jpg/'.format(folder_path_out, ii)

            image = frame.as_opencv_image()
            # print("image.shape", image.shape)
            image_copy = cv2.resize(image, (int(image.shape[1]/resize_factor), int(image.shape[0]/resize_factor)))
            cv2.imshow('img', image_copy)
            # cv2.waitKey(0)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

            cv2.imwrite(output_file, image)

            ii+=1
            pass

cv2.destroyAllWindows()