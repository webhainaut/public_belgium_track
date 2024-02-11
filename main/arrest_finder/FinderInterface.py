import re

from main.Exceptions.DataNotFoundException import DataNotFoundException


class FinderInterface:
    IS_RECTIFIED_LABEL = 'isRectified'

    def __init__(self, label):
        self.label = label

    def find(self, ref, reader, args=None):
        """Find data from Arrest file"""
        raise NotImplementedError

    def extract_text_between_delimiters(self, ref, text, first_delimiter_pattern, second_delimiter_pattern):
        pattern_delimiter = re.compile(first_delimiter_pattern.pattern + r'(.*?)' + second_delimiter_pattern.pattern,
                                       re.DOTALL)
        match = pattern_delimiter.search(text)

        if match:
            return match.group(0).strip()
        else:
            raise DataNotFoundException(data=self.label, ref=ref, message="Delimiters not found in text")
