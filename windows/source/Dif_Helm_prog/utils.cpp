#include "utils.h"
#include <openssl/rand.h>
#include <openssl/sha.h>
#include <fstream>
#include <iostream>
#include <unordered_map>
#include <stdexcept> // Для обработки исключений

// Глобальный кеш для простых чисел
static std::unordered_map<int, BIGNUM*> prime_cache;

void generate_p_g_a(int bits, BIGNUM** p, BIGNUM** g, BIGNUM** a) {
    if (bits < 512 || bits > 8192) {
        throw std::invalid_argument("Invalid bit size. Must be between 512 and 8192.");
    }

    std::cout << "[INFO] Starting generate_p_g_a with bits = " << bits << std::endl;

    // Проверяем, есть ли p в кеше
    if (prime_cache.count(bits)) {
        std::cout << "[INFO] Found prime number in cache for bits = " << bits << std::endl;
        *p = BN_dup(prime_cache[bits]);
    }
    else {
        std::cout << "[INFO] Generating new prime number for bits = " << bits << std::endl;
        *p = BN_new();
        BN_generate_prime_ex(*p, bits, 1, nullptr, nullptr, nullptr);
        prime_cache[bits] = BN_dup(*p);
    }

    // Генерация g
    *g = BN_new();
    BN_set_word(*g, 2);
    std::cout << "[INFO] Generated g = 2" << std::endl;

    // Генерация a
    *a = BN_new();
    BIGNUM* range = BN_new();
    BN_sub(range, *p, BN_value_one());
    BN_rand_range(*a, range);
    BN_free(range);

    std::cout << "[INFO] Finished generate_p_g_a.\np: " << BN_bn2dec(*p)
        << "\ng: " << BN_bn2dec(*g) << "\na: " << BN_bn2dec(*a) << std::endl;
}

void generate_b(const BIGNUM* p, const BIGNUM* g, BIGNUM** b) {
    std::cout << "[INFO] Starting generate_b" << std::endl;
    *b = BN_new();
    BIGNUM* range = BN_new();
    BN_sub(range, p, BN_value_one());
    BN_rand_range(*b, range);
    BN_free(range);
    std::cout << "[INFO] Finished generate_b.\nb: " << BN_bn2dec(*b) << std::endl;
}

void generate_A(const BIGNUM* p, const BIGNUM* g, const BIGNUM* a, BIGNUM** A) {
    std::cout << "[INFO] Starting generate_A" << std::endl;
    *A = BN_new();
    BN_CTX* ctx = BN_CTX_new();
    BN_mod_exp(*A, g, a, p, ctx);
    BN_CTX_free(ctx);
    std::cout << "[INFO] Finished generate_A.\nA: " << BN_bn2dec(*A) << std::endl;
}

void generate_shared_key(const BIGNUM* A, const BIGNUM* p, const BIGNUM* g, const BIGNUM* b, BIGNUM** shared_key) {
    std::cout << "[INFO] Starting generate_shared_key" << std::endl;
    *shared_key = BN_new();
    BN_CTX* ctx = BN_CTX_new();
    BN_mod_exp(*shared_key, A, b, p, ctx);
    BN_CTX_free(ctx);
    std::cout << "[INFO] Finished generate_shared_key.\nShared key: " << BN_bn2dec(*shared_key) << std::endl;
}

std::string hash_shared_key(const BIGNUM* shared_key) {
    std::cout << "[INFO] Starting hash_shared_key" << std::endl;
    unsigned char hash[SHA256_DIGEST_LENGTH];
    unsigned char* key_bytes;
    int key_len = BN_num_bytes(shared_key);

    // Получение байтов общего ключа
    key_bytes = new unsigned char[key_len];
    BN_bn2bin(shared_key, key_bytes);

    // Хеширование с помощью SHA-256
    SHA256(key_bytes, key_len, hash);
    delete[] key_bytes;

    // Конвертация хэша в строку
    std::string hash_hex;
    for (int i = 0; i < SHA256_DIGEST_LENGTH; i++) {
        char buf[3];
        snprintf(buf, sizeof(buf), "%02x", hash[i]);
        hash_hex += buf;
    }

    std::cout << "[INFO] Finished hash_shared_key.\nHash: " << hash_hex << std::endl;
    return hash_hex;
}

void clear_prime_cache() {
    std::cout << "[INFO] Clearing prime cache" << std::endl;
    for (auto& entry : prime_cache) {
        BN_free(entry.second);
    }
    prime_cache.clear();
    std::cout << "[INFO] Prime cache cleared" << std::endl;
}
