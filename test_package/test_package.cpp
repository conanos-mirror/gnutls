
#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <string.h>
#include <stdarg.h>
#include <gnutls/gnutls.h>
#include <gnutls/pkcs11.h>

#define fail(format, ...) \
    printf("%s:%d: "format, __func__, __LINE__, ##__VA_ARGS__);


#define CHECK_OK(x,y,z) \
	if (x >= 0 && y >= 0 && z >= 0) { \
	if (!gnutls_check_version_numeric(x, y, z)) { \
		fail("error in gnutls_check_version_numeric %d.%d.%d: %d\n", x, y, z, __LINE__); \
		exit(1); \
	} \
	}

#define CHECK_FAIL(x,y,z) \
	if (gnutls_check_version_numeric(x, y, z)) { \
		fail("error in neg gnutls_check_version_numeric %d.%d.%d: %d\n", x, y, z, __LINE__); \
		exit(1); \
	}

int main(void)
{
	printf("GnuTLS header version %s.\n", GNUTLS_VERSION);
	printf("GnuTLS library version %s.\n",gnutls_check_version(NULL));

	if (!gnutls_check_version_numeric(GNUTLS_VERSION_MAJOR, GNUTLS_VERSION_MINOR, GNUTLS_VERSION_PATCH)) {
		exit(1);
	}

	CHECK_FAIL(99, 9, 9)
	CHECK_FAIL(90, 1, 0)
	CHECK_FAIL(90, 0, 0)

	CHECK_OK(2, 0, 0)
	CHECK_OK(2, 99, 99)
	CHECK_OK(3, 0, 0)
	return 0;

}
