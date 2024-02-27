import setuptools

with open("README.txt", "r") as fh:
    long_description = fh.read()

VERSION = "0.0.1"

setuptools.setup(
    name="dowker",
    version=VERSION,
    author="Jongkook Choi",
    author_email="jongkook90@hotmail.com",
    description="Simplex tree for Dowker complex",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/thessal/dowker",
    packages=setuptools.find_packages(),
    python_requires='>=3.11.*',
    classifiers=[
        'Development Status :: 4 - Beta',
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    keywords='dowker complex simplex tree',
    install_requires=[
        "gudhi>=3.9.0"
      ],
    include_package_data=True
)