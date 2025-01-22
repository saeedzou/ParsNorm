# ParsNorm: Advanced Persian Text Normalization

ParsNorm is a comprehensive text normalization tool for Persian (Farsi) text, designed to streamline text preprocessing, cleaning, and transformation. It is particularly suited for speech dataset creation, following methodologies inspired by "**CTC-Segmentation of Large Corpora for German End-to-End Speech Recognition**" [(arXiv:2007.09127)](arXiv:2007.09127). Accurate segmentation of speech datasets requires text to closely match how it is pronounced, and ParsNorm facilitates this by handling various text normalization and transliteration tasks.

One of its standout features is English-to-Persian Transliteration, which uniquely converts English words into their Persian phonetic equivalents. This capability is vital for Persian speech dataset creation, where non-Persian words in the text need accurate phonetic representation for proper segmentation. This improves segmentation accuracy and alignment between audio and text.

## Features

* **Unique English-to-Persian Transliteration**: Converts English words into their Persian phonetic equivalents, making this library a first of its kind.
* **Advanced Normalization**: Handles Persian-specific text cleaning and correction using multiple libraries like hazm, and parsinorm.
* **Date and Time Conversion**: Converts dates and times into textual formats.
* **Abbreviation Expansion**: Replaces common abbreviations with their full forms.
* **Emoji and Special Character Removal**: Cleans text by removing emojis and other unwanted characters.
* **Number Normalization**: Converts numerical expressions to their textual forms.
* **URL and Email Cleaning**: Detects and removes URLs and email addresses from the text.

## Methods

1. `en_fa_transliterate(text)`

    **Unique Feature**: Transliterates English words in the input text into Persian phonetic equivalents. This capability is exclusive to ParsNorm, making it essential for datasets containing English terms in Persian text.

    **Parameters**

    `text` (str): The input text containing English words.

    **Returns**

    (str): The text with English words transliterated to Persian.

2. `normalize(text, **kwargs)`

    Performs a comprehensive normalization process based on the options specified in the arguments.

    **Key Parameters**

    `text` (str): The input text to be normalized.

    `clean_urls` (bool): Remove URLs (default: True).

    `clean_emails` (bool): Remove email addresses (default: True).

    `convert_time` (bool): Convert times to text (default: True).

    `convert_date` (bool): Convert dates to text (default: True).

    `alphabet_correction` (bool): Apply Persian alphabet corrections (default: True).

    `semi_space_correction` (bool): Correct semi-spaces (default: True).

    `number_conversion` (bool): Convert numbers to textual form (default: True).

    `en_fa_transliteration` (bool): Transliterates English words to Persian (default: True).

    ... (*and many more options for fine-grained control*)

    **Returns**

    (str): Fully normalized text.

## References

* "CTC-Segmentation of Large Corpora for German End-to-End Speech Recognition" [(arXiv:2007.09127)](arXiv:2007.09127)

* Libraries used:

    `hazm`
    `parsinorm`

## Contributing

Contributions are welcome! If you have ideas for improving the library or want to report a bug, feel free to open an issue or submit a pull request.

## Author: Saeedreza Zouashkiani

[GitHub](https://github.com/saeedzou) | [Email](saeedzou2012@gmail.com)
