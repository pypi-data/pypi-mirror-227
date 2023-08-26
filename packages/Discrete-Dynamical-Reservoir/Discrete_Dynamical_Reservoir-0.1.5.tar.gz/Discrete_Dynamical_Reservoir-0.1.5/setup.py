import os

from setuptools import find_packages, setup

URL = "https://github.com/matteo-789/Discrete-Dynamical-Reservoir/"

if __name__ == "__main__":
    setup(
        name="Discrete_Dynamical_Reservoir",
        version="0.1.5",
        author="Matteo Cisneros",
        description="Use of discrete dynamical systems within recurrent neural networks",
        long_description="Python library to build and use discrete dynamical systems within recurrent neural networks. This library is a user-friendly tool made to use discrete dynamical systems such as Binary ECA, 3 states ECA and CML as a reservoir. Each type of reservoir has its hyper-parameters to enhance the reservoir performance.",
        url=URL,
        packages=find_packages(),
        classifiers=[
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python",
            "Topic :: Scientific/Engineering",
            "Operating System :: Microsoft :: Windows",
            "Operating System :: POSIX",
            "Operating System :: Unix",
            "Operating System :: MacOS",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
        ],
        python_requires=">=3.6",
    )
