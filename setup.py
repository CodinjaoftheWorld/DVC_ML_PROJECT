from setuptools import setup

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="src",
    version="0.0.1",
    author="CodinjaoftheWorld",
    description="Package of dvc ml pipeline for bank note authentication",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CodinjaoftheWorld/DVC_ML_PROJECT",
    author_email="gauravsaini.728@gmail.com",
    package=["src"],
    python_requires=">=3.7",
    install_requires=[
        'dvc',
        'pandas',
        'scikit-learn'
    ]

)
