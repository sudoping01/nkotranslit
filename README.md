


# nkotranslit

A simple Python library for bidirectional **Latin ↔ N'Ko transliteration** 

## Features

- Convert Latin script to N'Ko.
- Convert N'Ko script to Latin.
- Command-line interface for quick use.

## Installation

```bash
pip install nkotranslit
````

## Usage

### Python

```python
from nkotranslit import Latin2Nko, Nko2Latin

converter = Latin2Nko()
print(converter.convert("i ye san joli ye"))

converter2 = Nko2Latin()
print(converter2.convert("ߌ ߦߋ ߛߊ߲ ߖߏߟߌ ߦߋ"))
```

### CLI

```bash
latin2nko "i ye san joli ye"
nko2latin "ߌ ߦߋ ߛߊ߲ ߖߏߟߌ ߦߋ"
```

## License

MIT



