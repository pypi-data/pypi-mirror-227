import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name="central_system",
    version="1.0.2",
    author="centralSystem.org",
    author_email="opensource@centralSystem.org",
    description="retrieve data from centralSystem.org",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'requests',
        'pandas',
        'httpx',
        'logging'
    ],
    python_requires='>=3',
)