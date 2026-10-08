cmake_minimum_required(VERSION 3.10)
project(dashcam_streamer C)

set(CMAKE_C_STANDARD 99)

# Paths for Luckfox Pico SDK headers and libraries
# Typically set via SDK environment or passed via cmake command:
# cmake -DCMAKE_SYSROOT=/path/to/sysroot ..

include_directories(
    ${CMAKE_CURRENT_SOURCE_DIR}/include
    /usr/include/rkmedia
)

add_executable(dashcam_streamer dashcam_streamer.c)

# Link Rockchip MPI libraries and POSIX threads
target_link_libraries(dashcam_streamer
    rockchip_mpp
    rga
    pthread
    m
)
