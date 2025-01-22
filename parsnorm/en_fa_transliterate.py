import re
import nltk
from nltk.corpus import cmudict


nltk.download("cmudict")
# Load the CMU Pronouncing Dictionary
pronouncing_dict = cmudict.dict()

# Add the word 'frightner' to a custom dictionary
custom_dict = {
    "frightner": [["F", "R", "AY1", "T", "N", "ER0"]],
    "frightners": [["F", "R", "AY1", "T", "N", "ER0", "Z"]],
    "hollyman": [["HH", "AA1", "L", "IY0", "M", "AE1", "N"]],
    "avenger": [["AH0", "V", "EH1", "N", "JH", "ER0"]],
    "avengers": [["AH0", "V", "EH1", "N", "JH", "ER0", "Z"]],
    "Snowpiercer": [["S", "N", "OW1", "P", "IH1", "R", "S", "ER0"]],
    "Snowpiercer": [["S", "N", "OW1", "P", "IH1", "R", "S", "ER0", "Z"]],
    "revenant": [["R", "EH1", "V", "AH0", "N", "AH0", "NT"]],
    "revenant": [["R", "EH1", "V", "AH0", "N", "AH0", "NT", "Z"]]
}
pronouncing_dict.update(custom_dict)

WEB_TO_FA = {
    "http": "اچ تی تی پی",
    "https": "اچ تی تی پی اس",
    "www": "دبلیو دبلیو دبلیو",
    "com": "کام",
    "org": "ارگ",
    "net": "نت",
    "edu": "ادو",
    "gov": "گا‌و",
    "mil": "میل",
    "io": "آی او",
    "ai": "آی",
    "biz": "بیز",
    "info": "اینفو",
    "name": "نیم",
    "email": "ایمیل",
    "user": "یوزر",
    "mail": "میل",
    "admin": "ادمین",
    "support": "ساپورت",
    "login": "لاگین",
    "signup": "ساین آپ",
    "logout": "لاگ آوت",
    "home": "هوم",
    "index": "ایندکس",
    "search": "سرچ",
    "about": "اباوت",
    "contact": "کانتکت",
    "profile": "پروفایل",
    "dashboard": "دشبورد",
    "download": "دانلود",
    "upload": "آپلود",
    "settings": "ستینگز",
    "help": "هلپ",
    "file": "فایل",
    "folder": "فولدر",
    "api": "ای پی آی",
    "blog": "بلاگ",
    "shop": "شاپ",
    "cart": "کارت",
    "checkout": "چک آوت",
    "product": "پروداکت",
    "service": "سرویس",
    "news": "نیوز",
    "forum": "فوروم",
    "faq": "اف ای کیو",
    "error": "ارور"
}

# Map English IPA sequences to Pinglish equivalents
IPA_TO_PINGLISH = {
    "aɪ": "ai", "ɔɪ": "oy", "ʌ": "a", "oʊ": "o", "eɪ": "ey", "ɪŋ": "ing", "ɑː": "a", "æ": "æ", "ɑ":'a',
    "e": "e", "i": "i", "o": "o", "ɒ": "a", "ɜː": "er", "ə": "e", "ɜ": "e", "ʊ": "u", "aʊ":"ow",
    "ɔː": "o", "uː": "u", "ɪ": "i", "ɛ": "e", "ɔ":"o",
    "l": "l", "v": "v", "p": "p", "r": "r",
    "g": "g", "m": "m", "h": "h", "ŋg": "ng",
    "w": "v", "j": "y", "u": "u", "tʃ": "ch", "dʒ": "j",
    "ʃ": "sh", "ʒ": "zh", "θ": "th1", "ð": "th2", "ŋ": "ng",
    "z": "z", "t": "t", "s": "s", "k": "k", "d": "d",
    "f": "f", "b": "b", "n": "n",
}

