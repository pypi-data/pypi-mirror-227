from setuptools import setup, find_packages

with open('README.md','r') as file:
    long_desc = file.read()

setup(
    name = "AniDSAKit",
    version = "0.1.0",
    author = "Anirudhra rao",
    author_email = "raorudhra16@gmail.com",
    description = "This DSAkit package contains searching algorithm",
    long_description = long_desc,
    url = 'https://github.com/Anirudhrarao/DSAkit',
    packages = find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)