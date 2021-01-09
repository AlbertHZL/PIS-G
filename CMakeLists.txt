cmake_minimum_required(VERSION 3.19 FATAL_ERROR)

project(make_dlls CXX CUDA)

find_package(CUDA REQUIRED)
find_package(OpenMP REQUIRED)

if(OpenMP_FOUND)
set(CMAKE_CUDA_FLAGS "${CMAKE_CUDA_FLAGS} -Xcompiler=${OpenMP_CXX_FLAGS}") 
endif()

add_library(Forwarding_DLL SHARED Forwarding_DLL.cpp)

add_library(grav_rfi_ompcuda SHARED grav_rfi_ompcuda.cu grav_rfi_ompcuda.h)
target_include_directories(grav_rfi_ompcuda PRIVATE $ENV{NVCUDASAMPLES_ROOT}/common/inc)

target_link_directories(grav_rfi_ompcuda PRIVATE $ENV{CUDA_PATH}/lib/x64)
target_link_libraries(grav_rfi_ompcuda cudart.lib)
