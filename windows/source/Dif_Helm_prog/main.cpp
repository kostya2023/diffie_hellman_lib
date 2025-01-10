#include "utils.h"
#include <iostream>
#include <chrono>
#include <limits> // Для проверки ввода

int main() {
    BIGNUM* p = nullptr, * g = nullptr, * a = nullptr, * b = nullptr, * A = nullptr, * shared_key = nullptr;

    // Запрос ввода размера ключа p
    int bit_size = 0;
    while (true) {
        std::cout << "Enter the size of prime number p in bits (512 to 8192): ";
        std::cin >> bit_size;

        // Проверяем ввод
        if (std::cin.fail() || bit_size < 512 || bit_size > 8192) {
            std::cout << "Invalid input. Please enter a number between 512 and 8192." << std::endl;
            std::cin.clear();
            std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
        }
        else {
            break;
        }
    }

    // Замер общего времени
    auto total_start = std::chrono::high_resolution_clock::now();

    // Замер времени генерации p, g, a
    auto start = std::chrono::high_resolution_clock::now();
    generate_p_g_a(bit_size, &p, &g, &a);
    auto end = std::chrono::high_resolution_clock::now();
    std::cout << "Time to generate p, g, a: "
        << std::chrono::duration_cast<std::chrono::milliseconds>(end - start).count()
        << " ms" << std::endl;

    // Вывод значений
    std::cout << "p: " << BN_bn2dec(p) << std::endl;
    std::cout << "g: " << BN_bn2dec(g) << std::endl;
    std::cout << "a: " << BN_bn2dec(a) << std::endl;

    // Замер времени генерации b
    start = std::chrono::high_resolution_clock::now();
    generate_b(p, g, &b);
    end = std::chrono::high_resolution_clock::now();
    std::cout << "Time to generate b: "
        << std::chrono::duration_cast<std::chrono::milliseconds>(end - start).count()
        << " ms" << std::endl;

    // Замер времени генерации A
    start = std::chrono::high_resolution_clock::now();
    generate_A(p, g, a, &A);
    end = std::chrono::high_resolution_clock::now();
    std::cout << "Time to generate A: "
        << std::chrono::duration_cast<std::chrono::milliseconds>(end - start).count()
        << " ms" << std::endl;

    // Замер времени генерации общего ключа
    start = std::chrono::high_resolution_clock::now();
    generate_shared_key(A, p, g, b, &shared_key);
    end = std::chrono::high_resolution_clock::now();
    std::cout << "Time to generate shared key: "
        << std::chrono::duration_cast<std::chrono::milliseconds>(end - start).count()
        << " ms" << std::endl;

    // Хеширование общего ключа
    start = std::chrono::high_resolution_clock::now();
    std::string hashed_key = hash_shared_key(shared_key);
    end = std::chrono::high_resolution_clock::now();
    std::cout << "Time to hash shared key: "
        << std::chrono::duration_cast<std::chrono::milliseconds>(end - start).count()
        << " ms" << std::endl;

    // Вывод хэша
    std::cout << "Hashed shared key: " << hashed_key << std::endl;

    // Замер общего времени выполнения
    auto total_end = std::chrono::high_resolution_clock::now();
    std::cout << "Total time: "
        << std::chrono::duration_cast<std::chrono::milliseconds>(total_end - total_start).count()
        << " ms" << std::endl;

    // Освобождение памяти
    BN_free(p);
    BN_free(g);
    BN_free(a);
    BN_free(b);
    BN_free(A);
    BN_free(shared_key);

    clear_prime_cache();
    return 0;
}
