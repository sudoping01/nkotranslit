

# nkotranslit

[![PyPI](https://img.shields.io/pypi/v/nkotranslit.svg)](https://pypi.org/project/nkotranslit/)
[![Python Versions](https://img.shields.io/pypi/pyversions/nkotranslit.svg)](https://pypi.org/project/nkotranslit/)
[![License](https://img.shields.io/pypi/l/nkotranslit.svg)](https://github.com/sudoping01/nkotranslit/blob/main/LICENSE)


A lightweight Python package for bidirectional **Latin ↔ N'Ko transliteration** 

## Features
- Convert Latin script to N'Ko  
- Convert N'Ko script to Latin  
- Command-line interface (CLI)  
- Graphical User Interface (GUI)


## GUI Requirement

The GUI requires Tkinter, which must be installed at system level.

On Ubuntu/Debian:
```bash 
    sudo apt install python3-tk
```

## Installation

```bash
pip install nkotranslit
````

## Usage

```python
from nkotranslit import NkoLatinConverter

converter = NkoLatinConverter()

text = "i ye san joli ye"
print(converter.convert_text(text, converter.LATIN_TO_NKO_RULES))

nko = "ߌ ߦߋ ߛߊ߲ ߖߏߟߌ ߦߋ"
print(converter.convert_text(nko, converter.NKO_TO_LATIN_RULES))
```

### CLI

```bash
latin2nko "i ye san joli ye"
nko2latin "ߌ ߦߋ ߛߊ߲ ߖߏߟߌ ߦߋ"
```

### GUI

Launch the graphical interface:
```bash
nkotranslit-gui
```

This opens a simple window where you can type text and convert between:
- Latin → N'Ko
- N'Ko → Latin




