import ctypes
import os
import platform

def load_library():
    """
    Загружает соответствующую библиотеку в зависимости от ОС и архитектуры.
    """
    system = platform.system()
    arch = platform.machine()

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
            lib_name = "dif_helm_arm64.so" if "64" in arch else "dif_helm_armv7.so"
        else:
            raise OSError(f"Unsupported architecture: {arch}")
    else:
        raise OSError(f"Unsupported operating system: {system}")

    base_path = os.path.dirname(__file__)
    lib_path = os.path.join(base_path, "libs", lib_name)

    try:
        library = ctypes.CDLL(lib_path)
        print(f"Loaded library: {lib_name}")
        return library
    except OSError as e:
        raise OSError(f"Failed to load library {lib_name}: {e}")

# Загрузка библиотеки
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

# Функции-обёртки
def generate_p_g(bits: int):
    """
    Генерирует параметры p и g для алгоритма Диффи-Хеллмана.

    :param bits: Размер p в битах.
    :return: Кортеж (p, g).
    :raises ValueError: Если bits не является положительным целым числом.
    """
    if not isinstance(bits, int) or bits <= 0:
        raise ValueError(f"Parameter 'bits' must be a positive integer. Received: {bits}")

    p = ctypes.c_char_p()
    g = ctypes.c_char_p()
    a = ctypes.c_char_p()
    try:
        dif_helm.generate_p_g_a(bits, ctypes.byref(p), ctypes.byref(g), ctypes.byref(a))
        return int(p.value), int(g.value)
    finally:
        free_memory(p)
        free_memory(g)
        free_memory(a)

def generate_a_or_b(p, g):
    """
    Генерирует секретное число a или b.

    :param p: Простое число p.
    :param g: Основание g.
    :return: Секретное число a или b.
    :raises ValueError: Если p или g некорректны.
    """
    if not isinstance(p, int) or not isinstance(g, int):
        raise ValueError(f"Both p and g must be integers. Received: p={type(p)}, g={type(g)}")
    if p <= 0 or g <= 0:
        raise ValueError(f"Both p and g must be positive integers. Received: p={p}, g={g}")

    b = ctypes.c_char_p()
    try:
        dif_helm.generate_b(str(p).encode(), str(g).encode(), ctypes.byref(b))
        return int(b.value)
    finally:
        free_memory(b)

def generate_A_or_B(p, g, a):
    """
    Генерирует публичный ключ A или B.

    :param p: Простое число p.
    :param g: Основание g.
    :param a: Секретное число a.
    :return: Публичный ключ A или B.
    :raises ValueError: Если входные параметры некорректны.
    """
    if not all(isinstance(x, int) for x in [p, g, a]):
        raise ValueError(f"Parameters p, g, and a must be integers. Received: p={type(p)}, g={type(g)}, a={type(a)}")
    if p <= 0 or g <= 0 or a <= 0:
        raise ValueError(f"Parameters p, g, and a must be positive integers. Received: p={p}, g={g}, a={a}")

    A = ctypes.c_char_p()
    try:
        dif_helm.generate_A(str(p).encode(), str(g).encode(), str(a).encode(), ctypes.byref(A))
        return int(A.value)
    finally:
        free_memory(A)

def generate_shared_key(A, p, g, b):
    """
    Генерирует общий секретный ключ.

    :param A: Публичный ключ другой стороны.
    :param p: Простое число p.
    :param g: Основание g.
    :param b: Секретное число b.
    :return: Общий секретный ключ.
    :raises ValueError: Если входные параметры некорректны.
    """
    if not all(isinstance(x, int) for x in [A, p, g, b]):
        raise ValueError(f"Parameters A, p, g, and b must be integers. Received: A={type(A)}, p={type(p)}, g={type(g)}, b={type(b)}")
    if any(x <= 0 for x in [A, p, g, b]):
        raise ValueError(f"Parameters A, p, g, and b must be positive integers. Received: A={A}, p={p}, g={g}, b={b}")

    shared_key = ctypes.c_char_p()
    try:
        dif_helm.generate_shared_key(str(A).encode(), str(p).encode(), str(g).encode(), str(b).encode(), ctypes.byref(shared_key))
        return int(shared_key.value)
    finally:
        free_memory(shared_key)

def hash_shared_key(shared_key):
    """
    Хеширует общий секретный ключ.

    :param shared_key: Общий секретный ключ.
    :return: Хеш ключа в виде строки.
    :raises ValueError: Если shared_key некорректен.
    """
    if not isinstance(shared_key, int) or shared_key <= 0:
        raise ValueError(f"Parameter 'shared_key' must be a positive integer. Received: {shared_key}")

    hashed_key = ctypes.c_char_p()
    try:
        dif_helm.hash_shared_key(str(shared_key).encode(), ctypes.byref(hashed_key))
        return hashed_key.value.decode()
    finally:
        free_memory(hashed_key)
