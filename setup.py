from setuptools import setup, find_packages

setup(
    name="nkotranslit",    
    version="1.0.0",
    description="A bidirectional Latin ↔ N'Ko transliteration library for Bamanankan.",
    author="sudopnig01@gmail.com",
    author_email="sudopnig01@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.7",
    install_requires=[
        # No external dependencies for now
    ],
    entry_points={
        "console_scripts": [
            "latin2nko=nkotranslit.cli:latin_to_nko_cli",
            "nko2latin=nkotranslit.cli:nko_to_latin_cli",
        ]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
         "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],

)