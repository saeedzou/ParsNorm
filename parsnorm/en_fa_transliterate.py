import re
import nltk
import os
from nltk.corpus import cmudict

nltk_data_dir = os.getenv("NLTK_DATA", "./nltk_data")
nltk.download("cmudict", download_dir=nltk_data_dir)
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

# ARPAbet to PERSIAN mapping
ARPABET_TO_PERSIAN = {
    # Vowels - Monophthongs
    'AO': 'ُ', 'AO0': 'ُ', 'AO1': 'ُ', 'AO2': 'ُ',
    'AA': 'ا', 'AA0': 'ا', 'AA1': 'ا', 'AA2': 'ا',
    'IY': 'ی', 'IY0': 'ی', 'IY1': 'ی', 'IY2': 'ی',
    'UW': 'و', 'UW0': 'و', 'UW1': 'و', 'UW2': 'و',
    'EH': 'ِ', 'EH0': 'ِ', 'EH1': 'ِ', 'EH2': 'ِ',
    'IH': 'ی', 'IH0': 'ی', 'IH1': 'ی', 'IH2': 'ی',
    'UH': 'و', 'UH0': 'و', 'UH1': 'و', 'UH2': 'و',
    'AH': 'ا', 'AH0': 'ا', 'AH1': 'ا', 'AH2': 'ا',
    'AE': 'َ', 'AE0': 'َ', 'AE1': 'َ', 'AE2': 'َ',
    'AX': 'ِ', 'AX0': 'ِ', 'AX1': 'ِ', 'AX2': 'ِ',

    # Vowels - Diphthongs
    'EY': 'ِی', 'EY0': 'ِی', 'EY1': 'ِی', 'EY2': 'ِی',
    'AY': 'ای', 'AY0': 'ای', 'AY1': 'ای', 'AY2': 'ای',
    'OW': 'ُ', 'OW0': 'ُ', 'OW1': 'ُ', 'OW2': 'ُ',
    'AW': 'و', 'AW0': 'و', 'AW1': 'و', 'AW2': 'و',
    'OY': 'ُی', 'OY0': 'ُی', 'OY1': 'ُی', 'OY2': 'ُی',
    # Consonants - Stops
    'P': 'پ', 'B': 'ب', 'T': 'ت', 'D': 'د', 'K': 'ک', 'G': 'گ',

    # Consonants - Affricates
    'CH': 'چ', 'JH': 'ج',

    # Consonants - Fricatives
    'F': 'ف', 'V': 'و', 'TH': 'ت', 'DH': 'د', 'S': 'س', 'Z': 'ز',
    'SH': 'ش', 'ZH': 'ژ', 'HH': 'ه',

    # Consonants - Nasals
    'M': 'م', 'N': 'ن', 'NG': 'نگ',

    # Consonants - Liquids
    'L': 'ل', 'R': 'ر',

    # Vowels - R-colored vowels
    'ER': 'ِر', 'ER0': 'ِر', 'ER1': 'ِر', 'ER2': 'ِر',
    'AXR': 'ِر', 'AXR0': 'ِر', 'AXR1': 'ِر', 'AXR2': 'ِر',
    # Consonants - Semivowels
    'W': 'و', 'Y': 'ی',
}

START_DIACRITICS = {
    'AO': 'اُ', 'AO0': 'اُ', 'AO1': 'اُ', 'AO2': 'اُ',
    'AA': 'آ', 'AA0': 'آ', 'AA1': 'آ', 'AA2': 'آ',
    'IY': 'ای', 'IY0': 'ای', 'IY1': 'ای', 'IY2': 'ای',
    'UW': 'او', 'UW0': 'او', 'UW1': 'او', 'UW2': 'او',
    'EH': 'اِ', 'EH0': 'اِ', 'EH1': 'اِ', 'EH2': 'اِ',
    'IH': 'ای', 'IH0': 'ای', 'IH1': 'ای', 'IH2': 'ای',
    'UH': 'او', 'UH0': 'او', 'UH1': 'او', 'UH2': 'او',
    'AH': 'ا', 'AH0': 'ا', 'AH1': 'ا', 'AH2': 'ا',
    'AE': 'اَ', 'AE0': 'اَ', 'AE1': 'اَ', 'AE2': 'اَ',
    'AX': 'اِ', 'AX0': 'اِ', 'AX1': 'اِ', 'AX2': 'اِ',
    'EY': 'اِی', 'EY0': 'اِی', 'EY1': 'اِی', 'EY2': 'اِی',
    'AY': 'آی', 'AY0': 'آی', 'AY1': 'آی', 'AY2': 'آی',
    'OW': 'اُ', 'OW0': 'اُ', 'OW1': 'اُ', 'OW2': 'اُ',
    'AW': 'او', 'AW0': 'او', 'AW1': 'او', 'AW2': 'او',
    'OY': 'اُی', 'OY0': 'اُی', 'OY1': 'اُی', 'OY2': 'اُی',
    'ER': 'اِر', 'ER0': 'اِر', 'ER1': 'اِر', 'ER2': 'اِر',
    'AXR': 'اِر', 'AXR0': 'اِر', 'AXR1': 'اِر', 'AXR2': 'اِر',
}

