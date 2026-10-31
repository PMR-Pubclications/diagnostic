cmake_minimum_required(VERSION 3.14)
project(DiagnosticCore VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_library(DiagnosticCore INTERFACE)
target_include_directories(DiagnosticCore INTERFACE include)

# Standalone CLI binary for running system audits on demand
add_executable(diagnostic_runner src/main.cpp)
target_link_libraries(diagnostic_runner PRIVATE DiagnosticCore)

cmake_minimum_required(VERSION 3.14)
project(DiagnosticCore VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Define the reusable interface library
add_library(DiagnosticCore INTERFACE)
target_include_directories(DiagnosticCore INTERFACE 
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:include>
)

# Standalone CLI binary for running system audits
add_executable(diagnostic_runner src/main.cpp)
target_link_libraries(diagnostic_runner PRIVATE DiagnosticCore)

# Installation targets for external linking
include(GNUInstallDirs)
install(TARGETS DiagnosticCore EXPORT DiagnosticCoreTargets
    INCLUDES DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
)
install(DIRECTORY include/ DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})

