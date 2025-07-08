cmake_minimum_required(VERSION 3.15)
project(phantomroll)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# TDLib JSON include
include_directories(${CMAKE_SOURCE_DIR}/td/build)
include_directories(${CMAKE_SOURCE_DIR}/td)
link_directories(${CMAKE_SOURCE_DIR}/td/build)

# Include local headers
include_directories(${CMAKE_SOURCE_DIR}/include)

# Add subdirectories
add_subdirectory(src)

# Copy config file to build directory (for runtime access)
configure_file(${CMAKE_SOURCE_DIR}/config/tdlib_config.json ${CMAKE_BINARY_DIR}/config/tdlib_config.json COPYONLY)

# PhantomRoll final binary
add_executable(phantomroll main.cpp)

# OS-specific platform logic
if(WIN32)
    message(STATUS "Configuring for Windows")
    target_link_libraries(phantomroll
        core
        tdjson
        ws2_32
    )
elseif(APPLE)
    message(STATUS "Configuring for macOS")
    target_link_libraries(phantomroll
        core
        tdjson
    )
elseif(UNIX)
    message(STATUS "Configuring for Linux")
    target_link_libraries(phantomroll
        core
        tdjson
        pthread
    )
else()
    message(FATAL_ERROR "Unsupported platform")
endif()
