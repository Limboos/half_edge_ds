from setuptools import setup, find_packages

setup(
    name="half_edge",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.21.0",
        "scipy>=1.7.0",
        "matplotlib>=3.4.0",
        "PyQt6>=6.2.0",
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="A Python implementation of the Half-Edge data structure",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/half_edge",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
) 