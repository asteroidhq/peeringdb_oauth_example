import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="peeringdb_oauth",
    version="0.0.1",
    author="Andy Davidson",
    author_email="andy@asteroidhq.com",
    description="Example which implements PeeringDB's OAuth 2.0 service",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/asteroidhq/peeringdb_oauth_example",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
