#
#
# cmake build for gnutls, this out-of-source-build script
#
# 
#
cmake_minimum_required (VERSION 3.10)
project (gnutls C)
set (MAJOR_VERSION 3)
set (MINOR_VERSION 5)
set (VERSION_PATCH 19)
set (PATCH_VERSION ${VERSION_PATCH})
set (VERSION ${MAJOR_VERSION}.${MINOR_VERSION}.${VERSION_PATCH})
set (NUMBER_VERSION "(${MAJOR_VERSION}<<16|${MINOR_VERSION}<<8|${VERSION_PATCH})")

OPTION(ENABLE_TESTS "enable build test and check..." ON)

if(NOT PROJECT_HOME_DIR)
  set(PROJECT_HOME_DIR ${CMAKE_CURRENT_SOURCE_DIR}/${PROJECT_NAME}-${VERSION})
endif()

message(STATUS "project home : ${PROJECT_HOME_DIR}")

include(cmake/conanos.cmake)

foreach(name unictype uninorm unistr unitypes)
  configure_file(${PROJECT_HOME_DIR}/lib/unistring/${name}.in.h
                 ${PROJECT_HOME_DIR}/lib/unistring/${name}.h @ONLY)
endforeach()               
  configure_file(${PROJECT_HOME_DIR}/gl/alloca.in.h
                 ${PROJECT_HOME_DIR}/gl/alloca.h @ONLY)

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
  
  configure_file(${PROJECT_HOME_DIR}/lib/includes/gnutls/gnutls.h.in
                 ${PROJECT_HOME_DIR}/lib/includes/gnutls/gnutls.h @ONLY)
endif() 

add_definitions(-DHAVE_CONFIG_H	)

set(lib_sub_folders .
      unistring  unistring/uninorm unistring/unistr unistring/unictype
	  system openpgp opencdk 
      nettle nettle/int #minitasn1
      extras ext auth algorithms 
      accelerated accelerated/x86 x509)

include_directories(${PROJECT_HOME_DIR}
    ${PROJECT_HOME_DIR}/lib	
	${PROJECT_HOME_DIR}/lib/includes	
	${CMAKE_CURRENT_BINARY_DIR}
	${CMAKE_CURRENT_BINARY_DIR}/lib	
	${CMAKE_CURRENT_BINARY_DIR}/lib/includes	
	${PROJECT_HOME_DIR}/gl
	${CMAKE_CURRENT_SOURCE_DIR}/cmake/msvc
	${CMAKE_CURRENT_SOURCE_DIR}/cmake/msvc/gnu
	${CMAKE_CURRENT_BINARY_DIR}
	#${PROJECT_HOME_DIR}/lib/nettle
	#${PROJECT_HOME_DIR}/lib/nettle/int
	${PROJECT_HOME_DIR}/lib/minitasn1
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
    lib/nettle/sysrng-linux.c
    lib/nettle/sysrng-getentropy.c )

