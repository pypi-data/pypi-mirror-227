import setuptools

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "bodycr",
    version = "1.0.0",
    author = "Lucas de Oliveira Barros Modesto",
    author_email = "lucas.barros1804@gmail.com",
    description = "Body Capture and Recognition",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/BodyCR/bodycr",
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages = ["bodycr"],
    python_requires = ">=3.0"
)
