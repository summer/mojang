import setuptools

with open("README.md") as f:
    long_description = f.read()

required_modules = ["requests>=2.27.0,<3"]

setuptools.setup(
    name="mojang",
    version="1.0.1",
    author="summer",
    description="A Python wrapper for the Mojang API and Minecraft website",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/summer/mojang",
    packages=setuptools.find_packages(),
    install_requires=required_modules,
    license="MIT",
    keywords=["mojang", "minecraft", "api", "mojang api", "minecraft api"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
    python_requires=">=3.7",
)
