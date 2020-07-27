import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="noolite2mqtt",
    version="0.1.0",
    author="Uladzislau Vasilyeu",
    author_email="vasvlad@gmail.com",
    description="NooLite to MQTT bridge",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vasvlad/noolite2mqtt",
    keywords="noolite mqtt",
    packages=['noolite2mqtt'],
    install_requires=[
        'NooLite_F',
    ],
    scripts=[
        'noolite2mqtt/noolite2mqtt.py',
    ],
    entry_points={
    },
    classifiers=[
        "Development Status :: 1 - Beta",
        "Topic :: Home Automation",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
