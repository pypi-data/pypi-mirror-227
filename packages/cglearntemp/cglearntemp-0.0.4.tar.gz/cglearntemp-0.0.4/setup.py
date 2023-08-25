from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as readme_file:
    long_description = readme_file.read()

setup(
    name="cglearntemp",
    version="0.0.4",
    author="Mohammad Ali Javidian, Shantanu Deore",
    author_email="javidianma@appstate.edu, shantanudeore223@gmail.com",
    description="cglearn is a Python library that aims to spark probabilistic reasoning and analysis via chain graphs.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/majavid/cglearn",
    packages=find_packages(where="cglearntemp"),
    package_dir={"": "cglearntemp"},
    package_data={
        "" : ["*.csv", "*.dll", "*.so"],
        "cglearntemp" : ["*.csv", "*.dll", "*.so"],
    },
    include_package_data=True,
    install_requires=[
        "numpy",
        "networkx",
        "matplotlib",
        "pandas",
        "igraph",
        "scipy",
    ],
    extras_require={
        "extras": [
            # List your optional dependencies here
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
