


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

## License

MIT



