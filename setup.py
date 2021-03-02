import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="qfa",
    version="0.1.0",
    author="Gustaw Lippa",
    author_email="glippa@student.agh.edu.pl",
    description="Quantum Finite Automata simulators",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gustawlippa/qfa",
    packages=setuptools.find_packages(include=["qfa", "qfa.*"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'cycler',
        'kiwisolver',
        'matplotlib',
        'numpy',
        'pyparsing',
        'python-dateutil',
        'scipy',
        'six',
      ],
    python_requires='>=3.6',
)