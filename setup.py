import setuptools

setuptools.setup(
    name="tfhe",
    version="0.1",
    author="Ayoub Benaissa",
    description="TFHE implementation",
    long_description="",
    long_description_content_type="text/markdown",
    url="https://github.com/youben11/TFHE",
    packages=setuptools.find_packages(include=["tfhe", "tfhe.*"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
