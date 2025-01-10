import os
import platform
from setuptools import setup, find_packages
from setuptools.command.install import install

class CustomInstallCommand(install):
    """Кастомная команда для проверки архитектуры и ОС."""
    def run(self):
        system = platform.system()
        arch = platform.machine()

        if system == "Windows":
            if arch in ["AMD64", "x86_64"]:
                lib_name = "dif_helm_x64.dll"
            elif arch in ["i386", "i686"]:
                lib_name = "dif_helm_x86.dll"
            else:
                raise RuntimeError(f"Ошибка: неподдерживаемая архитектура Windows: {arch}")
        elif system == "Linux":
            if arch in ["AMD64", "x86_64"]:
                lib_name = "dif_helm_x64.so"
            elif arch in ["i386", "i686"]:
                lib_name = "dif_helm_x86.so"
            elif "arm" in arch:
                if "64" in arch:
                    lib_name = "dif_helm_arm64.so"
                else:
                    lib_name = "dif_helm_armv7.so"
            else:
                raise RuntimeError(f"Ошибка: неподдерживаемая архитектура Linux: {arch}")
        else:
            raise RuntimeError(f"Ошибка: неподдерживаемая операционная система: {system}")

        print(f"Установлена библиотека: {lib_name}")
        install.run(self)

# Чтение содержимого README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='diffie-hellman-lib',
    version='1.5.1',
    description='Библиотека упрошённой генерации чисел для протокола Diffie_Hellman =)',
    long_description=long_description,
    long_description_content_type="text/markdown",  # Указывает формат Markdown
    author='Konstantin Gorshkov',
    author_email='kostya_gorshkov_06@vk.com',
    url='https://github.com/kostya2023/diffie_hellman_lib',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: Implementation :: CPython',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
    ],
    python_requires='>=3.6',
    cmdclass={
        'install': CustomInstallCommand,
    },
)
