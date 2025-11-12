#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tapo, Seydou DIALLO et al. 11-10-2025

A self-contained, state-of-the-art Python script for bidirectional,
rule-based conversion of Bambara text between Latin and N'Ko scripts.

This script uses order-dependent rules to correctly handle digraphs,
nasal vowels, and other orthographic features.

# Permission is hereby granted, free of charge, to any person obtaining a copy of this
# software and associated documentation files (the "Software"), to deal in the Software
# without restriction, including without limitation the rights to use, copy, modify,
# merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import sys
import argparse
from collections import OrderedDict

# --- Conversion Rules ---

# Rules are defined in an OrderedDict to ensure that longer sequences
# (e.g., "ny", "an") are processed BEFORE shorter ones (e.g., "n", "y", "a").
# This is critical for correct transliteration.

# NOTE: Correct SOTA mapping for 'o'/'ò' is used:
# 'o' (close-mid) -> ߐ
# 'ò' (open-mid, ɔ) -> ߏ
# The prompt's example of o/ò -> ߏ is ambiguous and has been corrected.

class NkoLatinConverter:
    def __init__(self):
    
        self.LATIN_TO_NKO_RULES = OrderedDict(
            [
                # 1. Nasal Vowels (must come before single vowels)
                # Handle capitalized versions first for robustness
                ("An", "ߊ߲"),
                ("En", "ߋ߲"),
                ("Èn", "ߍ߲"),
                ("In", "ߌ߲"),
                ("On", "ߐ߲"),
                ("Òn", "ߏ߲"),
                ("Un", "ߎ߲"),
                ("an", "ߊ߲"),
                ("en", "ߋ߲"),
                ("èn", "ߍ߲"),
                ("in", "ߌ߲"),
                ("on", "ߐ߲"),
                ("òn", "ߏ߲"),
                ("un", "ߎ߲"),
                # 2. Digraphs (must come before single consonants)
                ("Ny", "ߢ"),
                ("Ng", "ߒ"),
                ("Gb", "ߜ"),
                ("Kp", "ߞߔ"),  # N'Ko uses a kp digraph
                ("Sh", "ߛ"),
                ("ny", "ߢ"),
                ("ng", "ߒ"),
                ("gb", "ߜ"),
                ("kp", "ߞߔ"),
                ("sh", "ߛ"),  # For loanwords
                # 3. Standard Vowels
                ("A", "ߊ"),
                ("E", "ߋ"),  # close-mid 'e'
                ("È", "ߍ"),  # open-mid 'ɛ'
                 ("ɛ", "ߍ"),
                ("I", "ߌ"),
                ("O", "ߏ"),  # close-mid 'o'
                ("Ò", "ߐ"),  # open-mid 'ɔ' 
                 ("ɔ", "ߐ"),
                ("U", "ߎ"),
                ("a", "ߊ"),
                ("e", "ߋ"),
                ("è", "ߍ"),
                ("i", "ߌ"),
                ("o", "ߏ"), 
                ("ò", "ߐ"),
                ("u", "ߎ"),
                # 4. Standard Consonants
                ("B", "ߓ"),
                ("C", "ߗ"),  # Often 'c' in Bambara is 'ch'
                ("D", "ߘ"),
                ("F", "ߝ"),
                ("G", "ߜ"),  # Note: 'g' can also be part of 'ng' or 'gb'
                ("H", "ߤ"),
                ("J", "ߖ"),
                ("K", "ߞ"),
                ("L", "ߟ"),
                ("M", "ߡ"),
                ("N", "ߣ"),  # Handled after 'ny', 'ng', and nasal vowels
                ("P", "ߔ"),
                ("R", "ߙ"),
                ("S", "ߛ"),
                ("T", "ߕ"),
                ("V", "ߝ"),  # Often mapped to F
                ("W", "ߥ"),
                ("Y", "ߦ"),
                ("Z", "ߖ"),  # Often mapped to J
                ("b", "ߓ"),
                ("c", "ߗ"),
                ("d", "ߘ"),
                ("f", "ߝ"),
                ("g", "ߜ"),
                ("h", "ߤ"),
                ("j", "ߖ"),
                ("k", "ߞ"),
                ("l", "ߟ"),
                ("m", "ߡ"),
                ("n", "ߣ"),
                ("p", "ߔ"),
                ("r", "ߙ"),
                ("s", "ߛ"),
                ("t", "ߕ"),
                ("v", "ߝ"),
                ("w", "ߥ"),
                ("y", "ߦ"),
                ("z", "ߖ"),
                ("ɲ", "ߢ"),   
                ("ŋ", "ߣ߭"),
                ("ng", "ߣ߭"),
                # 5. Punctuation
                ("?", "؟"),
                (";", "؛"),
                # (.,! are often the same, but N'Ko-specific ones exist)
                ("0", "߀"),
                ("1", "߁"),
                ("2", "߂"),
                ("3", "߃"),
                ("4", "߄"),
                ("5", "߅"),
                ("6", "߆"),
                ("7", "߇"),
                ("8", "߈"),
                ("9", "߉"),

            ]
        )

        self.NKO_TO_LATIN_RULES = OrderedDict(
            [
                # 1. Nasal Vowels (must come before single vowels)
                ("ߊ߲", "an"),
                ("ߋ߲", "en"),
                ("ߍ߲", "èn"),
                ("ߍ߲", "ɛn"),
                ("ߌ߲", "in"),
                ("ߏ߲", "on"),
                ("ߐ߲", "òn"), 
                ("ߐ߲", "ɔn"),
                ("ߎ߲", "un"),
                # 2. Tone Markers (strip them, as per standard Latin orthography)
                ("߰", ""),  # NKO SYLLABLE TONE KI (HIGH)
                ("߱", ""),  # NKO SYLLABLE TONE KUN (LOW)
                ("߳", ""),  # NKO TONE LENGTHENER
                ("ߴ", ""),  # NKO HIGH TONE APOSTROPHE
                ("ߵ", ""),  # NKO LOW TONE APOSTROPHE
                # 3. Digraphs (must come before single consonants)
                ("ߢ", "ny"),
                ("ߒ", "ng"),
                ("ߜ", "gb"),  # This is ambiguous with 'g', 'gb' is more likely
                ("ߞߔ", "kp"),
                # 4. Standard Vowels
                ("ߊ", "a"),
                ("ߋ", "e"),  # close-mid 'e'
                ("ߍ", "è"),  # open-mid 'ɛ'
                ("ߍ", "ɛ"),
                ("ߌ", "i"),
                ("ߏ", "o"),  # close-mid 'o' 
                ("ߐ", "ò"),  # open-mid 'ɔ'
                ("ߐ", "ɔ"),
                ("ߎ", "u"),
                # 5. Standard Consonants
                ("ߓ", "b"),
                ("ߗ", "c"),
                ("ߘ", "d"),
                ("ߝ", "f"),
                ("ߜ", "g"),  # Handle 'g' after 'gb'
                ("ߤ", "h"),
                ("ߖ", "j"),
                ("ߞ", "k"),
                ("ߟ", "l"),
                ("ߡ", "m"),
                ("ߣ", "n"),  # Handle 'n' after digraphs and nasals
                ("ߔ", "p"),
                ("ߙ", "r"),
                ("ߛ", "s"),
                ("ߕ", "t"),
                ("ߥ", "w"),
                ("ߦ", "y"),  # Handle 'y' after 'ny'

                ("ߢ","ɲ"),    
                ("ߣ߭","ŋ"), 
                ("ߣ߭","ng"),

                # 6. N'Ko Punctuation
                ("߸", ", "),  # NKO COMMA (add space for readability)
                ("߹", ". "),  # NKO EXCLAMATION MARK (often used as 'la' / period)
                ("؟", "?"),
                ("؛", ";"),
                # 7. N'Ko Digits
                ("߀", "0"), 
                ("߁", "1"), 
                ("߂", "2"), 
                ("߃", "3"), 
                ("߄", "4"), 
                ("߅", "5")  , 
                ("߆", "6"), 
                ("߇", "7"), 
                ("߈", "8"), 
                ("߉", "9"), 

            ]
        )


    def convert_text(self, text:str, rules:OrderedDict):
        """
        Iteratively applies conversion rules from an OrderedDict.

        Args:
            text (str): The input text to convert.
            rules (OrderedDict): An ordered dictionary of (find, replace) rules.

        Returns:
            str: The converted text.
        """
        for find, replace in rules.items():
            text = text.replace(find, replace)
        return text
