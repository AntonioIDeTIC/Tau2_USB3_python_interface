import matplotlib
import numpy as np
import cv2

def normalize(image, from_min, from_max, to_min, to_max):
    from_range = from_max - from_min
    to_range = to_max - to_min
    scaled = np.array((image - from_min) / float(from_range), dtype= float)
    return np.asarray(to_min + (scaled * to_range))
    
def apply_colormap(frame, cmap, clahe):
    frame = np.asarray(normalize(frame, np.min(frame), np.max(frame), 0, 255), dtype=np.uint8)
    frame = clahe.apply(frame)
    frame = np.asarray(normalize(frame, np.min(frame), np.max(frame), 0, 1.0), dtype=np.float32)

    color = matplotlib.colormaps.get_cmap(cmap)
    frame = np.asarray(color(frame) * 255, dtype=np.uint8) 
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return frame
