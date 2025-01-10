import ctypes
import os
import platform

def load_library():
    # Определение архитектуры и системы
    system = platform.system()
    arch = platform.machine()

    # Определение имени библиотеки
    if system == "Windows":
        if arch in ["x86_64", "AMD64"]:
            lib_name = "dif_helm_x64.dll"
        elif arch in ["i386", "i686"]:
            lib_name = "dif_helm_x86.dll"
        else:
            raise OSError(f"Unsupported architecture: {arch}")
    elif system == "Linux":
        if arch in ["x86_64", "AMD64"]:
            lib_name = "dif_helm_x64.so"
        elif arch in ["i386", "i686"]:
            lib_name = "dif_helm_x86.so"
        elif "arm" in arch:
            if "64" in arch:  # ARM64
                lib_name = "dif_helm_arm64.so"
            else:  # ARMv7
                lib_name = "dif_helm_armv7.so"
        else:
            raise OSError(f"Unsupported architecture: {arch}")
    else:
        raise OSError(f"Unsupported operating system: {system}")

    # Определение пути к библиотеке
    base_path = os.path.dirname(__file__)
    lib_path = os.path.join(base_path, "libs", lib_name)

    # Загрузка библиотеки
    try:
        library = ctypes.CDLL(lib_path)
        print(f"Loaded library: {lib_name}")
        return library
    except OSError as e:
        raise OSError(f"Failed to load library {lib_name}: {e}")

# Загрузка нужной библиотеки
dif_helm = load_library()

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
def generate_p_g(bits:int):
    p = ctypes.c_char_p()
    g = ctypes.c_char_p()
    a = ctypes.c_char_p()
    dif_helm.generate_p_g_a(bits, ctypes.byref(p), ctypes.byref(g), ctypes.byref(a))
    p_value = p.value
    g_value = g.value
    free_memory(p)
    free_memory(g)
    free_memory(a)
    return int(p_value), int(g_value)

def generate_a_or_b(p, g):
    p = str(p)
    g = str(g)
    b = ctypes.c_char_p()
    dif_helm.generate_b(p.encode(), g.encode(), ctypes.byref(b))
    b_value = b.value
    free_memory(b)
    return int(b_value)

def generate_A_or_B(p, g, a):
    p = str(p)
    g = str(g)
    a = str(a)
    A = ctypes.c_char_p()
    dif_helm.generate_A(p.encode(), g.encode(), a.encode(), ctypes.byref(A))
    A_value = A.value
    free_memory(A)
    return int(A_value)

def hash_shared_key(shared_key):
    hashed_key = ctypes.c_char_p()
    dif_helm.hash_shared_key(shared_key.encode(), ctypes.byref(hashed_key))
    hashed_key_value = hashed_key.value
    free_memory(hashed_key)
    return str(hashed_key_value.decode())

def generate_shared_key(A, p, g, b):
    A = str(A)
    p = str(p)
    g = str(g)
    b = str(b)
    shared_key = ctypes.c_char_p()
    dif_helm.generate_shared_key(A.encode(), p.encode(), g.encode(), b.encode(), ctypes.byref(shared_key))
    shared_key_value = shared_key.value
    free_memory(shared_key)
    return hash_shared_key(shared_key_value)
