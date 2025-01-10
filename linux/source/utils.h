#ifndef UTILS_H
#define UTILS_H

#include <string>

extern "C" {
    void generate_p_g_a(int bits, char** p, char** g, char** a);
    void generate_b(const char* p, const char* g, char** b);
    void generate_A(const char* p, const char* g, const char* a, char** A);
    void generate_shared_key(const char* A, const char* p, const char* g, const char* b, char** shared_key);
    void hash_shared_key(const char* shared_key, char** hash);
    void free_memory(char* ptr);
}

#endif // UTILS_H
