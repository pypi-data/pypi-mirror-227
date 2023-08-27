from setuptools import setup, find_packages

setup(
    name='camera-simulator-28-08-23',
    version='1.0.0',
    author="Daniel Beltran",
    author_email="dmbeltranr1@gmail.com",
    description="Package of a basic lens and sensor simulator",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Image Processing",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    install_requires=["numpy", "scikit-image", "pytest",],
    url="https://github.com/DanBeltranuwu/camera-simulator",
    download_url="https://github.com/DanBeltranuwu/camera-simulator/archive/refs/tags/Alpha.tar.gz",
)