foreach(folder ${lib_sub_folders})
   if(${folder} STREQUAL ".")
   	   include_directories(${PROJECT_HOME_DIR}/lib)
	   file(GLOB SOURCES_ ${PROJECT_HOME_DIR}/lib/*.c)
   else()
	   include_directories(${PROJECT_HOME_DIR}/lib/${folder})
	   file(GLOB SOURCES_ ${PROJECT_HOME_DIR}/lib/${folder}/*.c)
   endif()
   
   set(rlist_)
   # replace patches file 
   foreach(i ${SOURCES_})
     file(RELATIVE_PATH p ${PROJECT_HOME_DIR} ${i})
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
    ${PROJECT_HOME_DIR}/gl/c-ctype.c    
    ${PROJECT_HOME_DIR}/gl/hash-pjw-bare.c
    ${PROJECT_HOME_DIR}/gl/msvc-inval.c
    ${PROJECT_HOME_DIR}/gl/msvc-nothrow.c
    ${PROJECT_HOME_DIR}/gl/read-file.c
    ${PROJECT_HOME_DIR}/gl/secure_getenv.c)

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

install(DIRECTORY  ${PROJECT_HOME_DIR}/lib/includes/gnutls DESTINATION include)
INSTALL(TARGETS gnutls
       RUNTIME DESTINATION bin
       LIBRARY DESTINATION lib
	   ARCHIVE DESTINATION lib )

	   
	  #--------------------------------------#
    #    TEST                              #
    #--------------------------------------#	
if(ENABLE_TESTS )
  set(TEST_HOME_DIR ${PROJECT_HOME_DIR}/tests)
  set(THOME_ ${TEST_HOME_DIR})
  enable_testing()

  add_library(libutils STATIC ${THOME_}/seccomp.c ${THOME_}/utils-adv.c
  ${THOME_}/common-cert-key-exchange.c
    ${CMAKE_CURRENT_SOURCE_DIR}/cmake/msvc/patches/lib/tests/utils.c)
  target_compile_definitions(libutils PRIVATE IN_GNUTLS_TESTS)
  
  include_directories(${THOME_})

  macro(make_test name)
    set(dirname ${ARGV1})
    string(REPLACE "/" "_" tname ${name})
    if(NOT dirname)
      set(filename ${THOME_}/${name}.c)
    else()
      set(filename ${dirname}/${name}.c)

    endif()
    message("  [${name}] ${dirname}")

    add_executable(${tname} ${filename})
    set(libs_ libutils gnutls gmp nettle hogweed zlib libtasn1)
    if(MSVC)
      set(libs_ ${libs_} Crypt32 ws2_32)
    endif()
    target_link_libraries(${tname} ${libs_} )
    target_compile_definitions(${tname} PRIVATE IN_GNUTLS_TESTS)
    
    add_test(NAME ${tname} COMMAND ${CMAKE_COMMAND}
      -DPROGRAM=${tname}
      -DARGUMENTS=0
      -DLOGFILE=${tname}-test.log  # optional
      -DCMAKE_SYSTEM_NAME=${CMAKE_SYSTEM_NAME}
      -DBIN_DIRS_LIBTASN1=${CONAN_BIN_DIRS_LIBTASN1}
      -DBIN_DIRS_ZLIB=${CONAN_BIN_DIRS_ZLIB}
      -DTEST_DIR=${THOME_}
      -P ${CMAKE_CURRENT_SOURCE_DIR}/cmake/runtest.cmake)

  endmacro(make_test name)

  #---------------------------------------------------#
  #        Test Case                                  #
  #---------------------------------------------------#

set( CTESTS_ simple set_pkcs12_cred cert certuniqueid	
  
  mpi certificate_set_x509_crl dn parse_ca x509-dn record-sizes
  hostname-check cve-2008-4989 pkcs12_s2k chainverify record-sizes-range 
  crq_key_id x509sign-verify cve-2009-1415 cve-2009-1416		
  crq_apis init_roundtrip pkcs12_s2k_pem dn2 mini-eagain	tls-rehandshake-cert-3 
  nul-in-x509-names x509_altname pkcs12_encode mini-x509		
  tls-rehandshake-cert rng-fork mini-eagain-dtls resume-dtls 
  x509cert x509cert-tl infoaccess mini-dtls-hello-verify 
  mini-tdb dtls-rehandshake-anon mini-alpn mini-dtls-large 
  mini-termination mini-x509-cas mini-x509-2 pkcs12_simple 
  mini-emsgsize-dtls chainverify-unsorted mini-overhead 
  mini-dtls-heartbeat mini-x509-callbacks key-openssl priorities	
  mini-dtls-srtp rsa-encrypt-decrypt mini-loss-time 
  mini-record mini-dtls-record mini-handshake-timeout mini-record-range 
  mini-cert-status rsa-psk global-init sec-params 
  fips-test mini-global-load name-constraints x509-extensions 
  long-session-id mini-x509-callbacks-intr mini-dtls-lowmtu 
  crlverify mini-dtls-discard init_fds mini-record-failure 
  tls-rehandshake-cert-2 custom-urls set_x509_key_mem set_x509_key_file 
  mini-chain-unsorted x509-verify-with-crl mini-dtls-mtu privkey-verify-broken 
  mini-dtls-record-asym openpgp-callback key-import-export 
  mini-dtls-fork mini-dtls-pthread mini-key-material x509cert-invalid 
  tls-ext-register tls-supplemental mini-dtls0-9 
  mini-record-retvals mini-server-name tls-etm x509-cert-callback 
  sign-md5-rep keygen mini-tls-nonblock no-signal pkcs7-gen dtls-etm 
  x509sign-verify2 mini-alignment oids atfork prf psk-file 
  status-request status-request-ok status-request-missing 
  fallback-scsv pkcs8-key-decode urls dtls-rehandshake-cert 
  key-usage-rsa key-usage-ecdhe-rsa mini-session-verify-function auto-verify 
  record-timeouts mini-dtls-hello-verify-48 mini-x509-default-prio 
  mini-x509-dual global-init-override tlsext-decoding rsa-psk-cb 
  rehandshake-switch-cert rehandshake-switch-cert-allow rehandshake-switch-cert-client 
  rehandshake-switch-cert-client-allow handshake-versions dtls-handshake-versions 
  dtls-max-record tls-max-record alpn-server-prec ocsp-filename-memleak 
  dh-params rehandshake-ext-secret pcert-list session-export-funcs 
  handshake-false-start version-checks key-material-dtls key-material-set-dtls 
  system-prio-file name-constraints-merge crl-basic crq-basic 
  send-client-cert custom-urls-override hex rehandshake-switch-psk-id 
  rehandshake-switch-srp-id base64 srpbase64 pkcs1-digest-info set_x509_key 
  set_x509_key_file_der set_x509_pkcs12_key crt_apis tls1.2-cert-key-exchange 
  tls1.1-cert-key-exchange tls1.0-cert-key-exchange ssl3.0-cert-key-exchange 
  dtls1.2-cert-key-exchange dtls1.0-cert-key-exchange x509-cert-callback-legacy 
  keylog-env ssl2-hello tlsfeature-ext dtls-rehandshake-cert-2 
  tlsfeature-crt dtls-rehandshake-cert-3 resume-with-false-start 
  set_x509_key_file_ocsp client-fastopen rng-sigint srp rng-pthread 
  safe-renegotiation/srn0 safe-renegotiation/srn1 safe-renegotiation/srn2 
  safe-renegotiation/srn3 safe-renegotiation/srn4 safe-renegotiation/srn5 
  rsa-illegal-import set_x509_key_file_ocsp_multi set_key set_x509_key_file_ocsp_multi2 
  set_key_utf8 set_x509_key_utf8 insecure_key handshake-large-packet 
  client_dsa_key server_ecdsa_key tls-session-ext-register tls-session-supplemental 
  multi-alerts naked-alerts pkcs7-cat-parse set_known_dh_params_x509 
  set_known_dh_params_anon set_known_dh_params_psk session-tickets-ok 
  session-tickets-missing set_x509_key_file_legacy status-request-ext 
  rng-no-onload crl_apis cert_verify_inv_utf8 
  hostname-check-utf8 pkcs8-key-decode-encrypted priority-mix trust-store 
  dtls-repro-20170915 )

set(failures_ 
set_pkcs12_cred chainverify crq_apis tls-rehandshake-cert-3 rng-fork
resume-dtls x509cert-tl mini-dtls-hello-verify dtls-rehandshake-anon
mini-alpn mini-dtls-large mini-termination mini-x509-cas pkcs12_simple
mini-overhead mini-dtls-heartbeat mini-dtls-srtp mini-loss-time mini-record
mini-dtls-record mini-handshake-timeout mini-record-range mini-cert-status
rsa-psk fips-test mini-global-load name-constraints long-session-id
mini-dtls-lowmtu crlverify mini-dtls-discard mini-record-failure tls-rehandshake-cert-2
custom-urls mini-chain-unsorted x509-verify-with-crl mini-dtls-mtu mini-dtls-record-asym
openpgp-callback mini-dtls-fork mini-dtls-pthread mini-key-material tls-ext-register
tls-supplemental mini-dtls0-9 mini-record-retvals mini-server-name tls-etm x509-dn-decode 
sign-md5-rep mini-tls-nonblock no-signal pkcs7-gen dtls-etm mini-alignment rng-no-onload 
atfork prf psk-file status-request status-request-ok ocsp-filename-memleak crl_apis
status-request-missing fallback-scsv pkcs8-key-decode dtls-rehandshake-cert pkcs7-cat-parse
mini-dtls-hello-verify-48 global-init-override tlsext-decoding rsa-psk-cb alpn-server-prec
dh-params pcert-list key-material-dtls key-material-set-dtls system-prio-file custom-urls-override
pkcs1-digest-info keylog-env ssl2-hello dtls-rehandshake-cert-2 dtls-rehandshake-cert-3
client-fastopen rng-sigint srp rng-pthread set_key_utf8 set_x509_key_utf8 handshake-large-packet
tls-session-ext-register tls-session-supplemental multi-alerts naked-alerts cert_verify_inv_utf8 
session-tickets-ok session-tickets-missing status-request-ext pkcs8-key-decode-encrypted )

list(REMOVE_ITEM CTESTS_ ${failures_})

message(STATUS "GnuTLS Tests")
foreach(name ${CTESTS_})
  make_test(${name})  
endforeach()
set(PTEST_ ${CMAKE_CURRENT_SOURCE_DIR}/cmake/msvc/patches/lib/tests)
make_test(dtls1-2-mtu-check ${PTEST_})  

endif()