CXX = g++
CXXFLAGS = -D_UNIX_ -D_LINUX_ -I/opt/workswell/wic_sdk/include -I/opt/pleora/ebus_sdk/Ubuntu-x86_64/include -O0 -g3 -Wall -fPIC -std=c++11
LDFLAGS = -shared -L/opt/workswell/wic_sdk/lib -L/opt/pleora/ebus_sdk/Ubuntu-x86_64/lib \
          -lWIC_SDK -lWT-lib -ljpeg -lPvBase -lPvDevice -lPvBuffer -lPvGenICam -lPvTransmitter -lPvVirtualDevice -lPvAppUtils -lPvPersistence -lPvSerial -lPvStream -pthread
TARGET = libTau.so
SRCS = libTau.cpp

$(TARGET): $(SRCS)
	$(CXX) $(CXXFLAGS) -o $(TARGET) $(SRCS) $(LDFLAGS)

.PHONY: clean
clean:
	rm -f $(TARGET)
