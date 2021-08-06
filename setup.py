import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="consolet",
    version="0.0.1",
    author="Ali Nazari",
    author_email="alinazarigh110@gamil.com",
    description="Create your console applications easy and powerful 💥",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mr-nazari/Consolet",
    project_urls={
        "Github": "https://github.com/mr-nazari/Consolet",
        "Bug Tracker": "https://github.com/mr-nazari/Consolet/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "colorama",
        "pywin32",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
