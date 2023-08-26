from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent.resolve()
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name='bodycr',
    version='1.0.2',
    description='Body Capture and Recognition',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Lucas de Oliveira Barros Modesto',
    author_email='lucas.barros1804@gmail.com',
    url="https://github.com/BodyCR/bodycr",
    license="MIT",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    include_package_data=True,
    #package_data={
    #    '': ["Base.py","cert.pem","key.pem"]
    #},
    install_requires=[
        'tensorflow',
        'mediapipe',
        'opencv-python',
        'numpy'
    ],
    python_requires=">=3, <4",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ]
)