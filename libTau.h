// camera_functions.h
#ifndef CAMERA_FUNCTIONS_H
#define CAMERA_FUNCTIONS_H

#ifdef __cplusplus
extern "C" {
#endif

struct CaptureResult {
    int width;
    int height;
    uint16_t* data;
};

struct TempCaptureResult {
    int width;
    int height;
    double* data;
};

Camera* open_camera(const char* licensePath);
void delete_camera(Camera* cam);
void performFFC(Camera* cam);
void changeMode(Camera* cam, int mode);
CaptureResult get_raw_capture(Camera* cam);
TempCaptureResult get_temp_capture(Camera* cam);
void release_buffer(Camera* cam);

#ifdef __cplusplus
}
#endif

#endif // CAMERA_FUNCTIONS_H
