from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="nkotranslit",    
    version="1.1.1",
    description="A bidirectional Latin ↔ N'Ko transliteration library for Bamanankan.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="sudopnig01, Allasera Tapo et al",
    author_email="sudopnig01@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.7",
    install_requires=[
       "customtkinter"
    ],
    entry_points={
        "console_scripts": [
            "latin2nko=nkotranslit.cli:latin_to_nko_cli",
            "nko2latin=nkotranslit.cli:nko_to_latin_cli",
            "nkotranslit-gui=nkotranslit.cli:launch_gui_cli",
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