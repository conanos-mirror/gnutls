cmake_minimum_required (VERSION 3.1)
project (GnuTLS C)
set (MAJOR_VERSION 3)
set (MINOR_VERSION 5)
set (VERSION_PATCH 19)
set (VERSION ${MAJOR_VERSION}.${MINOR_VERSION}.${VERSION_PATCH})

OPTION(ENABLE_UNIT_TESTS "enable test ..." ON)

if(NOT GNUTLS_PROJECT_DIR)
  set(GNUTLS_PROJECT_DIR ${CMAKE_CURRENT_SOURCE_DIR}/gnutls-${VERSION})
endif()
message(STATUS "source : ${GNUTLS_PROJECT_DIR}")
include(cmake/conanos.cmake)

foreach(name unictype uninorm unistr unitypes)
  configure_file(${GNUTLS_PROJECT_DIR}/lib/unistring/${name}.in.h
                 ${GNUTLS_PROJECT_DIR}/lib/unistring/${name}.h @ONLY)
endforeach()               
  configure_file(${GNUTLS_PROJECT_DIR}/gl/alloca.in.h
                 ${GNUTLS_PROJECT_DIR}/gl/alloca.h @ONLY)

if(MSVC)
  string(CONCAT DEFINE_SSIZE_T 
         "#include <sys/types.h>\n"
         "#include <basetsd.h>\n"
         "typedef SSIZE_T ssize_t;\n")
         
  string(CONCAT  DEFINE_IOVEC_T 
         "typedef struct {\n"
         "  void *iov_base;\n"
         "  size_t iov_len;\n"
         "} giovec_t;\n")
  
  configure_file(${GNUTLS_PROJECT_DIR}/lib/includes/gnutls/gnutls.h.in
                 ${GNUTLS_PROJECT_DIR}/lib/includes/gnutls/gnutls.h @ONLY)
endif() 

add_definitions(-DHAVE_CONFIG_H
				#-DHAVE_LIBNETTLE
				#-DHAVE_SYS_SOCKET_H
				#-D_GL_INLINE_HEADER_BEGIN=
				#-D_GL_INLINE_HEADER_END=
				#-D_GL_EXTERN_INLINE=inline
				#-D_GL_INLINE=inline
				#-D_GL_ATTRIBUTE_PURE=
				#-DENABLE_OPENPGP
				)

set(lib_sub_folders unistring system openpgp opencdk 
      #nettle minitasn1
      extras ext auth algorithms 
      accelerated accelerated/x86 x509)

include_directories(${GNUTLS_PROJECT_DIR}
    ${GNUTLS_PROJECT_DIR}/lib	
	${GNUTLS_PROJECT_DIR}/lib/includes	
	${CMAKE_CURRENT_BINARY_DIR}
	${CMAKE_CURRENT_BINARY_DIR}/lib	
	${CMAKE_CURRENT_BINARY_DIR}/lib/includes	
	${GNUTLS_PROJECT_DIR}/gl
	${CMAKE_CURRENT_SOURCE_DIR}/cmake/msvc
	${CMAKE_CURRENT_SOURCE_DIR}/cmake/msvc/gnu
	${CMAKE_CURRENT_BINARY_DIR}
	${GNUTLS_PROJECT_DIR}/lib/nettle
	${GNUTLS_PROJECT_DIR}/lib/minitasn1
	)
set(patches_ lib/algorithms/ciphersuites.c
             lib/algorithms/protocols.c)
set(ignores_ lib/system/keys-dummy.c)

set(lib_SOURCES_)
foreach(folder ${lib_sub_folders})
   include_directories(${GNUTLS_PROJECT_DIR}/lib/${folder})
   file(GLOB SOURCES_ ${GNUTLS_PROJECT_DIR}/lib/${folder}/*.c)
   
   set(rlist_)
   # replace patches file 
   foreach(i ${SOURCES_})
     file(RELATIVE_PATH p ${GNUTLS_PROJECT_DIR} ${i})
	 list(FIND patches_ ${p} _result)
	 if(${_result} GREATER  -1)
	   list(APPEND rlist_ ${i})
	   message(STATUS "patch -> ${p}")
	 endif()
	 
	 list(FIND ignores_ ${p} _result)
	 if(${_result} GREATER  -1)
	   list(APPEND rlist_ ${i})
	 endif()

   endforeach()
   if(rlist_)
     list(REMOVE_ITEM SOURCES_ ${rlist_})
   endif()
   
   set(lib_SOURCES_ ${lib_SOURCES_} ${SOURCES_})
endforeach()



file(GLOB gl_SOURCES_ 
    ${GNUTLS_PROJECT_DIR}/gl/c-ctype.c    
    ${GNUTLS_PROJECT_DIR}/gl/hash-pjw-bare.c
    ${GNUTLS_PROJECT_DIR}/gl/msvc-inval.c
    ${GNUTLS_PROJECT_DIR}/gl/msvc-nothrow.c
    ${GNUTLS_PROJECT_DIR}/gl/read-file.c
    ${GNUTLS_PROJECT_DIR}/gl/secure_getenv.c)

foreach( i ${patches_})
  set(gnutls_SOURCES ${gnutls_SOURCES} 
      ${CMAKE_CURRENT_SOURCE_DIR}/cmake/msvc/patches/${i})
endforeach()


set(gnutls_SOURCES ${gnutls_SOURCES} ${gl_SOURCES_} ${lib_SOURCES_})

add_library(gnutls STATIC ${gnutls_SOURCES} ${msvc_SOURCES_})
assign_source_group(${gnutls_SOURCES})

install(DIRECTORY  ${GNUTLS_PROJECT_DIR}/lib/includes DESTINATION include)
INSTALL(TARGETS gnutls
       RUNTIME DESTINATION bin
       LIBRARY DESTINATION lib
	   ARCHIVE DESTINATION lib )

if(ENABLE_UNIT_TESTS )
enable_testing()


endif()