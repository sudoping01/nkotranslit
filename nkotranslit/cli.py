from nkotranslit.convert import NkoLatinConverter

def latin_to_nko_cli():
    import sys
    converter =NkoLatinConverter()
    sentence = " ".join(sys.argv[1:])
    print(converter.convert_text(sentence, converter.LATIN_TO_NKO_RULES))

def nko_to_latin_cli():
    import sys
    converter = NkoLatinConverter()
    sentence = " ".join(sys.argv[1:])
    print(converter.convert_text(sentence, converter.NKO_TO_LATIN_RULES))