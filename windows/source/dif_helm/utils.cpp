#include "pch.h"
#include "utils.h"
#include <openssl/rand.h>
#include <openssl/sha.h>
#include <iostream>

#define LOG_START(func) std::cout << "[INFO] Starting " << func << std::endl;
#define LOG_END(func) std::cout << "[INFO] Finished " << func << std::endl;

void generate_p_g_a(int bits, char** p, char** g, char** a) {
    LOG_START("generate_p_g_a");

    BIGNUM* bn_p = BN_new();
    BIGNUM* bn_g = BN_new();
    BIGNUM* bn_a = BN_new();

    BN_generate_prime_ex(bn_p, bits, 1, nullptr, nullptr, nullptr);
    *p = BN_bn2dec(bn_p);

    BN_set_word(bn_g, 2);
    *g = BN_bn2dec(bn_g);

    BIGNUM* range = BN_new();
    BN_sub(range, bn_p, BN_value_one());
    BN_rand_range(bn_a, range);
    *a = BN_bn2dec(bn_a);

    BN_free(bn_p);
    BN_free(bn_g);
    BN_free(bn_a);
    BN_free(range);

    LOG_END("generate_p_g_a");
}

void generate_b(const char* p, const char* g, char** b) {
    LOG_START("generate_b");

    BIGNUM* bn_p = BN_new();
    BIGNUM* bn_b = BN_new();

    BN_dec2bn(&bn_p, p);
    BIGNUM* range = BN_new();
    BN_sub(range, bn_p, BN_value_one());
    BN_rand_range(bn_b, range);
    *b = BN_bn2dec(bn_b);

    BN_free(bn_p);
    BN_free(bn_b);
    BN_free(range);

    LOG_END("generate_b");
}

void generate_A(const char* p, const char* g, const char* a, char** A) {
    LOG_START("generate_A");

    BIGNUM* bn_p = BN_new();
    BIGNUM* bn_g = BN_new();
    BIGNUM* bn_a = BN_new();
    BIGNUM* bn_A = BN_new();

    BN_dec2bn(&bn_p, p);
    BN_dec2bn(&bn_g, g);
    BN_dec2bn(&bn_a, a);

    BN_CTX* ctx = BN_CTX_new();
    BN_mod_exp(bn_A, bn_g, bn_a, bn_p, ctx);
    *A = BN_bn2dec(bn_A);

    BN_CTX_free(ctx);
    BN_free(bn_p);
    BN_free(bn_g);
    BN_free(bn_a);
    BN_free(bn_A);

    LOG_END("generate_A");
}

void generate_shared_key(const char* A, const char* p, const char* g, const char* b, char** shared_key) {
    LOG_START("generate_shared_key");

    BIGNUM* bn_A = BN_new();
    BIGNUM* bn_p = BN_new();
    BIGNUM* bn_b = BN_new();
    BIGNUM* bn_shared_key = BN_new();

    BN_dec2bn(&bn_A, A);
    BN_dec2bn(&bn_p, p);
    BN_dec2bn(&bn_b, b);

    BN_CTX* ctx = BN_CTX_new();
    BN_mod_exp(bn_shared_key, bn_A, bn_b, bn_p, ctx);
    *shared_key = BN_bn2dec(bn_shared_key);

    BN_CTX_free(ctx);
    BN_free(bn_A);
    BN_free(bn_p);
    BN_free(bn_b);
    BN_free(bn_shared_key);

    LOG_END("generate_shared_key");
}

void hash_shared_key(const char* shared_key, char** hash) {
    LOG_START("hash_shared_key");

    unsigned char digest[SHA256_DIGEST_LENGTH];
    SHA256((unsigned char*)shared_key, strlen(shared_key), digest);

    *hash = (char*)OPENSSL_malloc(SHA256_DIGEST_LENGTH * 2 + 1);
    for (int i = 0; i < SHA256_DIGEST_LENGTH; i++) {
        sprintf_s(*hash + i * 2, 3, "%02x", digest[i]);
    }

    LOG_END("hash_shared_key");
}

void free_memory(char* ptr) {
    LOG_START("free_memory");
    OPENSSL_free(ptr);
    LOG_END("free_memory");
}
