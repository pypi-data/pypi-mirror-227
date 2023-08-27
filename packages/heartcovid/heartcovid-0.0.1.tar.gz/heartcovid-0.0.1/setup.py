import setuptools

with open("README.md", "r",encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="heartcovid",
    version="0.0.1",
    author="Izuru Inose",
    author_email="i.inose0304@gmail.com",
    description="Various numerical output and graphing software related to heart disease and Covid-19",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/i-inose/heartcovid",
    project_urls={
        "Bug Tracker":
            "https://github.com/i-inose/heartcovid",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    py_modules=['heartcovid'],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
    entry_points = {
        'console_scripts': [
            'heartcovid = heartcovid:main'
        ]
    },
)