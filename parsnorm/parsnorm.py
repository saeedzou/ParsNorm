"""
ParsNorm Module
===============

This module provides comprehensive text normalization for Persian (Farsi) text,
leveraging multiple libraries and techniques for cleaning, transliterating, and
correcting text.

This is mainly developed as normalization for speech dataset creation using method in
CTC-Segmentation of Large Corpora for German End-to-End Speech Recognition: 
https://arxiv.org/abs/2007.09127

Classes
-------
ParsNorm
    A class that integrates normalization functionalities from `hazm`, ``,
    `parsinorm`, and `english_to_persian_transliteration` to provide advanced
    text processing capabilities.

"""
import re

from hazm import Normalizer as HazmNormalizer
from parsinorm import Mail_url_cleaner, Date_time_to_text, Abbreviation, Special_numbers
from parsinorm import General_normalization as ParsiNormalizer
from parsnorm.en_fa_transliterate import EnFaTransliterate

SYMBOLS_PRONUNCIATION = {
    "%": " درصد",
    "$": " دلار",
    "€": " یورو",
    "£": " پوند",
    "¥": " ین",
    "@": " ات ساین",
    "°C": " درجه سلسیوس",
    "°F": " درجه فارنهایت"
}

class ParsNorm:
    """
    ParsNorm
    --------
    A class for Persian text normalization that combines multiple tools and
    approaches to handle various aspects of text cleaning and normalization.

    Methods
    -------
    __init__()
        Initializes the ParsNorm instance with required sub-modules.

    en_fa_transliterate(text)
        Transliterates English words in the input text to Persian equivalents.

    normalize(text, **kwargs)
        Performs normalization on the given text based on provided options.

    """
    def __init__(self):
        self.hazm_norm = HazmNormalizer()

        self.parsi_norm = ParsiNormalizer()
        self.mail_url_cleaner = Mail_url_cleaner()
        self.date_time_to_text = Date_time_to_text()
        self.abbreviation = Abbreviation()
        self.special_numbers = Special_numbers()

        self.en_fa_transliterater = EnFaTransliterate()
    
    def en_fa_transliterate(self, text):
        """
        Transliterates English words in the input text to Persian equivalents.
        It also converts Pinglish words to Persian using Normalizer

        Parameters
        ----------
        text : str
            The input text containing English words to transliterate.

        Returns
        -------
        str
            Text with English words transliterated to Persian.
        """
        return re.sub(r"\b[a-zA-Z]+(?:'[a-zA-Z]+)?\b", lambda match: self.en_fa_transliterater.normalizer(match.group(0).lower()), text)
    
    def normalize(self, text,
                  clean_urls=False, clean_emails=False, 
                  convert_time=True, convert_date=False,
                  alphabet_correction=True, semi_space_correction=True,
                  english_correction=False, html_correction=True, 
                  arabic_correction=True, punctuation_correction=True, 
                  special_chars_removal=True, emoji_removal=True, 
                  comma_between_numbers_removal=True, number_correction=True, 
                  repeated_punctuation_removal=True,
                  date_abbrev_replacement=True, persian_label_abbrev_replacement=True,
                  law_abbrev_replacement=True, book_abbrev_replacement=True, 
                  other_abbrev_replacement=True,
                  number_conversion=True, en_fa_transliteration=True,
                  symbol_pronounciation=True,
                  hazm=True):
        """
        Normalizes the input text using a combination of cleaning, correction, and
        conversion techniques.

        Parameters
        ----------
        text : str
            The input text to be normalized.
        clean_urls : bool, optional
            If True, removes URLs from the text. Default is True.
        clean_emails : bool, optional
            If True, removes email addresses from the text. Default is True.
        convert_time : bool, optional
            If True, converts times to their textual representation. Default is True.
        convert_date : bool, optional
            If True, converts dates to their textual representation. Default is True.
        alphabet_correction : bool, optional
            If True, performs alphabet corrections. Default is True.
        semi_space_correction : bool, optional
            If True, corrects semi-spaces in the text. Default is True.
        english_correction : bool, optional
            If True, corrects English text in the input. Default is False.
        html_correction : bool, optional
            If True, fixes HTML issues in the text. Default is True.
        arabic_correction : bool, optional
            If True, corrects Arabic characters in the text. Default is True.
        punctuation_correction : bool, optional
            If True, corrects punctuation issues in the text. Default is True.
        special_chars_removal : bool, optional
            If True, removes special characters from the text. Default is True.
        emoji_removal : bool, optional
            If True, removes emojis from the text. Default is True.
        comma_between_numbers_removal : bool, optional
            If True, removes commas between numbers. Default is True.
        number_correction : bool, optional
            If True, corrects numerical representations. Default is True.
        repeated_punctuation_removal : bool, optional
            If True, removes repeated punctuation. Default is True.
        date_abbrev_replacement : bool, optional
            If True, replaces date abbreviations. Default is True.
        persian_label_abbrev_replacement : bool, optional
            If True, replaces Persian label abbreviations. Default is True.
        law_abbrev_replacement : bool, optional
            If True, replaces law abbreviations. Default is True.
        book_abbrev_replacement : bool, optional
            If True, replaces book abbreviations. Default is True.
        other_abbrev_replacement : bool, optional
            If True, replaces other abbreviations. Default is True.
        english_abbrev_replacement : bool, optional
            If True, replaces English abbreviations. Default is True.
        number_conversion : bool, optional
            If True, converts numbers to textual form. Default is True.
        en_fa_transliteration : bool, optional
            If True, transliterates English words to Persian. Default is True.
        symbol_pronounciation : bool, optional
            If True, replaces symbols with their pronounciation. Default is True.
        hazm : bool, optional
            If True, applies hazm normalization. Default is True.

        Returns
        -------
        str
            The normalized text.
        """
        if clean_urls:
            text = self.mail_url_cleaner.find_urls_clean(text)
        if clean_emails:
            text = self.mail_url_cleaner.find_mails_clean(text)

        if convert_time:
            text = self.date_time_to_text.time_to_text(text)
        if convert_date:
            text = self.date_time_to_text.date_to_text(text)
        
        if repeated_punctuation_removal:
            text = self.parsi_norm.remove_repeated_punctuation(text)
        if symbol_pronounciation:
            for symbol, pronunciation in SYMBOLS_PRONUNCIATION.items():
                text = text.replace(symbol, pronunciation)

        if alphabet_correction:
            text = self.parsi_norm.alphabet_correction(text)
        if semi_space_correction:
            text = self.parsi_norm.semi_space_correction(text)
        if english_correction:
            text = self.parsi_norm.english_correction(text)
        if html_correction:
            text = self.parsi_norm.html_correction(text)
        if arabic_correction:
            text = self.parsi_norm.arabic_correction(text)
        if punctuation_correction:
            text = self.parsi_norm.punctuation_correction(text)
        if special_chars_removal:
            text = self.parsi_norm.specials_chars(text)
        if emoji_removal:
            text = self.parsi_norm.remove_emojis(text)
        if comma_between_numbers_removal:
            text = self.parsi_norm.remove_comma_between_numbers(text)
        if number_correction:
            text = self.parsi_norm.number_correction(text)

        if date_abbrev_replacement:
            text = self.abbreviation.replace_date_abbreviation(text)
        if persian_label_abbrev_replacement:
            text = self.abbreviation.replace_persian_label_abbreviation(text)
        if law_abbrev_replacement:
            text = self.abbreviation.replace_law_abbreviation(text)
        if book_abbrev_replacement:
            text = self.abbreviation.replace_book_abbreviation(text)
        if other_abbrev_replacement:
            text = self.abbreviation.replace_other_abbreviation(text)

        if number_conversion:
            text = self.special_numbers.convert_numbers_to_text(text)

        if en_fa_transliteration:
            text = self.en_fa_transliterate(text)
        
        if hazm:
            text = self.hazm_norm.normalize(text)

        return text