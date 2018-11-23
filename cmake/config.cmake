
INCLUDE (CheckIncludeFiles)
INCLUDE (CheckFunctionExists)
INCLUDE (CheckLibraryExists) 
INCLUDE (CheckTypeSize) 
INCLUDE (CheckSymbolExists)

# Define to the number of bits in type 'ptrdiff_t'.
CHECK_TYPE_SIZE("ptrdiff_t" SIZEOF_PTRDIFF_T)
IF (SIZEOF_PTRDIFF_T)
    SET(BITSIZEOF_PTRDIFF_T "(${SIZEOF_PTRDIFF_T}*8)")
ENDIF (SIZEOF_PTRDIFF_T)


# Define to the number of bits in type 'sig_atomic_t'. 
CHECK_TYPE_SIZE("sig_atomic_t" SIZEOF_SIG_ATOMIC_T)
IF (SIZEOF_SIG_ATOMIC_T)
    SET(BITSIZEOF_SIG_ATOMIC_T "(${SIZEOF_SIG_ATOMIC_T}*8)")
ENDIF (SIZEOF_SIG_ATOMIC_T)


# Define to the number of bits in type 'size_t'.
CHECK_TYPE_SIZE("size_t" SIZEOF_SIZE_T)
IF (SIZEOF_SIZE_T)
    SET(BITSIZEOF_SIZE_T "(${SIZEOF_SIZE_T}*8)")
ENDIF (SIZEOF_SIZE_T)

# Define to the number of bits in type 'wchar_t'.
CHECK_TYPE_SIZE("wchar_t" SIZEOF_WCHAR_T)
IF (SIZEOF_WCHAR_T)
    SET(BITSIZEOF_WCHAR_T "(${SIZEOF_WCHAR_T}*8)")
ENDIF (SIZEOF_WCHAR_T)

# Define to the number of bits in type 'wint_t'.
CHECK_TYPE_SIZE("wint_t" SIZEOF_WINT_T)
IF (SIZEOF_WINT_T)
    SET(BITSIZEOF_WINT_T "(${SIZEOF_WINT_T}*8)")
ENDIF (SIZEOF_WINT_T)

# Define to 1 if you have `alloca', as a function or macro.
CHECK_FUNCTION_EXISTS(alloca HAVE_ALLOCA)

# Define to 1 if you have <alloca.h> and it should be used (not on Ultrix).
CHECK_INCLUDE_FILES(alloca.h HAVE_ALLOCA_H)

# Define to 1 if you have the `canonicalize_file_name' function.
CHECK_FUNCTION_EXISTS(canonicalize_file_name HAVE_CANONICALIZE_FILE_NAME)

# Define to 1 if you have the MacOS X function CFLocaleCopyCurrent in the
# CoreFoundation framework. 
CHECK_FUNCTION_EXISTS(CFLocaleCopyCurrent HAVE_CFLOCALECOPYCURRENT)

# Define to 1 if you have the MacOS X function CFPreferencesCopyAppValue in
# the CoreFoundation framework.
CHECK_FUNCTION_EXISTS(CoreFoundation HAVE_CFPREFERENCESCOPYAPPVALUE)

# Define if the GNU dcgettext() function is already present or preinstalled.
CHECK_FUNCTION_EXISTS(dcgettext HAVE_DCGETTEXT)

# Define to 1 if you have the declaration of `fflush_unlocked', and to 0 if
# you don't. 
CHECK_FUNCTION_EXISTS(fflush_unlocked HAVE_DECL_FFLUSH_UNLOCKED)

# Define to 1 if you have the declaration of `fputs_unlocked', and to 0 if
# you don't. 
CHECK_FUNCTION_EXISTS(fputs_unlocked HAVE_DECL_FPUTS_UNLOCKED)

# Define to 1 if you have the declaration of `getc_unlocked', and to 0 if you
# don't. 
CHECK_FUNCTION_EXISTS(getc_unlocked HAVE_DECL_GETC_UNLOCKED)

# Define to 1 if you have the declaration of `putc_unlocked', and to 0 if you
# don't. 
CHECK_FUNCTION_EXISTS(putc_unlocked HAVE_DECL_PUTC_UNLOCKED)

# Define to 1 if you have the declaration of `strerror_r', and to 0 if you
# don't. 
CHECK_FUNCTION_EXISTS(strerror_r HAVE_DECL_STRERROR_R)

# Define to 1 if you have the <dlfcn.h> header file. 
CHECK_INCLUDE_FILES(dlfcn.h HAVE_DLFCN_H)

# Define if you have the declaration of environ. 
CHECK_FUNCTION_EXISTS(environ HAVE_ENVIRON_DECL)

# Define to 1 if you have the <errno.h> header file. 
CHECK_INCLUDE_FILES(errno.h HAVE_ERRNO_H)

# Define if the GNU gettext() function is already present or preinstalled. 
CHECK_FUNCTION_EXISTS(gettext HAVE_GETTEXT)

