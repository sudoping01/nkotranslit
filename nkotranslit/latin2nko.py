#!/usr/bin/env python3
# -*- coding: utf8 -*-

from nkotranslit.utils import OrthographyConverter
import re
import unicodedata

debug = False

class Latin2Nko(OrthographyConverter):
    def __init__(self, *args, **kwargs):
        self.title = 'latin_to_nko'
        self.desc = 'General-purpose converter from Latin script to NKO, updated based on LoC romanization tables'

    def _convert(self, token):
        """
        Main Latin>NKO conversion method based on standardized mappings
        from the Library of Congress romanization table, with fixes for tones, punctuation, and gaps.
        """
        w = token
        
        # Skip conversion for tokens already containing N'Ko characters
        if re.search("[\u07c0-\u07ff]", w):
            return [w]

        if debug:
            print("LAT", w)
            
        # Handle capitalization - N'Ko doesn't have case distinctions,
        # but we should track for statistics or debugging
        is_capitalized = w[0].isupper() if w else False
        
        # Decompose accents for proper handling (NFD normalization)
        w = unicodedata.normalize('NFD', w)
        # Convert to lowercase for processing (combining marks preserved)
        w = w.lower()

        # STEP 1: Handle punctuation (updated based on Unicode standards)
        w = w.replace(",", '\u07f8')        # , -> ߸ NKO COMMA
        w = w.replace(".", '\u07f7')         # . -> ߷ NKO SYMBOL GBAKURUNEN (section end/full stop)
        w = w.replace("-", '\u07fa')         # - -> ߺ NKO LAJANYALAN (hyphen/extender)
        w = w.replace(";", '\u07f8')         # ; -> ߸ NKO COMMA (shared)
        w = w.replace("?", '\u061f')         # ? -> ؟ ARABIC QUESTION MARK (common in N'Ko)
        w = w.replace("!", '\u07f9')         # ! -> ߹ NKO EXCLAMATION MARK
        w = w.replace("'", '\u07f4')         # ' -> ߴ NKO HIGH TONE APOSTROPHE (for elision)
        
        # STEP 2: Handle nasalization EARLY (before special vowels, after punct) to catch toned/decomposed
        # Updated to construct pattern and repl to properly interpret Unicode
        vowel_class = 'aeiouɛɔεͻǝ'
        comb_range = '\u0300' + '-' + '\u036f'
        non_vowel = '[^' + vowel_class + ']'
        nasal_pattern = '([' + vowel_class + '][' + comb_range + ']*)n(' + non_vowel + '|$)'
        nasal_repl = '\\1\u07f2\\2'
        w = re.sub(nasal_pattern, nasal_repl, w)
        
        # STEP 3: Handle special digraphs and trigraphs first (must come before single letters)
        w = w.replace("sh", '\u07db\u07ed')  # sh -> ߛ߭ (s + rising)
        w = w.replace("gb", '\u07dc')         # gb -> ߜ
        w = w.replace("rr", '\u07da')         # rr -> ߚ
        w = w.replace("kp", '\u07de\u07ed')   # kp -> ߞ߭ (k + rising)
        w = w.replace("zh", '\u07d7\u07ed')   # zh -> ߗ߭ (c + rising)
        w = w.replace("kh", '\u07de\u07eb')   # kh -> ߞ߫ (k + high)
        w = w.replace("th", '\u07d5\u07ed')   # th -> ߕ߭ (t + rising)
        
        # STEP 4: Handle special vowels (now with decomposed forms via re.sub)
        w = w.replace("ɛ", '\u07cd')          # ɛ -> ߍ
        w = w.replace("ε", '\u07cd')          # ε -> ߍ (alternate)
        w = w.replace("ɔ", '\u07d0')          # ɔ -> ߐ
        w = w.replace("ͻ", '\u07d0')          # ͻ -> ߐ (alternate)
        w = w.replace("ǝ", '\u07cb')          # ǝ -> ߋ (schwa)
        w = re.sub('a' + '\u0308', '\u07cb', w)   # ä (decomposed) -> ߋ (schwa)
        w = re.sub('u' + '\u0308', '\u07ce', w)   # ü (decomposed) -> ߎ
        
        # STEP 5: Handle special consonants with diacritics (foreign sounds from LoC)
        w = w.replace("ɓ", '\u07d3\u07ed')    # ɓ -> ߓ߭ (b + rising)
        w = w.replace("ɗ", '\u07d8\u07ed')    # ɗ -> ߘ߭ (d + rising)
        w = w.replace("ɣ", '\u07dc\u07eb')    # ɣ -> ߜ߫ (gb + high? simplified)
        w = w.replace("ɲ", '\u07e2')          # ɲ -> ߢ (primary; alt ߧ not added)
        w = w.replace("ŋ", '\u07e3\u07ed')    # ŋ -> ߣ߭ (n + rising)
        w = w.replace("g", '\u07dc\u07ed')    # g -> ߜ߭ (gb + rising)
        w = w.replace("v", '\u07dd\u07ed')    # v -> ߝ߭ (f + rising)
        w = w.replace("z", '\u07d6\u07ed')    # z -> ߖ߭ (j + rising)
        w = w.replace("x", '\u07de\u07ed')    # x -> ߞ߭ (k + rising)
        w = w.replace("q", '\u07e4\u07ed')    # q -> ߤ߭ (h + rising)
        # Added more foreign from LoC (simplified compositions; exact may vary)
        w = w.replace("t’", '\u07d5\u07ec')   # t’ -> ߕ߬ (t + low, approx for glottal)
        w = w.replace("j’", '\u07d6\u07ec')   # j’ -> ߖ߬ (j + low)
        w = w.replace("d’", '\u07d8\u07ec')   # d’ -> ߘ߬ (d + low)
        w = w.replace("r’", '\u07d9\u07ec')   # r’ -> ߙ߬ (r + low)
        w = w.replace("s’", '\u07db\u07ec')   # s’ -> ߛ߬ (s + low)
        w = w.replace("l’", '\u07df\u07ec')   # l’ -> ߟ߬ (l + low)
        w = w.replace("m’", '\u07e1\u07ec')   # m’ -> ߡ߬ (m + low)
        
        # STEP 6: Convert basic consonants according to the LoC romanization table
        w = w.replace("y", '\u07e6')         # y -> ߦ
        w = w.replace("w", '\u07e5')         # w -> ߥ
        w = w.replace("h", '\u07e4')         # h -> ߤ
        w = w.replace("n", '\u07e3')         # n -> ߣ (primary; variants ߒ/ߠ context-dependent)
        w = w.replace("m", '\u07e1')         # m -> ߡ
        w = w.replace("l", '\u07df')         # l -> ߟ
        w = w.replace("k", '\u07de')         # k -> ߞ
        w = w.replace("f", '\u07dd')         # f -> ߝ
        w = w.replace("s", '\u07db')         # s -> ߛ
        w = w.replace("r", '\u07d9')         # r -> ߙ
        w = w.replace("d", '\u07d8')         # d -> ߘ
        w = w.replace("c", '\u07d7')         # c -> ߗ
        w = w.replace("j", '\u07d6')         # j -> ߖ
        w = w.replace("t", '\u07d5')         # t -> ߕ
        w = w.replace("p", '\u07d4')         # p -> ߔ
        w = w.replace("b", '\u07d3')         # b -> ߓ
        
        # STEP 7: Convert basic vowels (now with decomposed tones preserved as combining marks)
        w = w.replace("o", '\u07cf')         # o -> ߏ
        w = w.replace("u", '\u07ce')         # u -> ߎ
        w = w.replace("i", '\u07cc')         # i -> ߌ
        w = w.replace("e", '\u07cb')         # e -> ߋ
        w = w.replace("a", '\u07ca')         # a -> ߊ
        
        # STEP 8: Handle tone marks on N'Ko vowels (now catches decomposed Latin combining marks)
        # High tones (á \u0301)
        w = re.sub('(\u07ca|\u07cb|\u07cc|\u07cd|\u07ce|\u07cf|\u07d0)\u0301', '\\1\u07eb', w)
        
        # Low tones (à \u0300)
        w = re.sub('(\u07ca|\u07cb|\u07cc|\u07cd|\u07ce|\u07cf|\u07d0)\u0300', '\\1\u07ec', w)
        
        # Rising tones (ǎ \u030c)
        w = re.sub('(\u07ca|\u07cb|\u07cc|\u07cd|\u07ce|\u07cf|\u07d0)\u030c', '\\1\u07ed', w)
        
        # Descending tones (â \u0302) - approximated as long descending \u07ee (LoC short unmarked word-final complex; use for all)
        w = re.sub('(\u07ca|\u07cb|\u07cc|\u07cd|\u07ce|\u07cf|\u07d0)\u0302', '\\1\u07ee', w)
        
        # STEP 9: Handle numerals
        w = w.replace("0", '\u07c0')         # 0 -> ߀
        w = w.replace("1", '\u07c1')         # 1 -> ߁
        w = w.replace("2", '\u07c2')         # 2 -> ߂
        w = w.replace("3", '\u07c3')         # 3 -> ߃
        w = w.replace("4", '\u07c4')         # 4 -> ߄
        w = w.replace("5", '\u07c5')         # 5 -> ߅
        w = w.replace("6", '\u07c6')         # 6 -> ߆
        w = w.replace("7", '\u07c7')         # 7 -> ߇
        w = w.replace("8", '\u07c8')         # 8 -> ߈
        w = w.replace("9", '\u07c9')         # 9 -> ߉
        
        # STEP 10: Handle vowel lengthening (double vowels with tone marks) - updated to catch tone on either position
        vowels = {
            '\u07ca': '\u07ef',  # a high long
            '\u07cb': '\u07ef',  # e
            '\u07cc': '\u07ef',  # i
            '\u07cd': '\u07ef',  # ɛ
            '\u07ce': '\u07ef',  # u
            '\u07cf': '\u07ef',  # o
            '\u07d0': '\u07ef',  # ɔ
        }
        tones = {
            'high': ('\u07eb', '\u07ef'),
            'low': ('\u07ec', '\u07f0'),
            'rising': ('\u07ed', '\u07f1'),
            'descending': ('\u07ee', '\u07ee'),  # reuse for long
        }
        
        for v, long_mark in vowels.items():
            for tone_name, (short_tone, long_tone) in tones.items():
                # Tone on first vowel
                w = re.sub(f'({v})({short_tone})({v})', rf'\1{long_tone}', w)
                # Tone on second vowel
                w = re.sub(f'({v})({v})({short_tone})', rf'\1{long_tone}', w)
        
        # STEP 11: Handle the Gbàralí (contraction) rule - simplified approximation
        # Remove repeated short vowels in potential consecutive syllables (e.g., CV CV -> C V if same vowel)
        # Updated non-vowel capture to N'Ko consonants/range
        gb_vowels = ['\u07ca', '\u07cb', '\u07cc', '\u07cd', '\u07ce', '\u07cf', '\u07d0']
        for v in gb_vowels:
            w = re.sub(f'({v})([^\u07ca-\u07d0]+)(?={v})', r'\2', w)
        # Note: This is approximate and may over-apply; full rule requires syllable boundaries.
        # The lookahead ensures it removes the first v before the second, leaving the second.
        
        # STEP 12: Add RTL mark for proper display
        if not w.endswith('\u200f'):
            w = w + '\u200f'  
        
        if debug:
            print("NKO", w)
        return [w]
    
    def convert(self, sentence):
        result = []
        for word in sentence.split():
                    if "'" in word:
                        parts = word.split("'")
                        converted_parts = []
                        for part in parts:
                            if part:  # Skip empty parts
                                converted = self._convert(part)[0]
                                converted_parts.append(converted)
                        # Join with N'Ko apostrophe
                        result.append('\u07f5'.join(converted_parts))
                    else:
                        converted = self._convert(word)[0]
                        result.append(converted)

        return ' '.join(result).replace('\n', '\n')
    

    
# def main():
#     converter = Latin2Nko()

#     examples = [
#         "i ye san joli ye",
#         "min bɛ deli ka kɛ",
#         "O tamira, ne yεrε kɔrɔkε Maratu\nBala, o sigira o nɔ la.\nO sigira o nɔ la, o fana bannen, ne\nde tugura o la. Ne de sigira, awa-a,\nalu ma sɔn o ma.",
#         "bi ni sini mͻgͻw ka kan k'u sinsin minnu kan",
#         "ka hakili to fana yɛrɛmahɔrɔya tabagaw ka hakililaw la"
#     ]

#     for i, example in enumerate(examples):
#         print(f"Example {i+1}:")
#         print(f"Latin: {example}")
#         print(f"N'Ko:  {converter.convert(example)}")
#         print("-" * 50)


# if __name__ == "__main__":
#     main()
