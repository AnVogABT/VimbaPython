# # Synchronous grab
# from vimba import *
# import cv2
# with Vimba.get_instance() as vimba:
#     cams = vimba.get_all_cameras()
#     with cams[0] as cam:
#         # Aquire single frame synchronously
#         frame = cam.get_frame()
#         image = frame.as_opencv_image()
#         print(f'shape -> {image.shape}')
#         img = cv2.resize(image, (1066, 800))
#         cv2.imshow('img', img)
#         cv2.waitKey(30)
#         # cv2.imwrite(r'C:\Users\a.vogiatzis\Repositories\VimbaPython\trouts', img)
#         # Aquire 10 frames synchronously
#         for frame in cam.get_frame_generator(limit=10):
#             pass


from vimba import *
import cv2

with Vimba.get_instance() as vimba:
    cams = vimba.get_all_cameras()
    with cams[0] as cam:
        exposure_time = cam.ExposureTime

        time = exposure_time.get()

        inc = exposure_time.get_increment()

        print(f'The old exposure tiime -> {exposure_time.get()}')
        
        exposure_time.set(max(162.465, time + inc))
        exposure_time.set(1000)

        print(f'The new exposure tiime -> {exposure_time.get()}')
        # Aquire single frame synchronously
        frame = cam.get_frame()
        image = frame.as_opencv_image()
        print(f'shape -> {image.shape}')
        img = cv2.resize(image, (1066, 800))
        cv2.imshow('img', img)
        cv2.waitKey(3000)
