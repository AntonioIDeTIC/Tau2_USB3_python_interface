import ctypes
import os
import time
import numpy as np
import cv2
import matplotlib

def apply_colormap(frame, cmap):
    frame = np.asarray(normalize(frame, np.min(frame), np.max(frame), 0, 255), dtype=np.uint8)
    frame = clahe.apply(frame)
    frame = np.asarray(normalize(frame, np.min(frame), np.max(frame), 0, 1.0), dtype=np.float32)

    color = matplotlib.colormaps.get_cmap(cmap)
    frame = np.asarray(color(frame) * 255, dtype=np.uint8) 
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return frame
    
class TauCamera:
    def __init__(self, license_path):
        # Load the shared library
        lib_path = os.path.abspath("libTau.so")
        self.libTau = ctypes.CDLL(lib_path)
        
        # Define Camera class (pointer type)
        class Camera(ctypes.Structure):
            pass
        
        self.CameraPointer = ctypes.POINTER(Camera)
        
        # Define CaptureResult struct
        class CaptureResult(ctypes.Structure):
            _fields_ = [
                ("width", ctypes.c_int),
                ("height", ctypes.c_int),
                ("data", ctypes.POINTER(ctypes.c_uint16))
            ]
        
        self.CaptureResult = CaptureResult
        
        # Define TempCaptureResult struct
        class TempCaptureResult(ctypes.Structure):
            _fields_ = [
                ("width", ctypes.c_int),
                ("height", ctypes.c_int),
                ("data", ctypes.POINTER(ctypes.c_double))
            ]
        
        self.TempCaptureResult = TempCaptureResult
        
        # Define function argument and return types
        self.libTau.open_camera.argtypes = [ctypes.c_char_p]
        self.libTau.open_camera.restype = self.CameraPointer

        self.libTau.performFFC.argtypes = [self.CameraPointer]
        self.libTau.performFFC.restype = None

        self.libTau.changeMode.argtypes = [self.CameraPointer, ctypes.c_int]
        self.libTau.changeMode.restype = None

        self.libTau.close_camera.argtypes = [self.CameraPointer]
        self.libTau.close_camera.restype = None

        self.libTau.get_raw_capture.argtypes = [self.CameraPointer]
        self.libTau.get_raw_capture.restype = self.CaptureResult

        self.libTau.get_temp_capture.argtypes = [self.CameraPointer]
        self.libTau.get_temp_capture.restype = self.TempCaptureResult

        self.libTau.release_buffer.argtypes = [self.CameraPointer]
        self.libTau.release_buffer.restype = None
        
        # Open the camera
        self.camera = self.libTau.open_camera(license_path)
        if not self.camera:
            raise RuntimeError("Failed to open camera")
        self.libTau.performFFC(self.camera)  # Perform Flat Field Correction
    
    def capture_frame(self):
        raw_capture = self.libTau.get_raw_capture(self.camera)
        if raw_capture.data:
            width = raw_capture.width
            height = raw_capture.height
            raw_data = np.ctypeslib.as_array(raw_capture.data, shape=(height, width))
            return raw_data
        return None
    
    def release(self):
        self.libTau.release_buffer(self.camera)
        self.libTau.close_camera(self.camera)

def main():
    license_path = b"/opt/workswell/wic_sdk/sample/src/"  # Provide the correct path to the license
    camera = TauCamera(license_path)

    starttime = time.time()  # Record the start time

    try:
        while True:
            currtime = time.time()  # Get the current time

            if currtime - starttime >= 0.1:  # Check if 0.1 seconds have passed
                raw_data = camera.capture_frame()  # Capture a frame

                if raw_data is not None:
                    # Process and display the captured frame
                    tau_image = np.asarray(raw_data, dtype=np.uint16)
                    tau_image = apply_plasma_colormap(tau_image)
                    visual_tau_pic = cv2.resize(tau_image, (640, 480))

                    cv2.imshow("Tau Frame", visual_tau_pic)  # Display the frame
                    key = cv2.waitKey(1) & 0xFF  # Wait for a key press
                    if key == ord('q'):  # Break the loop if 'q' is pressed
                        break

                    starttime = currtime  # Reset the start time
                else:
                    break

    except KeyboardInterrupt:
        pass  # Handle keyboard interrupt gracefully
    finally:
        cv2.destroyAllWindows()  # Destroy all OpenCV windows
        camera.release()  # Release the camera resources

if __name__ == "__main__":
    main()  # Run the main function if this script is executed directly

