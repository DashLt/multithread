import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="multithread",
    version="1.0",
    author="DashLt",
    description="An optionally asynchronous multithreaded downloader for python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DashLt/multithread",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Framework :: AsyncIO",
        "Topic :: Internet :: WWW/HTTP"
    ],
    python_requires=">3.5",
    install_requires=['aiohttp', 'aiofile'],
    extras_require={
        "progress": "tqdm"
    }
)