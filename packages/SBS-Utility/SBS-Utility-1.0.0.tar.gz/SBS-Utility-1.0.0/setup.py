from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="SBS-Utility",
    version="1.0.0",
    author="Suraj Singh",
    author_email="surajsingh04092002@gmail.com",
    description="A utility for text manipulation, compression, and task management.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SinghSuraj-04092002/IN_Utility.git",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "your-utility = your_utility.script:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
