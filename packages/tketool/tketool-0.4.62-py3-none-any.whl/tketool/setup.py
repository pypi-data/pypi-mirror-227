import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("Version.txt", "r") as fh:
    version = fh.read()

setuptools.setup(
    name="tketool",
    version=version,
    author="Ke",
    author_email="jiangke1207@icloud.com",
    description="Some base methods for developing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://www.example.com/~cschultz/bvote/",
    packages=setuptools.find_packages(),
    package_data={
        'tketool': ['pyml/trainerplugins/*.html'],
    },
    include_package_data=True,
    install_requires=['redis==4.5.4', 'paramiko', 'minio', 'seaborn', 'tabulate', 'prettytable', 'flask'],
    entry_points={
        'console_scripts': [
            'tketool=tketool.main:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