# Map Pinglish to Persian equivalents
PINGLISH_TO_PERSIAN = {
    "l": "ل", "v": "و", "p": "پ", "r": "ر",
    "o": "و", "g": "گ", "m": "م", "h": "ه", "ei": "ای", "ing": "ینگ",
    "ch": "چ", "sh": "ش", "zh": "ژ", "th1": "ت", "th2": "د", "j": "ج", "ng": "نگ",
    "z": "ز", "t": "ت", "k": "ک", "d": "د",
    "f": "ف", "b": "ب", "n": "ن", "er": "ار", "e": "ی", "i": "ی",
    "u": "و", "a": "ا", "o": "او", "y": "ی",
    "s_start":'اِس',
    "s_middle_end":"س",
    "ow_middle_end":'و',
    "ow_start":'او',
    # Mapping for 'ae' with two cases
    "ae_start": "اَ",  # For the start of the word
    "ae_middle": "َ",  # For the middle of the word
    "ae_end":"ه",
    "a_start": "آ",
    "a_middle_end": "ا",
    # Mapping for 'o' with two cases
    "o_start": "اُ",   # For the start of the word
    "o_middle": "و",   # For the middle of the word
    "o_end": "و",
    # Mapping for 'e' with two cases
    "e_start": "اِ",   # For the start of the word
    "e_middle": "ِ",   # For the middle of the word
    "e_end": "ه",
    # Mapping for "i"
    "i_start": "ای",   # For the start of the word
    "i_middle_end": "ی", # For the middle or end of the word
    # Mapping for "ai"
    "ai_start": "آی",  # For the start of the word
    "ai_middle_end": "ای", # For the middle of the word
}
# ARPAbet to IPA mapping
ARPABET_TO_IPA = {
    # Vowels - Monophthongs
    'AO': 'ɔ', 'AO0': 'ɔ', 'AO1': 'ɔ', 'AO2': 'ɔ',
    'AA': 'ɑ', 'AA0': 'ɑ', 'AA1': 'ɑ', 'AA2': 'ɑ',
    'IY': 'i', 'IY0': 'i', 'IY1': 'i', 'IY2': 'i',
    'UW': 'u', 'UW0': 'u', 'UW1': 'u', 'UW2': 'u',
    'EH': 'e', 'EH0': 'e', 'EH1': 'e', 'EH2': 'e',
    'IH': 'ɪ', 'IH0': 'ɪ', 'IH1': 'ɪ', 'IH2': 'ɪ',
    'UH': 'ʊ', 'UH0': 'ʊ', 'UH1': 'ʊ', 'UH2': 'ʊ',
    'AH': 'ʌ', 'AH0': 'ə', 'AH1': 'ʌ', 'AH2': 'ʌ',
    'AE': 'æ', 'AE0': 'æ', 'AE1': 'æ', 'AE2': 'æ',
    'AX': 'ə', 'AX0': 'ə', 'AX1': 'ə', 'AX2': 'ə',

    # Vowels - Diphthongs
    'EY': 'eɪ', 'EY0': 'eɪ', 'EY1': 'eɪ', 'EY2': 'eɪ',
    'AY': 'aɪ', 'AY0': 'aɪ', 'AY1': 'aɪ', 'AY2': 'aɪ',
    'OW': 'oʊ', 'OW0': 'oʊ', 'OW1': 'oʊ', 'OW2': 'oʊ',
    'AW': 'aʊ', 'AW0': 'aʊ', 'AW1': 'aʊ', 'AW2': 'aʊ',
    'OY': 'ɔɪ', 'OY0': 'ɔɪ', 'OY1': 'ɔɪ', 'OY2': 'ɔɪ',

    # Consonants - Stops
    'P': 'p', 'B': 'b', 'T': 't', 'D': 'd', 'K': 'k', 'G': 'g',

    # Consonants - Affricates
    'CH': 'tʃ', 'JH': 'dʒ',

    # Consonants - Fricatives
    'F': 'f', 'V': 'v', 'TH': 'θ', 'DH': 'ð', 'S': 's', 'Z': 'z',
    'SH': 'ʃ', 'ZH': 'ʒ', 'HH': 'h',

    # Consonants - Nasals
    'M': 'm', 'N': 'n', 'NG': 'ŋ',

    # Consonants - Liquids
    'L': 'l', 'R': 'r',

    # Vowels - R-colored vowels
    'ER': 'ɜr', 'ER0': 'ɜr', 'ER1': 'ɜr', 'ER2': 'ɜr',
    'AXR': 'ər', 'AXR0': 'ər', 'AXR1': 'ər', 'AXR2': 'ər',

    # Consonants - Semivowels
    'W': 'w', 'Y': 'j',
}

ENG_CHAR_TO_PER = {
    'a': 'ای',
    'b': 'بی',
    'c': 'سی',
    'd': 'دی',
    'e': 'ای',
    'f': 'اف',
    'g': 'جی',
    'h': 'اچ',
    'i': 'آی',
    'j': 'جی',
    'k': 'کی',
    'l': 'ال',
    'm': 'ام',
    'n': 'ان',
    'o': 'او',
    'p': 'پی',
    'q': 'کیو',
    'r': 'آر',
    's': 'اس',
    't': 'تی',
    'u': 'یو',
    'v': 'وی',
    'w': 'دابلیو',
    'x': 'ایکس',
    'y': 'وای',
    'z': 'زد',
}

def replace_web_words(text):
    # Iterate over the dictionary and replace each word
    for word, replacement in WEB_TO_FA.items():
        # Use a word boundary to ensure we're replacing whole words only
        text = re.sub(r'\b' + re.escape(word) + r'\b', replacement, text)
    return text

def transliterate_abbreviations(text):
    pattern = r'\b[a-zA-Z]+\b'
    
    def transliterate_word(word):
        # Convert each character in the word to its Persian equivalent
        return ' '.join(ENG_CHAR_TO_PER.get(char.lower(), char) for char in word)
    
    # Find all English words in the text
    matches = re.findall(pattern, text)
    
    # Replace each English word with its transliterated Persian version
    for match in matches:
        transliterated = transliterate_word(match)
        text = text.replace(match, transliterated)
    
    return text


