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
    description=PACKAGE["__description__"],
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    author=PACKAGE["__author__"],
    author_email=PACKAGE["__author_email__"],
    keywords="skin-tone image-recognition face-detection",
    url=PACKAGE["__url__"],
    project_urls={
        "Documentation": PACKAGE["__code__"],
        "Code": PACKAGE["__code__"],
        "Issue tracker": PACKAGE["__issues__"],
    },
    entry_points={
        "console_scripts": ["stone = stone.__main__:main"],
    },
    python_requires=">=3.9",
    install_requires=[
        "opencv-python>=4.9.0.80",
        "numpy>=1.21.5",
        "colormath>=3.0.0",
        "tqdm>=4.64.0",
        "colorama>=0.4.6",
        "packaging>=23.1",
        "requests>=2.31.0",
        "gooey>=1.0.8.1",
        "re-wx==0.0.10",
        "colored==1.3.93",
    ],
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
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
