from setuptools import setup, find_packages

setup(
    name="cryptanalysis",
    version="0.0.2",
    packages=find_packages(),
    author="Himanshu Sheoran",
    description="Automated cryptanalysis library for substitution permutation network",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/deut-erium/auto-cryptanalysis",
    license="GPL",
    install_requires=[
        "z3-solver",
        "tqdm"
    ],
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    include_package_data=True,
    python_requires=">=3.6",
)




