import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="txrrc_data_harvest",
    version="0.0.1",
    url="https://github.com/mlbelobraydi/TXRRC_data_harvest",
    author="mlbelobraydi",
    maintainer="mlbelobraydi",
    license="The Unlicense",
    description="Tools for working with oil and gas well data from the Texas Railroad Commission",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: UnLicense",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
    ],
    # packages=["txrrc_data_harvest"],
    # install_requires=[],
    python_requires='>=3',
)
