#
# Usage:
# 
# add_test(NAME compress_block_size_1
#     COMMAND ${CMAKE_COMMAND}
#     -DPROGRAM=testprogs # program name
# 	  -DLOGFILE=test.log  # optional
#     -DCMAKE_SYSTEM_NAME=${CMAKE_SYSTEM_NAME}
#     -P ${CMAKE_CURRENT_SOURCE_DIR}/runtest.cmake)
#
######################################

macro(_log msg)
  set(_LOGMSGS "${_LOGMSGS}\n${msg}")
endmacro()

set(_names ${PROGRAM})
if(CMAKE_SYSTEM_NAME STREQUAL Windows)
  set(_names ${_names} ${PROGRAM}.exe)
endif()


find_file(_program NAMES ${_names}
          PATHS ${CMAKE_CURRENT_BINARY_DIR} 
          ${CMAKE_CURRENT_BINARY_DIR}/bin
          ${CMAKE_CURRENT_BINARY_DIR}/Debug
          ${CMAKE_CURRENT_BINARY_DIR}/Release
          NO_DEFAULT_PATH )
if(${_program} STREQUAL _program-NOTFOUND)
  _log("Could not find program : ${PROGRAM}")
else()
  _log("found program : ${_program}")
  _log("BIN_DIRS_LIBTASN1=${BIN_DIRS_LIBTASN1}")
  _log("BIN_DIRS_ZLIB=${BIN_DIRS_ZLIB}")
  #--------------------------------------#
  #   Your test here                     #
  #--------------------------------------#
  set(_RESULT 0)

  execute_process (COMMAND  ${CMAKE_COMMAND} -E env PATH=${BIN_DIRS_LIBTASN1}\;${BIN_DIRS_ZLIB} ${_program} 
                  RESULT_VARIABLE _RESULT
                  WORKING_DIRECTORY ${TEST_DIR} )


endif()		  


if(LOGFILE )
   _log("result : ${_RESULT}")
   file(WRITE ${LOGFILE} ${_LOGMSGS})
endif()

if(NOT _RESULT EQUAL 0)
  message (SEND_ERROR "exec program failed")
endif()