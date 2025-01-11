import os
from setuptools import setup, find_packages
from setuptools.command.install import install
import shutil

class CustomInstallCommand(install):
    """Custom installation command to handle library selection and copying."""
    def run(self):
        libs = ["dif_helm_arm64.so",
                "dif_helm_armv7.so",
                "dif_helm_x64.dll",
                "dif_helm_x64.so",
                "dif_helm_x86.dll",
                "dif_helm_x86.so",
                "libcrypto-3-x64.dll",
                "libcrypto-3.dll"]
        
        # Copy libraries to the target installation directory
        target_libs_dir = os.path.join(self.install_lib, "diffiehellmanlib", "libs")
        os.makedirs(target_libs_dir, exist_ok=True)
        
        for lib in libs:
            lib_path = "./diffiehellmanlib/" + "libs/" + lib
            shutil.copy(lib_path, target_libs_dir)
            print(f"Library installed: {lib} -> {target_libs_dir}")

        # Continue with standard installation
        super().run()

# Read the contents of README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='diffiehellmanlib',
    version='1.6a1',
    description='Simplified number generation library for the Diffie-Hellman protocol.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Konstantin Gorshkov',
    author_email='kostya_gorshkov_06@vk.com',
    url='https://github.com/kostya2023/diffie_hellman_lib',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        '': ['diffiehellmanlib/libs/*.dll', 'diffiehellmanlib/libs/*.so'],  # Include all required libraries
    },
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
