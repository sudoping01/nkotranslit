from setuptools import setup, find_packages

setup(
    name="nkotranslit",    
    version="0.1.0",
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
        "Programming Language :: Python :: 3",
        "Natural Language :: Bambara",
        "Natural Language :: N'Ko",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Topic :: Text Processing :: Linguistic",
    ],
)
