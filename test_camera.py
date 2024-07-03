import ctypes
import os
import utils
import time
import numpy as np
import cv2

# Load the shared library
lib_path = os.path.abspath("libTau.so")
libTau = ctypes.CDLL(lib_path)

# Define Camera class (pointer type)
class Camera(ctypes.Structure):
    pass

CameraPointer = ctypes.POINTER(Camera)

# Define CaptureResult struct
class CaptureResult(ctypes.Structure):
    _fields_ = [
        ("width", ctypes.c_int),
        ("height", ctypes.c_int),
        ("data", ctypes.POINTER(ctypes.c_uint16))
    ]

# Define TempCaptureResult struct
class TempCaptureResult(ctypes.Structure):
    _fields_ = [
        ("width", ctypes.c_int),
        ("height", ctypes.c_int),
        ("data", ctypes.POINTER(ctypes.c_double))
    ]

# Define functions

# open_camera function
libTau.open_camera.argtypes = [ctypes.c_char_p]
libTau.open_camera.restype = CameraPointer

# performFFC function
libTau.performFFC.argtypes = [CameraPointer]
libTau.performFFC.restype = None

# changeMode function
libTau.changeMode.argtypes = [CameraPointer, ctypes.c_int]
libTau.changeMode.restype = None

# close_camera function
libTau.close_camera.argtypes = [CameraPointer]
libTau.close_camera.restype = None

# get_raw_capture function
libTau.get_raw_capture.argtypes = [CameraPointer]
libTau.get_raw_capture.restype = CaptureResult

# get_temp_capture function
libTau.get_temp_capture.argtypes = [CameraPointer]
libTau.get_temp_capture.restype = TempCaptureResult

# release_buffer function
libTau.release_buffer.argtypes = [CameraPointer]
libTau.release_buffer.restype = None

license_path = b"/opt/workswell/wic_sdk/sample/src/"  # Provide the correct path to the license
camera = libTau.open_camera(license_path)

libTau.performFFC(camera)

starttime = time.time()

while True:
    try:
        currtime = time.time()
        
        if currtime - starttime >=  0.1:            

            raw_capture = libTau.get_raw_capture(camera)
            
            if raw_capture.data:
                width = raw_capture.width
                height = raw_capture.height
                raw_data = [raw_capture.data[i] for i in range(width * height)]
                
                tau_image = np.asarray(raw_data, dtype = np.uint16).reshape(height, width)
                tau_image = utils.apply_plasma_colormap(tau_image)
                visual_tau_pic = cv2.resize(tau_image, (640, 480))

                cv2.imshow("Tau Frame", visual_tau_pic)
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
                starttime = currtime
            else:
                break
    
    except KeyboardInterrupt:
        break

cv2.destroyAllWindows()
# Release buffer
print("Releasing buffer")
libTau.release_buffer(camera)
# Close the camera
print("Closing camera")
libTau.close_camera(camera)





