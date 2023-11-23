from setuptools import setup
from setuptools import find_packages

PACKAGE = {}
with open("src/stone/package.py", "r", encoding="utf-8") as fp:
    exec(fp.read(), PACKAGE)

with open("README.md", "r", encoding="utf-8") as f:
    LONG_DESCRIPTION = f.read()

setup(
    name=PACKAGE["__package_name__"],
    version=PACKAGE["__version__"],
    description="An easy-to-use library for skin tone classification",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages("src"),
    package_dir={"": "src"},
    zip_safe=False,
    author="Chenglong Ma",
    author_email="chenglong.m@outlook.com",
    keywords="skin-tone image-recognition face-detection",
    url="https://chenglongma.com/SkinToneClassifier/",
    project_urls={
        "Documentation": "https://chenglongma.com/SkinToneClassifier/",
        "Code": "https://github.com/ChenglongMa/SkinToneClassifier",
        "Issue tracker": "https://github.com/ChenglongMa/SkinToneClassifier/issues",
    },
    entry_points={
        "console_scripts": ["stone = stone.__main__:main"],
    },
    install_requires=[
        "opencv-python>=4.6.0.66",
        "numpy>=1.21.5",
        "colormath>=3.0.0",
        "tqdm>=4.64.0",
        "colorama>=0.4.6",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Image Recognition",
        "Topic :: Scientific/Engineering :: Image Processing",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Environment :: Win32 (MS Windows)",
        "Environment :: MacOS X",
        "Environment :: Other Environment",
    ],
)
