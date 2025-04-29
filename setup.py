from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="passengen",
    version="0.1.0",
    author="Polina Moshenets",
    author_email="",
    description="A secure, offline password generator CLI tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/passengen",
    packages=find_packages(),
    py_modules=["passengen"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Topic :: Security",
        "Topic :: Utilities",
    ],
    python_requires=">=3.10",
    install_requires=[
        "colorama>=0.4.4",
    ],
    entry_points={
        "console_scripts": [
            "passengen=passengen:main",
        ],
    },
)
