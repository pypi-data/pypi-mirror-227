import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="packaging_extrapolation",
    version="0.0.2",
    author="ZhaoKai Xi",
    author_email="xizaokaiz@foxmail.com",
    description="Extrapolation Methods in quantum chemistry",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/xizaokaiz/packaging_extrapolation.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"],
    python_requires='>=3.6',
)
