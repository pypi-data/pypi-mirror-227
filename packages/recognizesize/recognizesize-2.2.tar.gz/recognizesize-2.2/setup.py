from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = ["matplotlib", "numpy", "opencv-contrib-python", "Pillow",
                "torch", "torchvision"]

setup(
    name="recognizesize",
    version="2.2",
    author="Maxim Laptev",
    author_email="maks-laptev.03@mail.ru",
    description="A package to recognize size of your body in format XS/S/M/L/XL",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/Reflect-Me/recognize-size",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)