class EnFaTransliterate:
    def __init__(self):
        self.arpabet_to_ipa = ARPABET_TO_IPA
        self.web_to_fa = WEB_TO_FA
        self.ipa_to_pinglish = IPA_TO_PINGLISH
        self.pinglish_to_persian = PINGLISH_TO_PERSIAN

    # Convert ARPAbet transcription to IPA
    def arpabet_to_ipa_conversion(self, arpabet):
        ipa_transcription = ""
        for symbol in arpabet:
            ipa_transcription += self.arpabet_to_ipa.get(symbol, symbol)  # Default to symbol if not found
        return ipa_transcription


    # Function to convert word to IPA using CMU Pronouncing Dictionary and ARPAbet to IPA conversion
    def word_to_ipa(self, word, d=pronouncing_dict):
        # Get ARPAbet transcription from CMU dictionary
        word = word.lower()
        if word in d:
            arpabet_transcription = d[word][0]  # Take the first pronunciation
            ipa_transcription = self.arpabet_to_ipa_conversion(arpabet_transcription)
            return ipa_transcription
        else:
            return None


    def clean_ipa(self, ipa_text):
        """Remove stress markers and extraneous symbols from IPA."""
        stress_markers = ['ˈ', 'ˌ']
        for marker in stress_markers:
            ipa_text = ipa_text.replace(marker, "")
        return ipa_text

    def ipa_to_pinglish_conversion(self, ipa_text):
        """Convert IPA sequences to Pinglish."""
        pinglish = ""
        i = 0
        while i < len(ipa_text):
            match = None
            # Try to match the longest IPA pattern from the current position
            for ipa_seq in sorted(self.ipa_to_pinglish.keys(), key=len, reverse=True):
                if ipa_text[i:i+len(ipa_seq)] == ipa_seq:
                    match = ipa_seq
                    break
            if match:
                pinglish += self.ipa_to_pinglish[match]
                i += len(match)  # Move forward by the length of the match
            else:
                pinglish += ipa_text[i]  # Preserve unmatched characters
                i += 1
        return pinglish


    def pinglish_to_persian_conversion(self, pinglish_text):
        """Convert Pinglish to Persian."""
        persian = ""
        i = 0
        while i < len(pinglish_text):
            length = 1
            match = None
            # Check for 'ae', 'o', or 'e' at the start, middle, or end of a word
            if pinglish_text[i:i+1] == "æ":
                # Check position: Start, Middle, or End of the word
                if i == 0:
                    match = "ae_start"
                elif i == len(pinglish_text) - 1:
                    match = "ae_end"
                else:
                    match = "ae_middle"
            elif pinglish_text[i:i+2] == "ai":
                length = 2
                # Check position: Start, Middle, or End of the word
                if i == 0:
                    match = "ai_start"
                else:
                    match = "ai_middle_end"
            elif pinglish_text[i:i+2] == "ow":
                length = 2
                # Check position: Start, Middle, or End of the word
                if i == 0:
                    match = "ow_start"
                else:
                    match = "ow_middle_end"
            elif pinglish_text[i:i+2] == "sh":
                length = 2
                # Check position: Start, Middle, or End of the word
                match = "sh"
            elif pinglish_text[i:i+1] == "a":
                if i == 0:
                    match = "a_start"
                else:
                    match = "a_middle_end"
            elif pinglish_text[i:i+1] == "o":
                # Check position: Start, Middle, or End of the word
                if i == 0:
                    match = "o_start"
                elif i == len(pinglish_text) - 1:
                    match = "o_end"
                else:
                    match = "o_middle"
            elif pinglish_text[i:i+1] == "e":
                # Check position: Start, Middle, or End of the word
                if i == 0:
                    match = "e_start"
                elif i == len(pinglish_text) - 1:
                    match = "e_end"
                else:
                    match = "e_middle"
            elif pinglish_text[i:i+1] == "i":
                # Check position: Start, Middle, or End of the word
                if i == 0:
                    match = "i_start"
                else:
                    match = "i_middle_end"
            elif pinglish_text[i:i+1] == "s":
                # Check position: Start, Middle, or End of the word
                if i == 0 and pinglish_text[i+1] not in "aeouiæ":
                    match = "s_start"
                else:
                    match = "s_middle_end"
            
            # If a match is found, add the corresponding Persian equivalent
            if match:
                persian += self.pinglish_to_persian[match]
                i += length  # Move forward by the length of the match
            else:
                # Try to match the longest Pinglish pattern
                for pinglish_seq in sorted(self.pinglish_to_persian.keys(), key=len, reverse=True):
                    if pinglish_text[i:i+len(pinglish_seq)] == pinglish_seq:
                        match = pinglish_seq
                        break
                if match:
                    persian += self.pinglish_to_persian[match]
                    i += len(match)
                else:
                    persian += pinglish_text[i]  # Preserve unmatched characters
                    i += 1
        return persian


    def normalizer(self, text):
        """Convert English text to Persian pronunciation."""
        # Convert English text to IPA
        ipa_text = self.word_to_ipa(text)
        # Clean the IPA transcription
        if ipa_text:
            text = self.clean_ipa(ipa_text)
            text = self.ipa_to_pinglish_conversion(text)
            text = self.pinglish_to_persian_conversion(text)
        text = replace_web_words(text)
        text = transliterate_abbreviations(text)
        return text
