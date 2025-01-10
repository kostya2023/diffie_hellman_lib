import ctypes
import os
import platform

# Определение системы и архитектуры
system = platform.system()  # Проверяем, это Linux
arch = platform.machine()   # Определяем архитектуру системы: x86, x64, ARM

# Выбираем правильные библиотеки в зависимости от системы и архитектуры
if system == "Linux":
    if arch in ["x86_64", "AMD64"]:
        helm_lib_name = "dif_helm_x64.so"
    elif arch in ["i386", "i686"]:
        helm_lib_name = "dif_helm_x86.so"
    elif "arm" in arch:
        if "64" in arch:  # ARM64
            helm_lib_name = "dif_helm_arm64.so"
        else:  # ARMv7 или ARM32
            helm_lib_name = "dif_helm_armv7.so"
    else:
        raise OSError(f"Unsupported architecture: {arch}")
else:
    raise OSError(f"Unsupported operating system: {system}")

# Определение пути к библиотеке
base_path = os.path.dirname(__file__)
helm_lib_path = os.path.join(base_path, helm_lib_name)

# Загрузка библиотеки
try:
    dif_helm = ctypes.CDLL(helm_lib_path)
    print(f"Loaded {helm_lib_name} successfully!")
except OSError as e:
    raise OSError(f"Failed to load {helm_lib_name}: {e}")

# Определение аргументов и возвращаемых типов функций
dif_helm.generate_p_g_a.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_char_p), ctypes.POINTER(ctypes.c_char_p), ctypes.POINTER(ctypes.c_char_p)]
dif_helm.generate_p_g_a.restype = None

dif_helm.generate_b.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_char_p)]
dif_helm.generate_b.restype = None

dif_helm.generate_A.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_char_p)]
dif_helm.generate_A.restype = None

dif_helm.generate_shared_key.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_char_p)]
dif_helm.generate_shared_key.restype = None

dif_helm.hash_shared_key.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_char_p)]
dif_helm.hash_shared_key.restype = None

dif_helm.free_memory.argtypes = [ctypes.c_char_p]
dif_helm.free_memory.restype = None

# Вспомогательная функция для освобождения памяти
def free_memory(ptr):
    if ptr:
        dif_helm.free_memory(ptr)

# Враппер функций
def generate_p_g_a(bits):
    p = ctypes.c_char_p()
    g = ctypes.c_char_p()
    a = ctypes.c_char_p()
    dif_helm.generate_p_g_a(bits, ctypes.byref(p), ctypes.byref(g), ctypes.byref(a))
    p_value = p.value.decode() if p else None
    g_value = g.value.decode() if g else None
    a_value = a.value.decode() if a else None
    free_memory(p)
    free_memory(g)
    free_memory(a)
    return int(p_value), int(g_value), int(a_value)

def generate_b(p, g):
    p = str(p)
    g = str(g)
    b = ctypes.c_char_p()
    dif_helm.generate_b(p.encode(), g.encode(), ctypes.byref(b))
    b_value = b.value.decode() if b else None
    free_memory(b)
    return int(b_value)

def generate_A(p, g, a):
    p = str(p)
    g = str(g)
    a = str(a)
    A = ctypes.c_char_p()
    dif_helm.generate_A(p.encode(), g.encode(), a.encode(), ctypes.byref(A))
    A_value = A.value.decode() if A else None
    free_memory(A)
    return int(A_value)

def generate_shared_key(A, p, g, b):
    A = str(A)
    p = str(p)
    g = str(g)
    b = str(b)
    shared_key = ctypes.c_char_p()
    dif_helm.generate_shared_key(A.encode(), p.encode(), g.encode(), b.encode(), ctypes.byref(shared_key))
    shared_key_value = shared_key.value.decode() if shared_key else None
    free_memory(shared_key)
    return str(shared_key_value)

def hash_shared_key(shared_key):
    hashed_key = ctypes.c_char_p()
    dif_helm.hash_shared_key(shared_key.encode(), ctypes.byref(hashed_key))
    hashed_key_value = hashed_key.value.decode() if hashed_key else None
    free_memory(hashed_key)
    return str(hashed_key_value)

# Пример использования
if __name__ == "__main__":
    print("Generating p, g, a...")
    p, g, a = generate_p_g_a(2048)
    print(f"p: {p}")
    print(f"g: {g}")
    print(f"a: {a}")

    print("\nGenerating b...")
    b = generate_b(p, g)
    print(f"b: {b}")

    print("\nGenerating A...")
    A = generate_A(p, g, a)
    print(f"A: {A}")

    print("\nGenerating shared key...")
    shared_key = generate_shared_key(A, p, g, b)
    print(f"Shared Key: {shared_key}")

    print("\nHashing shared key...")
    hashed_key = hash_shared_key(shared_key)
    print(f"Hashed Key: {hashed_key}")
