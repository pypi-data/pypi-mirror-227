from setuptools import setup, find_packages

setup(
    name="sbom-rule-diff",
    version="0.1.0",
    description="",
    author="williamfzc",
    author_email="williamfzc@foxmail.com",
    url="https://github.com/williamfzc/sbom-rule-diff",
    packages=find_packages(),
    include_package_data=True,
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.6",
    install_requires=["spdx_tools==0.8.1"],
)
