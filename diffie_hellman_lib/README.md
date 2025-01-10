
# Diffie - Hellman Python/C++ libray

Описание: Это библиотека для генерирования чисел для использования криптографического протокола Diffie-Hellman. Испольуется C++ для максимальной (которой мне удалось достичь) скорости генерации p - больших простых чисел. Используется python wrapper (обёртка) чтобы использовать функции из .dll (для Windows) или из .so (для Linux). я не нашёл другого способа как можно из питона использовать C++ функции =).
## Обзор функций из `utils.h` и `utils.cpp`

### 1. **`generate_p_g_a`**
   - **Описание**: Генерирует параметры \( p \) (простое число), \( g \) (основание) и \( a \) (приватное число).
   - **Реализация**:
     - Проверяет размер бит (от 512 до 8192).
     - Ограничение было введено для безопасности, минимально 512 для тестов и проверок, в реальных задачах, минимум 1024 а лучше 2048 бит.
     - Использует кэш для ускорения генерации \( p \), если число для данного размера уже сгенерировано.
     - Устанавливает \( g \) как 2.
     - Случайно генерирует \( a \) в диапазоне от \( 1 \) до \( p-1 \).
   - **В Python-врапере**:
     - Функция обёрнута как `generate_p_g`.
     - Возвращаются только \( p \) и \( g \). \( a \) освобождается.

### 2. **`generate_b`**
   - **Описание**: Генерирует приватное число \( b \) или \( a \), как выводную цифру назовёте.
   - **Реализация**:
     - Принимает \( p \) и \( g \) как входные данные.
     - Генерирует \( b \) или \( a \) в диапазоне от \( 1 \) до \( p-1 \).
   - **В Python-врапере**:
     - Переименована в `generate_a_or_b`.
     - Универсальная функция для генерации либо \( a \), либо \( b \).

### 3. **`generate_A`**
   - **Описание**: Генерирует \( A \) на основе \( p \), \( g \) и \( a \), где \( A = g^a \mod p \), может аналогично генерировать \( B \), просто формула станет: \( B = g^b \mod p \)
   - **Реализация**:
     - Использует модульное экспоненциальное вычисление с помощью OpenSSL.
   - **В Python-врапере**:
     - Переименована в `generate_A_or_B`.
     - Универсальная функция для вычисления \( A \) или \( B \).

### 4. **`generate_shared_key`**
   - **Описание**: Генерирует общий ключ \( K \), используя \( A \), \( b \), \( p \), \( g \): \( K = A^b \mod p \), может также использовать и \( B \) с \( a \), также формула: \( K = B^a \mod p \)
   - **Реализация**:
     - Вычисляет общий ключ на основе предоставленных данных.
   - **В Python-врапере**:
     - Общий ключ сразу передаётся в `hash_shared_key` для хэширования.
     - Возвращается хэшированный ключ.

### 5. **`hash_shared_key`**
   - **Описание**: Хэширует общий ключ с помощью SHA-256.
   - **Реализация**:
     - Преобразует ключ в строку 16-ричного формата.
   - **В Python-врапере**:
     - Вызов производится из `generate_shared_key`.

### 6. **`free_memory`**
   - **Описание**: Освобождает выделенную память для строк.
   - **Реализация**:
     - Использует `OPENSSL_free` для предотвращения утечек памяти.
   - **В Python-врапере**:
     - Используется для освобождения памяти после вызова каждой функции.

## Дополнительные возможности Python-врапера

1. **Автоматическая загрузка библиотеки**:
   - Определяет необходимую версию библиотеки DLL/SO на основе архитектуры и операционной системы.
   - Поддерживаются Windows (x86, x64) и Linux (x86, x64, ARMv7, ARM64).

2. **Переименование функций**:
   - `generate_b` → `generate_a_or_b`.
   - `generate_A` → `generate_A_or_B`.
   - Это сделано для повышения универсальности функций.

3. **Автоматическое хэширование ключа**:
   - Логика изменена: теперь общий ключ сразу хэшируется в `generate_shared_key`.

4. **Управление памятью**:
   - Все строки, выделенные в C++, освобождаются с помощью `free_memory`, чтобы избежать утечек памяти.
## Использование/Примеры


1. Генерация параметров \( p \) и \( g \)

```python
from diffie_hellman_lib.wrapper import generate_p_g

# Генерация параметров с использованием 2048-битного ключа
p, g = generate_p_g(2048)
print(f"Generated p: {p}")
print(f"Generated g: {g}")
```
Результат:
Выводит значения \( p \) и \( g \), сгенерированные для криптографических операций.

---

2. Генерация приватного числа \( a \) или \( b \)
```python
from diffie_hellman_lib.wrapper import generate_a_or_b

# Пример значений p и g
p = 23  # Пример числа p
g = 5   # Пример числа g

# Генерация приватного числа a или b
private_value = generate_a_or_b(p, g)
print(f"Generated private value: {private_value}")
```
Возвращает случайное приватное число, используемое для генерации ключей.

---

3. Генерация значения \( A \) или \( B \)
```python
from diffie_hellman_lib.wrapper import generate_A_or_B

# Пример значений
p = 23
g = 5
a = 6  # Приватное число

# Генерация A или B
public_value = generate_A_or_B(p, g, a)
print(f"Generated public value: {public_value}")
```
Результат:
Возвращает значение \( A \) или \( B \).

---

4. Генерация общего ключа \( K \)
```python
from diffie_hellman_lib.wrapper import generate_shared_key

# Пример значений
A = 8
p = 23
g = 5
b = 15

# Генерация общего ключа
shared_key = generate_shared_key(A, p, g, b)
print(f"Generated shared key (hashed): {shared_key}")
```
Результат:
Возвращает общий ключ, который автоматически хэшируется с использованием SHA-256.

---

5. Хэширование ключа
```python
from diffie_hellman_lib.wrapper import hash_shared_key

# Пример общего ключа
shared_key = "123456"

# Хэширование общего ключа
hashed_key = hash_shared_key(shared_key)
print(f"Hashed key: {hashed_key}")
```
Результат:
Возвращает SHA-256-хэш переданного общего ключа.

---

# Пример полного использования

Логика Alice (первой стороны):
```python
from diffie_hellman_lib import wrapper

p, g = wrapper.generate_p_g(1024) # получаем p и g, p размером 1024 бит. (рекомендуемо 2048)

a = wrapper.generate_a_or_b(p, g) # генерируем собственный секретный ключ
A = wrapper.generate_A_or_B(p, g, a) # генерируем свой публичный ключ

# логика отправки p, g, A Bob-у (Второй стороне) и логика получения B От Bob-а (Второй стороны) например через https или сокеты...

shared_key = wrapper.generate_shared_key(B, p, g, a) # Получаем общий секретный ключ
print(shared_key) # выводим полученный ключ
```

Логика Bob (второй стороны):
```python
from diffie_hellman_lib import wrapper

# Логика получения от Alice чисел p, g, A...

b = wrapper.generate_a_or_b(p, g) # Генерируем свой секретный ключ
B = wrapper.generate_A_or_B(p, g, b) # генерируем свой публичный ключ

# Логика отправки B (публичного ключа), Alice (первой стороне) например через https или сокеты...

shared_key = wrapper.generate_shared_key(A, p, g, b) # Получаем  общий секретный ключ
print(shared_key) # выводим общий секретный ключ
```

Таким вот образом можно обменятся ключами шифрования между двумя сторонами по не зашифрованному каналу.


## Лицензия

[MIT](https://choosealicense.com/licenses/mit/)


## Авторы

- [kostya2023](https://github.com/kostya2023)