# Define to 1 if you have the <inttypes.h> header file. 
CHECK_INCLUDE_FILES(inttypes.h HAVE_INTTYPES_H)

# Define to 1 if the system has the type `long long int'. 
CHECK_TYPE_SIZE("long long int" HAVE_LONG_LONG_INT)

# Define if the 'malloc' function is POSIX compliant. 
IF (WIN32)
  UNSET(HAVE_MALLOC_POSIX)
ELSE (WIN32)
  SET(HAVE_MALLOC_POSIX ON)
ENDIF (WIN32)

# Define to 1 if you have the `mbrtowc' function. 
CHECK_FUNCTION_EXISTS(mbrtowc HAVE_MBRTOWC)

# Define to 1 if you have the <memory.h> header file. 
CHECK_INCLUDE_FILES(memory.h HAVE_MEMORY_H)

# Define to 1 if you have the <search.h> header file. 
CHECK_INCLUDE_FILES(search.h HAVE_SEARCH_H)

# Define to 1 if you have the `setenv' function. 
CHECK_FUNCTION_EXISTS(setenv HAVE_SETENV)

# Define to 1 if the system has the type `sigset_t'. 
CHECK_SYMBOL_EXISTS(sigset_t signal.h HAVE_SIGSET_T)

# Define to 1 if stdbool.h conforms to C99. 
CHECK_INCLUDE_FILES(stdbool.h HAVE_STDBOOL_H)

# Define to 1 if you have the <stdint.h> header file. 
CHECK_INCLUDE_FILES(stdint.h HAVE_STDINT_H)

# Define to 1 if you have the <stdlib.h> header file. 
CHECK_INCLUDE_FILES(stdlib.h HAVE_STDLIB_H)

# Define to 1 if you have the `strerror_r' function. 
CHECK_INCLUDE_FILES(strerror_r HAVE_STRERROR_R)

# Define to 1 if you have the <strings.h> header file. 
CHECK_INCLUDE_FILES(strings.h HAVE_STRINGS_H)

# Define to 1 if you have the <string.h> header file. 
CHECK_INCLUDE_FILES(string.h HAVE_STRING_H)

# Define to 1 if you have the <sys/bitypes.h> header file. 
CHECK_INCLUDE_FILES(sys/bitypes.h HAVE_SYS_BITYPES_H)

# Define to 1 if you have the <sys/inttypes.h> header file. 
CHECK_INCLUDE_FILES(sys/inttypes.h HAVE_SYS_INTTYPES_H)

# Define to 1 if you have the <sys/param.h> header file. 
CHECK_INCLUDE_FILES(sys/param.h HAVE_SYS_PARAM_H)

# Define to 1 if you have the <sys/socket.h> header file. 
CHECK_INCLUDE_FILES(sys/socket.h HAVE_SYS_SOCKET_H)

# Define to 1 if you have the <sys/stat.h> header file. 
CHECK_INCLUDE_FILES(sys/stat.h HAVE_SYS_STAT_H)

# Define to 1 if you have the <sys/types.h> header file. 
CHECK_INCLUDE_FILES(sys/types.h HAVE_SYS_TYPES_H)

# Define to 1 if you have the `tsearch' function. 
CHECK_FUNCTION_EXISTS(tsearch HAVE_TSEARCH)

# Define to 1 if you have the <unistd.h> header file. 
CHECK_INCLUDE_FILES(unistd.h HAVE_UNISTD_H)

# Define to 1 if the system has the type `unsigned long long int'. 
CHECK_TYPE_SIZE("unsigned long long int" HAVE_UNSIGNED_LONG_LONG_INT)

# Define to 1 if you have the <wchar.h> header file. 
CHECK_INCLUDE_FILES(wchar.h HAVE_WCHAR_H)

# Define if you have the 'wchar_t' type. 
CHECK_SYMBOL_EXISTS(wchar_t wchar.h HAVE_WCHAR_T)

# Define to 1 if you have the `wcrtomb' function. 
CHECK_FUNCTION_EXISTS(wcrtomb HAVE_WCRTOMB)

# Define to 1 if you have the <winsock2.h> header file. 
IF (WIN32)
  SET(HAVE_WINSOCK2_H ON)
ELSE (WIN32)
  UNSET(HAVE_WINSOCK2_H)
ENDIF (WIN32)

# Define if you have the 'wint_t' type. 
CHECK_TYPE_SIZE("wint_t" HAVE_WINT_T)

# Define to 1 if you have the <ws2tcpip.h> header file.
CHECK_INCLUDE_FILES(ws2tcpip.h HAVE_WS2TCPIP_H)

# Define to 1 if the system has the type `_Bool'. 
CHECK_TYPE_SIZE(_Bool HAVE__BOOL)

# The size of `unsigned int', as computed by sizeof.
CHECK_TYPE_SIZE("unsigned int" SIZEOF_UNSIGNED_INT)

# The size of `unsigned long int', as computed by sizeof.
CHECK_TYPE_SIZE("unsigned long int" SIZEOF_UNSIGNED_LONG_INT)
