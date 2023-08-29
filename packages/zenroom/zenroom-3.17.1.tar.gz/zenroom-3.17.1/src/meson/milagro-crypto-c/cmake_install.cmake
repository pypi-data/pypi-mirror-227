# Install script for directory: /home/runner/work/Zenroom/Zenroom/bindings/python3/src/lib/milagro-crypto-c

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/usr/local")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "Release")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

# Set default install directory permissions.
if(NOT DEFINED CMAKE_OBJDUMP)
  set(CMAKE_OBJDUMP "/usr/bin/objdump")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE STATIC_LIBRARY FILES "/home/runner/work/Zenroom/Zenroom/bindings/python3/src/lib/milagro-crypto-c/build/lib/libamcl_core.a")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/amcl" TYPE FILE FILES
    "/home/runner/work/Zenroom/Zenroom/bindings/python3/src/lib/milagro-crypto-c/build/include/amcl.h"
    "/home/runner/work/Zenroom/Zenroom/bindings/python3/src/lib/milagro-crypto-c/build/include/arch.h"
    "/home/runner/work/Zenroom/Zenroom/bindings/python3/src/lib/milagro-crypto-c/build/include/version.h"
    "/home/runner/work/Zenroom/Zenroom/bindings/python3/src/lib/milagro-crypto-c/include/utils.h"
    "/home/runner/work/Zenroom/Zenroom/bindings/python3/src/lib/milagro-crypto-c/include/randapi.h"
    )
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/amcl" TYPE FILE FILES
    "/home/runner/work/Zenroom/Zenroom/bindings/python3/src/lib/milagro-crypto-c/build/include/config_test.h"
    "/home/runner/work/Zenroom/Zenroom/bindings/python3/src/lib/milagro-crypto-c/include/pbc_support.h"
    )
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/amcl" TYPE FILE FILES "/home/runner/work/Zenroom/Zenroom/bindings/python3/src/lib/milagro-crypto-c/include/ecdh_support.h")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE STATIC_LIBRARY FILES "/home/runner/work/Zenroom/Zenroom/bindings/python3/src/lib/milagro-crypto-c/build/lib/libamcl_curve_SECP256K1.a")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/amcl" TYPE FILE FILES
    "/home/runner/work/Zenroom/Zenroom/bindings/python3/src/lib/milagro-crypto-c/build/include/big_256_28.h"
    "/home/runner/work/Zenroom/Zenroom/bindings/python3/src/lib/milagro-crypto-c/build/include/config_big_256_28.h"
    "/home/runner/work/Zenroom/Zenroom/bindings/python3/src/lib/milagro-crypto-c/build/include/config_field_SECP256K1.h"
    "/home/runner/work/Zenroom/Zenroom/bindings/python3/src/lib/milagro-crypto-c/build/include/config_curve_SECP256K1.h"
    "/home/runner/work/Zenroom/Zenroom/bindings/python3/src/lib/milagro-crypto-c/build/include/fp_SECP256K1.h"
    "/home/runner/work/Zenroom/Zenroom/bindings/python3/src/lib/milagro-crypto-c/build/include/ecdh_SECP256K1.h"
    "/home/runner/work/Zenroom/Zenroom/bindings/python3/src/lib/milagro-crypto-c/build/include/ecp_SECP256K1.h"
    )
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE STATIC_LIBRARY FILES "/home/runner/work/Zenroom/Zenroom/bindings/python3/src/lib/milagro-crypto-c/build/lib/libamcl_curve_BLS381.a")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/amcl" TYPE FILE FILES
    "/home/runner/work/Zenroom/Zenroom/bindings/python3/src/lib/milagro-crypto-c/build/include/big_384_29.h"
    "/home/runner/work/Zenroom/Zenroom/bindings/python3/src/lib/milagro-crypto-c/build/include/config_big_384_29.h"
    "/home/runner/work/Zenroom/Zenroom/bindings/python3/src/lib/milagro-crypto-c/build/include/config_field_BLS381.h"
    "/home/runner/work/Zenroom/Zenroom/bindings/python3/src/lib/milagro-crypto-c/build/include/config_curve_BLS381.h"
    "/home/runner/work/Zenroom/Zenroom/bindings/python3/src/lib/milagro-crypto-c/build/include/fp_BLS381.h"
    "/home/runner/work/Zenroom/Zenroom/bindings/python3/src/lib/milagro-crypto-c/build/include/ecdh_BLS381.h"
    "/home/runner/work/Zenroom/Zenroom/bindings/python3/src/lib/milagro-crypto-c/build/include/ecp_BLS381.h"
    )
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE STATIC_LIBRARY FILES "/home/runner/work/Zenroom/Zenroom/bindings/python3/src/lib/milagro-crypto-c/build/lib/libamcl_pairing_BLS381.a")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/amcl" TYPE FILE FILES
    "/home/runner/work/Zenroom/Zenroom/bindings/python3/src/lib/milagro-crypto-c/build/include/fp2_BLS381.h"
    "/home/runner/work/Zenroom/Zenroom/bindings/python3/src/lib/milagro-crypto-c/build/include/fp4_BLS381.h"
    "/home/runner/work/Zenroom/Zenroom/bindings/python3/src/lib/milagro-crypto-c/build/include/fp12_BLS381.h"
    "/home/runner/work/Zenroom/Zenroom/bindings/python3/src/lib/milagro-crypto-c/build/include/ecp2_BLS381.h"
    "/home/runner/work/Zenroom/Zenroom/bindings/python3/src/lib/milagro-crypto-c/build/include/pair_BLS381.h"
    )
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE STATIC_LIBRARY FILES "/home/runner/work/Zenroom/Zenroom/bindings/python3/src/lib/milagro-crypto-c/build/lib/libamcl_bls_BLS381.a")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/amcl" TYPE FILE FILES "/home/runner/work/Zenroom/Zenroom/bindings/python3/src/lib/milagro-crypto-c/build/include/bls_BLS381.h")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pkgconfig" TYPE FILE FILES "/home/runner/work/Zenroom/Zenroom/bindings/python3/src/lib/milagro-crypto-c/build/amcl.pc")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/cmake/amcl/AMCLTargets.cmake")
    file(DIFFERENT _cmake_export_file_changed FILES
         "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/cmake/amcl/AMCLTargets.cmake"
         "/home/runner/work/Zenroom/Zenroom/bindings/python3/src/lib/milagro-crypto-c/build/CMakeFiles/Export/c2d8cd56cfa84a14e9895d8ff591d988/AMCLTargets.cmake")
    if(_cmake_export_file_changed)
      file(GLOB _cmake_old_config_files "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/cmake/amcl/AMCLTargets-*.cmake")
      if(_cmake_old_config_files)
        string(REPLACE ";" ", " _cmake_old_config_files_text "${_cmake_old_config_files}")
        message(STATUS "Old export file \"$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/cmake/amcl/AMCLTargets.cmake\" will be replaced.  Removing files [${_cmake_old_config_files_text}].")
        unset(_cmake_old_config_files_text)
        file(REMOVE ${_cmake_old_config_files})
      endif()
      unset(_cmake_old_config_files)
    endif()
    unset(_cmake_export_file_changed)
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cmake/amcl" TYPE FILE FILES "/home/runner/work/Zenroom/Zenroom/bindings/python3/src/lib/milagro-crypto-c/build/CMakeFiles/Export/c2d8cd56cfa84a14e9895d8ff591d988/AMCLTargets.cmake")
  if(CMAKE_INSTALL_CONFIG_NAME MATCHES "^([Rr][Ee][Ll][Ee][Aa][Ss][Ee])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cmake/amcl" TYPE FILE FILES "/home/runner/work/Zenroom/Zenroom/bindings/python3/src/lib/milagro-crypto-c/build/CMakeFiles/Export/c2d8cd56cfa84a14e9895d8ff591d988/AMCLTargets-release.cmake")
  endif()
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cmake/amcl" TYPE FILE FILES
    "/home/runner/work/Zenroom/Zenroom/bindings/python3/src/lib/milagro-crypto-c/build/AMCLConfig.cmake"
    "/home/runner/work/Zenroom/Zenroom/bindings/python3/src/lib/milagro-crypto-c/build/AMCLConfigVersion.cmake"
    )
endif()

if(CMAKE_INSTALL_COMPONENT)
  set(CMAKE_INSTALL_MANIFEST "install_manifest_${CMAKE_INSTALL_COMPONENT}.txt")
else()
  set(CMAKE_INSTALL_MANIFEST "install_manifest.txt")
endif()

string(REPLACE ";" "\n" CMAKE_INSTALL_MANIFEST_CONTENT
       "${CMAKE_INSTALL_MANIFEST_FILES}")
file(WRITE "/home/runner/work/Zenroom/Zenroom/bindings/python3/src/lib/milagro-crypto-c/build/${CMAKE_INSTALL_MANIFEST}"
     "${CMAKE_INSTALL_MANIFEST_CONTENT}")
