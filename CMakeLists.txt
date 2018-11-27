cmake_minimum_required (VERSION 3.1)
project (GnuTLS C)
set (MAJOR_VERSION 3)
set (MINOR_VERSION 4)
set (VERSION_PATCH 0)
set (VERSION 3.4)

OPTION(ENABLE_UNIT_TESTS "enable test ..." ON)

if(NOT GNUTLS_PROJECT_DIR)
  set(GNUTLS_PROJECT_DIR ${CMAKE_CURRENT_SOURCE_DIR}/gnutls-${VERSION})
endif()

include(cmake/conanos.cmake)
#include(cmake/config.cmake)
#configure_file(${CMAKE_CURRENT_SOURCE_DIR}/cmake/config.h.cmakein
#               ${CMAKE_CURRENT_BINARY_DIR}/config.h)

 
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

include_directories(${GNUTLS_PROJECT_DIR}/lib	
	${GNUTLS_PROJECT_DIR}/lib/includes	
	${GNUTLS_PROJECT_DIR}/gl
	${GNUTLS_PROJECT_DIR}/lib/unistring
	${GNUTLS_PROJECT_DIR}/lib/system
	${GNUTLS_PROJECT_DIR}/lib/openpgp
	${GNUTLS_PROJECT_DIR}/lib/opencdk
	${GNUTLS_PROJECT_DIR}/lib/nettle
	${GNUTLS_PROJECT_DIR}/lib/minitasn1
	${GNUTLS_PROJECT_DIR}/lib/extras
	${GNUTLS_PROJECT_DIR}/lib/ext
	${GNUTLS_PROJECT_DIR}/lib/auth
	${GNUTLS_PROJECT_DIR}/lib/algorithms
	${GNUTLS_PROJECT_DIR}/lib/accelerated
	${GNUTLS_PROJECT_DIR}/lib/accelerated/x86
	${GNUTLS_PROJECT_DIR}/lib/x509
	)

include_directories(${GNUTLS_PROJECT_DIR}
                    ${CMAKE_CURRENT_SOURCE_DIR}/cmake/msvc
					${CMAKE_CURRENT_SOURCE_DIR}/cmake/msvc/${__arch__}
					${CMAKE_CURRENT_SOURCE_DIR}/cmake/msvc/lib
					${CMAKE_CURRENT_SOURCE_DIR}/cmake/msvc/lib/unistring                 
                    ${CMAKE_CURRENT_BINARY_DIR}
					)
#set(msvcd_ ${CMAKE_CURRENT_SOURCE_DIR}/cmake/msvc)
#file(GLOB_RECURSE  msvc_SOURCES_ ${CMAKE_CURRENT_SOURCE_DIR}/cmake/msvc/*/*.c)
	   

