cmake_minimum_required(VERSION 3.9)

project(make_dlls CXX CUDA)

find_package(OpenMP REQUIRED)

if(OpenMP_FOUND)
set(CMAKE_CUDA_FLAGS "${CMAKE_CUDA_FLAGS} -Xcompiler=${OpenMP_CXX_FLAGS}")
endif()

add_library(Forwarding_DLL SHARED src/Forwarding_DLL.cpp)

add_library(grav_rfi_ompcuda SHARED src/grav_rfi_ompcuda.cu)
target_link_libraries(grav_rfi_ompcuda ${CUDA_LIBRARIES})
