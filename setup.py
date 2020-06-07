import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="qapi",
    version="0.0.1",
    author="Diego Peres",
    author_email="speres.diego@gmail.com",
    description="QAPI - API query language",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Zeon-Code/qapi",
    install_requires=[
          'sqlalchemy',
    ],
    packages=setuptools.find_packages(),
    keywords=["qapi", "API", "Query Language"],
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3.6',
)