set(SOURCES_ 
    gl/c-ctype.c
    gl/hash-pjw-bare.c
    gl/msvc-inval.c
    gl/msvc-nothrow.c
    gl/read-file.c
	gl/secure_getenv.c
	
    lib/accelerated/accelerated.c
    lib/accelerated/cryptodev-gcm.c
    lib/accelerated/cryptodev.c
    lib/accelerated/x86/aes-cbc-x86-aesni.c
    lib/accelerated/x86/aes-cbc-x86-ssse3.c
    lib/accelerated/x86/aes-ccm-x86-aesni.c
    lib/accelerated/x86/aes-gcm-padlock.c
    lib/accelerated/x86/aes-gcm-x86-aesni.c
    lib/accelerated/x86/aes-gcm-x86-pclmul-avx.c
    lib/accelerated/x86/aes-gcm-x86-pclmul.c
    lib/accelerated/x86/aes-gcm-x86-ssse3.c
    lib/accelerated/x86/aes-padlock.c
    lib/accelerated/x86/hmac-padlock.c
    lib/accelerated/x86/hmac-x86-ssse3.c
    lib/accelerated/x86/sha-padlock.c
    lib/accelerated/x86/sha-x86-ssse3.c
    lib/accelerated/x86/x86-common.c
    lib/alert.c
    lib/algorithms/cert_types.c
    lib/algorithms/ciphers.c
    #lib/algorithms/ciphersuites.c
    lib/algorithms/ecc.c
    lib/algorithms/kx.c
    lib/algorithms/mac.c
    #lib/algorithms/protocols.c
    lib/algorithms/publickey.c
    lib/algorithms/secparams.c
    lib/algorithms/sign.c
    lib/anon_cred.c
    lib/atfork.c
    lib/auth.c
    lib/auth/anon.c
    lib/auth/anon_ecdh.c
    lib/auth/cert.c
    lib/auth/dhe.c
    lib/auth/dhe_psk.c
    lib/auth/dh_common.c
    lib/auth/ecdhe.c
    lib/auth/psk.c
    lib/auth/psk_passwd.c
    lib/auth/rsa.c
    lib/auth/rsa_psk.c
    lib/auth/srp_kx.c
    lib/auth/srp_passwd.c
    lib/auth/srp_rsa.c
    lib/auth/srp_sb64.c
    lib/auto-verify.c
    lib/buffers.c
    lib/cert-session.c
    lib/cert.c
    lib/cipher.c
    lib/cipher_int.c
    lib/compress.c
    lib/constate.c
    lib/crypto-api.c
    lib/crypto-backend.c
    lib/datum.c
    lib/db.c
    lib/debug.c
    lib/dh-primes.c
    lib/dh-session.c
    lib/dh.c
    lib/dtls-sw.c
    lib/dtls.c
    lib/ecc.c
    lib/errors.c
    lib/extensions.c
    lib/extras/hex.c
    lib/extras/randomart.c
    lib/ext/alpn.c
    lib/ext/cert_type.c
    lib/ext/dumbfw.c
    lib/ext/ecc.c
    lib/ext/etm.c
    lib/ext/ext_master_secret.c
    lib/ext/heartbeat.c
    lib/ext/max_record.c
    lib/ext/safe_renegotiation.c
    lib/ext/server_name.c
    lib/ext/session_ticket.c
    lib/ext/signature.c
    lib/ext/srp.c
    lib/ext/srtp.c
    lib/ext/status_request.c
    lib/file.c
    lib/fingerprint.c
    lib/fips.c
    lib/global.c
    lib/gnutls_asn1_tab.c
    lib/handshake-checks.c
    lib/handshake.c
    lib/hash_int.c
    lib/kx.c
    lib/locks.c
    lib/mbuffers.c
    lib/mem.c
#    lib/minitasn1/coding.c
#    lib/minitasn1/decoding.c
#    lib/minitasn1/element.c
#    lib/minitasn1/errors.c
#    lib/minitasn1/gstr.c
#    lib/minitasn1/parser_aux.c
#    lib/minitasn1/structure.c
#    lib/minitasn1/version.c
    lib/mpi.c
#    lib/nettle/cipher.c
#    lib/nettle/init.c
#    lib/nettle/int/dsa-keygen-fips186.c
#    lib/nettle/int/dsa-validate.c
#    lib/nettle/int/provable-prime.c
#    lib/nettle/int/rsa-keygen-fips186.c
#    lib/nettle/mac.c
#    lib/nettle/mpi.c
#    lib/nettle/pk.c
#    lib/nettle/rnd-common.c
#    lib/nettle/rnd.c
#    lib/nettle/sysrng-windows.c
    lib/num.c
    lib/opencdk/armor.c
    lib/opencdk/kbnode.c
    lib/opencdk/keydb.c
    lib/opencdk/literal.c
    lib/opencdk/misc.c
    lib/opencdk/new-packet.c
    lib/opencdk/pubkey.c
    lib/opencdk/read-packet.c
    lib/opencdk/seskey.c
    lib/opencdk/sig-check.c
    lib/opencdk/stream.c
    lib/opencdk/write-packet.c
    lib/openpgp/compat.c
    lib/openpgp/extras.c
    lib/openpgp/openpgp.c
    lib/openpgp/output.c
    lib/openpgp/pgp.c
    lib/openpgp/pgpverify.c
    lib/openpgp/privkey.c
    lib/openpgp_compat.c
    lib/pcert.c
    lib/pin.c
    lib/pk.c
    lib/pkix_asn1_tab.c
    lib/prf.c
    #lib/priority.c
    lib/privkey.c
    lib/privkey_raw.c
    lib/psk.c
    lib/pubkey.c
    lib/random.c
    lib/randomart.c
    lib/range.c
    lib/record.c
    lib/safe-memfuncs.c
    lib/session.c
    lib/session_pack.c
    lib/srp.c
    lib/sslv2_compat.c
    lib/state.c
    lib/str-iconv.c
    lib/str-idna.c
    lib/str-unicode.c
    lib/str.c
    lib/supplemental.c
    lib/system.c
    lib/system/certs.c
    lib/system/fastopen.c
    lib/system/inet_ntop.c
    lib/system/inet_pton.c
    lib/system/keys-win.c
    lib/system/sockets.c
    lib/system/threads.c
    lib/system/vasprintf.c
    lib/system_override.c
    lib/tls-sig.c
    lib/tpm.c
    lib/unistring/unictype/categ_and.c
    lib/unistring/unictype/categ_and_not.c
    lib/unistring/unictype/categ_byname.c
    lib/unistring/unictype/categ_C.c
    lib/unistring/unictype/categ_Cc.c
    lib/unistring/unictype/categ_Cf.c
    lib/unistring/unictype/categ_Cn.c
    lib/unistring/unictype/categ_Co.c
    lib/unistring/unictype/categ_Cs.c
    lib/unistring/unictype/categ_L.c
    lib/unistring/unictype/categ_LC.c
    lib/unistring/unictype/categ_Ll.c
    lib/unistring/unictype/categ_Lm.c
    lib/unistring/unictype/categ_Lo.c
    lib/unistring/unictype/categ_longname.c
    lib/unistring/unictype/categ_Lt.c
    lib/unistring/unictype/categ_Lu.c
    lib/unistring/unictype/categ_M.c
    lib/unistring/unictype/categ_Mc.c
    lib/unistring/unictype/categ_Me.c
    lib/unistring/unictype/categ_Mn.c
    lib/unistring/unictype/categ_N.c
    lib/unistring/unictype/categ_name.c
    lib/unistring/unictype/categ_Nd.c
    lib/unistring/unictype/categ_Nl.c
    lib/unistring/unictype/categ_No.c
    lib/unistring/unictype/categ_none.c
    lib/unistring/unictype/categ_of.c
    lib/unistring/unictype/categ_or.c
    lib/unistring/unictype/categ_P.c
    lib/unistring/unictype/categ_Pc.c
    lib/unistring/unictype/categ_Pd.c
    lib/unistring/unictype/categ_Pe.c
    lib/unistring/unictype/categ_Pf.c
    lib/unistring/unictype/categ_Pi.c
    lib/unistring/unictype/categ_Po.c
    lib/unistring/unictype/categ_Ps.c
    lib/unistring/unictype/categ_S.c
    lib/unistring/unictype/categ_Sc.c
    lib/unistring/unictype/categ_Sk.c
    lib/unistring/unictype/categ_Sm.c
    lib/unistring/unictype/categ_So.c
    lib/unistring/unictype/categ_test.c
    lib/unistring/unictype/categ_Z.c
    lib/unistring/unictype/categ_Zl.c
    lib/unistring/unictype/categ_Zp.c
    lib/unistring/unictype/categ_Zs.c
    lib/unistring/unictype/combiningclass.c
    lib/unistring/unictype/pr_default_ignorable_code_point.c
    lib/unistring/unictype/pr_join_control.c
    lib/unistring/unictype/pr_not_a_character.c
    lib/unistring/uninorm/canonical-decomposition.c
    lib/unistring/uninorm/compat-decomposition.c
    lib/unistring/uninorm/composition.c
    lib/unistring/uninorm/decompose-internal.c
    lib/unistring/uninorm/decomposition-table.c
    lib/unistring/uninorm/decomposition.c
    lib/unistring/uninorm/nfc.c
    lib/unistring/uninorm/nfd.c
    lib/unistring/uninorm/nfkc.c
    lib/unistring/uninorm/nfkd.c
    lib/unistring/uninorm/u16-normalize.c
    lib/unistring/uninorm/u32-normalize.c
    lib/unistring/uninorm/u8-normalize.c
    lib/unistring/unistr/u16-cpy.c
    lib/unistring/unistr/u16-mbtouc-unsafe-aux.c
    lib/unistring/unistr/u16-mbtouc-unsafe.c
    lib/unistring/unistr/u16-mbtoucr.c
    lib/unistring/unistr/u16-to-u8.c
    lib/unistring/unistr/u16-uctomb-aux.c
    lib/unistring/unistr/u16-uctomb.c
    lib/unistring/unistr/u32-cpy.c
    lib/unistring/unistr/u32-mbtouc-unsafe.c
    lib/unistring/unistr/u32-to-u8.c
    lib/unistring/unistr/u32-uctomb.c
    lib/unistring/unistr/u8-check.c
    lib/unistring/unistr/u8-cpy.c
    lib/unistring/unistr/u8-mbtouc-unsafe-aux.c
    lib/unistring/unistr/u8-mbtouc-unsafe.c
    lib/unistring/unistr/u8-mbtoucr.c
    lib/unistring/unistr/u8-to-u16.c
    lib/unistring/unistr/u8-to-u32.c
    lib/unistring/unistr/u8-uctomb-aux.c
    lib/unistring/unistr/u8-uctomb.c
    lib/urls.c
    lib/verify-tofu.c
    #lib/x509.c
    lib/x509/attributes.c
    lib/x509/common.c
    lib/x509/crl.c
    lib/x509/crl_write.c
    lib/x509/crq.c
    lib/x509/dn.c
    lib/x509/email-verify.c
    lib/x509/extensions.c
    lib/x509/hostname-verify.c
    lib/x509/ip.c
    lib/x509/key_decode.c
    lib/x509/key_encode.c
    lib/x509/krb5.c
    lib/x509/mpi.c
    lib/x509/name_constraints.c
    lib/x509/ocsp.c
    lib/x509/ocsp_output.c
    lib/x509/output.c
    lib/x509/pkcs12.c
    lib/x509/pkcs12_bag.c
    lib/x509/pkcs12_encr.c
    lib/x509/pkcs7-attrs.c
    lib/x509/pkcs7-crypt.c
    lib/x509/pkcs7-output.c
    lib/x509/pkcs7.c
    lib/x509/privkey.c
    lib/x509/privkey_openssl.c
    lib/x509/privkey_pkcs8.c
    lib/x509/privkey_pkcs8_pbes1.c
    lib/x509/prov-seed.c
    lib/x509/sign.c
    lib/x509/time.c
    lib/x509/tls_features.c
    lib/x509/verify-high.c
    lib/x509/verify-high2.c
    lib/x509/verify.c
    lib/x509/virt-san.c
    lib/x509/x509.c
    lib/x509/x509_dn.c
    lib/x509/x509_ext.c
    lib/x509/x509_write.c
    lib/x509_b64.c
	)

	

foreach(name ${SOURCES_})
	set(gnutls_SOURCES ${gnutls_SOURCES} ${GNUTLS_PROJECT_DIR}/${name})
endforeach()


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