from setuptools import setup, find_packages

setup(
    name="trendup-python-lib",
    version="0.1.3",

    author="JerryLin",
    author_email="jerry.lin@keeptossinglab.com",
    packages=find_packages(),
    include_package_data=True,
    url="https://www.keeptossinglab.com/trendup-me",
    description="trendup library",
    install_requires=[
        "attrs",
        "pyyaml",
        "numpy",
        "opencv-python",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
