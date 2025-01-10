// utils.h
#ifndef UTILS_H
#define UTILS_H

#include <openssl/bn.h>
#include <string>

// Функции генерации
void generate_p_g_a(int bits, BIGNUM** p, BIGNUM** g, BIGNUM** a);
void generate_b(const BIGNUM* p, const BIGNUM* g, BIGNUM** b);
void generate_A(const BIGNUM* p, const BIGNUM* g, const BIGNUM* a, BIGNUM** A);
void generate_shared_key(const BIGNUM* A, const BIGNUM* p, const BIGNUM* g, const BIGNUM* b, BIGNUM** shared_key);

// Кеширование
void clear_prime_cache();

// Хэширование
std::string hash_shared_key(const BIGNUM* shared_key);

#endif // UTILS_H
