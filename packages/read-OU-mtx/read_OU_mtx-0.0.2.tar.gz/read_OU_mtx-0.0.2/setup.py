import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="read_OU_mtx",
    version="0.0.2",
    author="Wangchen",
    author_email="wch_bioinformatics@163.com",
    description="read single cell raw data in C4 platform .",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wangzichenbioinformatics/read_ou_mtx/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)
