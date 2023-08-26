from setuptools import setup, find_packages

setup(
    name="llama2-terminal",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "inquirer",
        "cmd2",
        "farm-haystack",
        "torch",
        "transformers>=4.0.0",
        "bitsandbytes>=3.9.0",
        "pyyaml"
    ],
    author="SamthinkGit",
    author_email="sebastianmayorquin@gmail.com",
    description="Descripción breve del proyecto",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/SamthinkGit/llama2-terminal",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
