#include <iostream>
#include <vector>
#include <tuple>
#include "CameraCenter.h"
#include "libTau.h"


extern "C" {
    Camera* open_camera(const char* licensePath) {
        CameraCenter* cameras = new CameraCenter(licensePath);
        std::cout << "Number of detected cameras: " << cameras->getCameras().size() << std::endl;

        if (cameras->getCameras().size() == 0) {
            std::cout << "No camera found!" << std::endl;
            exit(-1);
        }

        Camera* camera = cameras->getCameras().at(0);
        if (camera->connect() != 0) {
            std::cout << "Error connecting camera!" << std::endl;
            exit(-1);
        }

        camera->startAcquisition();
        return camera;
    }


    void close_camera(Camera* cam) {
        if (cam) {
            cam->stopAcquisition();
            cam->disconnect();
            delete cam;
        }
    }

    void performFFC(Camera* cam) {
        if (cam) {
            std::cout << "Performing flat field correction (FFC)..." << std::endl;
            cam->getSettings()->doFFC();
            std::cout << "FFC completed!" << std::endl;
        }
    }

    void changeMode(Camera* cam, int mode) {
        if (cam) {
            if (mode == 1) {
                std::cout << "Changing mode to Low mode." << std::endl;
                cam->getSettings()->setRangeMode(CameraSerialSettings::RangeModes::Low);
                if (cam->getSettings()->getRangeMode() == CameraSerialSettings::RangeModes::Low) {
                    std::cout << "You are in Low mode!!" << std::endl;
                }
            } else if (mode == 2) {
                std::cout << "Changing mode to Middle mode." << std::endl;
                cam->getSettings()->setRangeMode(CameraSerialSettings::RangeModes::Middle);
                if (cam->getSettings()->getRangeMode() == CameraSerialSettings::RangeModes::Middle) {
                    std::cout << "You are in Middle mode!!" << std::endl;
                }
            } else {
                std::cout << "Out of range!." << std::endl;
            }

            std::cout << "Check if camera is capable of radiometry (temperature linear data): " << std::endl;
            cam->getSettings()->doFFC();
            std::cout << "Mode change completed!" << std::endl;
        }
    }

    CaptureResult get_raw_capture(Camera* cam) {
        CaptureResult result = {0, 0, nullptr};
        if (cam) {
            uint16_t* buffer = (uint16_t*)cam->retrieveBuffer();
            if (buffer == nullptr) {
                std::cerr << "Error: Buffer retrieval failed!" << std::endl;
                return result;
            }

            result.width = cam->getSettings()->getResolutionX();
            result.height = cam->getSettings()->getResolutionY();
            result.data = buffer;
        }
        cam->releaseBuffer();
        return result;
    }

    TempCaptureResult get_temp_capture(Camera* cam) {
        TempCaptureResult result = {0, 0, nullptr};
        if (cam) {
            uint16_t* buffer = (uint16_t*)cam->retrieveBuffer();
            if (buffer == nullptr) {
                std::cerr << "Error: Buffer retrieval failed!" << std::endl;
                return result;
            }

            int width = cam->getSettings()->getResolutionX();
            int height = cam->getSettings()->getResolutionY();
            result.width = width;
            result.height = height;
            result.data = new double[width * height];

            for (int i = 0; i < width * height; i++) {
                result.data[i] = cam->calculateTemperatureC(buffer[i]);
            }
        }
        cam->releaseBuffer();
        return result;
    }

    void release_buffer(Camera* cam) {
        if (cam) {
            cam->releaseBuffer();
        }
    }
}
