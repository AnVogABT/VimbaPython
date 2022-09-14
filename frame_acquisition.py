import os
import time
import cv2
from datetime import datetime
from vimba import *

# Timeout in milliseconds of frame acquisition
# decrease this value to record faster
timeout_ms = 150

# The number of images the generator shall acquire. If limit is None,
# the generator will produce an unlimited amount of images and must be
# stopped by the user supplied code.
limit = 100000

# folder_path = r"C:\Users\a.vogiatzis\Desktop\vimba_camera\2022-07-04"
folder_path_out = r"C:\Users\a.vogiatzis\Desktop\11_07_2022"

settings_file = r"C:\Users\a.vogiatzis\Desktop\11_07_2022\2022-06-28 old_camera_settings_binary.xml"

image_extension = 'bmp' # 'bmp', 'jpg'

with Vimba.get_instance() as vimba:
    cams = vimba.get_all_cameras()
    with cams[0] as cam:

        # Load camera settings from file.
        cam.load_settings(settings_file, PersistType.All)

        # Aquire single frame synchronously
        frame = cam.get_frame()

        # Aquire n frames synchronously
        for frame in cam.get_frame_generator(limit=limit, timeout_ms=timeout_ms):
            frame.convert_pixel_format(PixelFormat.Mono8) # or Bgr8 for color

            now = datetime.now()
            timestampt = now.strftime("%Y%m%d_%H%M%S.%f")[:-3]

            output_file = os.path.join(folder_path_out, '{}.{}'.format(timestampt,image_extension))

            image = frame.as_opencv_image()
            cv2.imwrite(output_file, image)
            pass

