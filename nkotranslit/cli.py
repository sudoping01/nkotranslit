from nkotranslit.nko2latin import Nko2Latin
from nkotranslit.latin2nko import Latin2Nko

def latin_to_nko_cli():
    import sys
    converter = Latin2Nko()
    sentence = " ".join(sys.argv[1:])
    print(converter.convert(sentence))

def nko_to_latin_cli():
    import sys
    converter = Nko2Latin()
    sentence = " ".join(sys.argv[1:])
    print(converter.convert(sentence))
