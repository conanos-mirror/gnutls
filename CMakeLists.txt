cmake_minimum_required (VERSION 3.1)
project (GnuTLS C)
set (MAJOR_VERSION 3)
set (MINOR_VERSION 5)
set (VERSION_PATCH 19)
set (PATCH_VERSION ${VERSION_PATCH})
set (VERSION ${MAJOR_VERSION}.${MINOR_VERSION}.${VERSION_PATCH})
set (NUMBER_VERSION "(${MAJOR_VERSION}<<16|${MINOR_VERSION}<<8|${VERSION_PATCH})")
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

add_definitions(-DHAVE_CONFIG_H	)

set(lib_sub_folders .
      unistring  unistring/uninorm unistring/unistr unistring/unictype
	  system openpgp opencdk 
      nettle nettle/int #minitasn1
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
	#${GNUTLS_PROJECT_DIR}/lib/nettle
	#${GNUTLS_PROJECT_DIR}/lib/nettle/int
	${GNUTLS_PROJECT_DIR}/lib/minitasn1
	)
	
set(patches_ lib/priority.c
             lib/x509.c
             lib/algorithms/ciphersuites.c
             lib/algorithms/protocols.c
			 lib/nettle/int/provable-prime.c)
			 
			 
set(ignores_ lib/pkcs11_secret.c
			 lib/pkcs11.c
			 lib/pkcs11x.c
			 lib/pkcs11_privkey.c
			 lib/pkcs11_int.c
			 lib/pkcs11_write.c
             lib/system/keys-dummy.c
             lib/nettle/sysrng-linux.c )


#set(__lib_root_sources_  alert.c anon_cred.c atfork.c auth.c
#    buffers.c cert.c cipher.c cipher_int.c compress.c constate.c
#    datum.c db.c debug.c dh.c dtls.c ecc.c errors.c extensions.c 
#    file.c fingerprint.c fips.c global.c gnutls_asn1_tab.c handshake.c 
#    hash_int.c kx.c locks.c mbuffers.c mem.c mpi.c num.c openpgp_compat.c
#    pcert.c pin.c pk.c pkix_asn1_tab.c prf.c privkey.c privkey_raw.c 
#    psk.c pubkey.c random.c randomart.c range.c record.c session.c 
#    session_pack.c srp.c sslv2_compat.c state.c str.c str-iconv.c str-unicode.c
#	supplemental.c  safe-memfuncs.c crypto-backend.c
#    system.c system_override.c tpm.c urls.c  x509_b64.c
#	str-idna.c
#	)
#	
#set(lib_root_sources_)
#	
#file(GLOB srcs_ ${GNUTLS_PROJECT_DIR}/lib/*.c)
#
#
#
#foreach(name ${lib_root_sources_})
#   set(lib_SOURCES_ ${lib_SOURCES_} ${GNUTLS_PROJECT_DIR}/lib/${name})
#endforeach()
#set(lib_SOURCES_ ${lib_SOURCES_} 
#   ${CMAKE_CURRENT_SOURCE_DIR}/cmake/msvc/patches/lib/priority.c
#   ${CMAKE_CURRENT_SOURCE_DIR}/cmake/msvc/patches/lib/x509.c
#   )

foreach(folder ${lib_sub_folders})
   if(${folder} STREQUAL ".")
   	   include_directories(${GNUTLS_PROJECT_DIR}/lib)
	   file(GLOB SOURCES_ ${GNUTLS_PROJECT_DIR}/lib/*.c)
   else()
	   include_directories(${GNUTLS_PROJECT_DIR}/lib/${folder})
	   file(GLOB SOURCES_ ${GNUTLS_PROJECT_DIR}/lib/${folder}/*.c)
   endif()
   
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
#if(MSVC)
#  target_link_libraries(gnutls Crypt32.lib ws2_32.lib)
#endif()
#Crypt32.lib
assign_source_group(${gnutls_SOURCES})

install(DIRECTORY  ${GNUTLS_PROJECT_DIR}/lib/includes/gnutls DESTINATION include)
INSTALL(TARGETS gnutls
       RUNTIME DESTINATION bin
       LIBRARY DESTINATION lib
	   ARCHIVE DESTINATION lib )

if(ENABLE_UNIT_TESTS )
enable_testing()


endif()