END_DIACRITICS = {
    'AO': 'و', 'AO0': 'و', 'AO1': 'و', 'AO2': 'و',
    'AA': 'ا', 'AA0': 'ا', 'AA1': 'ا', 'AA2': 'ا',
    'IY': 'ی', 'IY0': 'ی', 'IY1': 'ی', 'IY2': 'ی',
    'UW': 'و', 'UW0': 'و', 'UW1': 'و', 'UW2': 'و',
    'EH': 'ه', 'EH0': 'ه', 'EH1': 'ه', 'EH2': 'ه',
    'IH': 'ی', 'IH0': 'ی', 'IH1': 'ی', 'IH2': 'ی',
    'UH': 'و', 'UH0': 'و', 'UH1': 'و', 'UH2': 'و',
    'AH': 'ا', 'AH0': 'ا', 'AH1': 'ا', 'AH2': 'ا',
    'AE': 'ه', 'AE0': 'ه', 'AE1': 'ه', 'AE2': 'ه',
    'AX': 'ه', 'AX0': 'ه', 'AX1': 'ه', 'AX2': 'ه',
    'EY': 'ِی', 'EY0': 'ِی', 'EY1': 'ِی', 'EY2': 'ِی',
    'AY': 'ای', 'AY0': 'ای', 'AY1': 'ای', 'AY2': 'ای',
    'OW': 'و', 'OW0': 'و', 'OW1': 'و', 'OW2': 'و',
    'AW': 'و', 'AW0': 'و', 'AW1': 'و', 'AW2': 'و',
    'OY': 'وی', 'OY0': 'وی', 'OY1': 'وی', 'OY2': 'وی',
    'ER': 'ِر', 'ER0': 'ِر', 'ER1': 'ِر', 'ER2': 'ِر',
    'AXR': 'ِر', 'AXR0': 'ِر', 'AXR1': 'ِر', 'AXR2': 'ِر',
}

S_SPECIAL = {
    'S': 'اِس', 'S0': 'اِس', 'S1': 'اِس', 'S2': 'اِس',
}

ENG_CHAR_TO_PER = {
    'a': 'اِی',
    'b': 'بی',
    'c': 'سی',
    'd': 'دی',
    'e': 'ای',
    'f': 'اف',
    'g': 'جی',
    'h': 'اِچ',
    'i': 'آی',
    'j': 'جِی',
    'k': 'کِی',
    'l': 'اِل',
    'm': 'اِم',
    'n': 'اِن',
    'o': 'او',
    'p': 'پی',
    'q': 'کیو',
    'r': 'آر',
    's': 'اِس',
    't': 'تی',
    'u': 'یو',
    'v': 'وی',
    'w': 'دابلیو',
    'x': 'ایکس',
    'y': 'وای',
    'z': 'زِد',
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
        self.web_to_fa = WEB_TO_FA

    def en_fa_transliterate(self, word):
        # Transliterate
        persian = ''
        for idx, phoneme in enumerate(word):
            if idx == 0 and phoneme in START_DIACRITICS:
                persian += START_DIACRITICS[phoneme]
            elif idx == len(word) - 1 and phoneme in END_DIACRITICS:
                persian += END_DIACRITICS[phoneme]
            elif idx == 0 and phoneme in S_SPECIAL and idx < len(word) - 1:
                if word[idx + 1] not in START_DIACRITICS:
                    persian += S_SPECIAL[phoneme]
                else:
                    persian += ARPABET_TO_PERSIAN[phoneme]
            elif phoneme in ARPABET_TO_PERSIAN:
                persian += ARPABET_TO_PERSIAN[phoneme]
            else:
                persian += phoneme

        return persian
    
    # Function to convert word to IPA using CMU Pronouncing Dictionary and ARPAbet to IPA conversion
    def transliterate(self, word, d=pronouncing_dict):
        # Get ARPAbet transcription from CMU dictionary
        word = word.lower()
        if word in d:
            arpabet_transcription = d[word][0]  # Take the first pronunciation
            ipa_transcription = self.en_fa_transliterate(arpabet_transcription)
            return ipa_transcription
        else:
            return None

    def normalizer(self, text):
        """Convert English text to Persian pronunciation."""
        # Convert English text to IPA
        transliterated = self.transliterate(text)
        # Clean the IPA transcription
        if transliterated:
            text = transliterated
        text = replace_web_words(text)
        text = transliterate_abbreviations(text)
        return text
