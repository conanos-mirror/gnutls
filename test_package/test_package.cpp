
#include "gnutls/gnutls.h"
#include "gnutls/abstract.h"
#include "gnutls/x509.h"

int main() {
    gnutls_pubkey_t pubkey;
    gnutls_pubkey_init(&pubkey);
    gnutls_pubkey_deinit(pubkey);
    return 0;
}
