#ifndef UTILS_H
#define UTILS_H

#ifdef EXPORTING_DLL
#define DLL_API __declspec(dllexport)
#else
#define DLL_API __declspec(dllimport)
#endif

#include <string>

extern "C" {
    DLL_API void generate_p_g_a(int bits, char** p, char** g, char** a);
    DLL_API void generate_b(const char* p, const char* g, char** b);
    DLL_API void generate_A(const char* p, const char* g, const char* a, char** A);
    DLL_API void generate_shared_key(const char* A, const char* p, const char* g, const char* b, char** shared_key);
    DLL_API void hash_shared_key(const char* shared_key, char** hash);
    DLL_API void free_memory(char* ptr);
}

#endif // UTILS_H
