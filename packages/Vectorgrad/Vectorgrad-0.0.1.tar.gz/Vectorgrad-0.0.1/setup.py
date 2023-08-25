import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Vectorgrad",
    version="0.0.1",
    author="Sina Hazeghi",
    author_email="shazeghian@gmail.com",
    description="A lightweight autograd engine that supports tensor operations and gradients with a small, customizable neural network library on top",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Sina-Haz/VectorGrad",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)