import re

from pypdf import PdfReader

from main.Exceptions.DataNotFoundException import DataNotFoundException


class FinderAbstract:
    FIRST_TITLE_PATTERN = r'I\.\s*Objets*\s*(de\s*la|de\s*s|du)\s*(requête|recours)'
    IS_RECTIFIED_LABEL = 'isRectified'

    def __init__(self, label):
        self.label = label

    def find(self, ref, reader, args=None):
        """Find data from Arrest file"""
        self.__check_args_contains(args)
        data = self.__find_data(ref, reader, args)
        return data

    def __check_args_contains(self, args):
        pass

    def __find_data(self, ref, reader, args):
        pass

    def __get_first_page(self, args):
        index_page = 0 if not args[self.IS_RECTIFIED_LABEL] else 1
        return index_page

    def args_contain_is_rectified(self, args):
        if args is None or self.IS_RECTIFIED_LABEL not in args:
            raise NotADirectoryError("{rectified} no in the dic".format(rectified=self.IS_RECTIFIED_LABEL))

    def extract_text_between_delimiters_1(self, ref, text, first_delimiter_pattern, second_delimiter_pattern):
        pattern_delimiter = re.compile(first_delimiter_pattern.pattern + r'(.*?)' + second_delimiter_pattern.pattern,
                                       re.DOTALL)
        match = pattern_delimiter.search(text)

        if match:
            return match.group(0).strip()
        else:
            raise DataNotFoundException(data=self.label, ref=ref, message="Delimiters not found in text")

    def extract_text_between_delimiters_for_reader(self, ref, reader: PdfReader, pattern_delimiter_1,
                                                   pattern_delimiter_2=None, page_1=None, page_2=None,
                                                   strict_2=True, reverse_1=False, reverse_2=False,
                                                   flags=re.IGNORECASE + re.DOTALL):
        """Extract text between 2 delimiters (the text contain the delimiters)"""

        delimiter_1 = re.compile(pattern_delimiter_1, flags)
        delimiter_2 = None
        if pattern_delimiter_2 is not None:
            delimiter_2 = re.compile(pattern_delimiter_2, flags)
        last_page = len(reader.pages) - 1

        first_page, second_page = self.__get_pages_search(page_1, page_2, last_page)

        self.__check_page_range(ref, last_page, first_page, second_page)

        if not reverse_1:
            current_page_1 = self.__ascending_search(ref, delimiter_1, first_page, reader, second_page, True)
        else:
            current_page_1 = self.__descending_search(ref, delimiter_1, first_page, reader, second_page, True)

        if delimiter_2 is None:
            current_page_2 = second_page
        else:
            if not reverse_2:
                current_page_2 = self.__ascending_search(ref, delimiter_2, current_page_1, reader, second_page,
                                                         strict_2)
            else:
                current_page_2 = self.__descending_search(ref, delimiter_2, current_page_1, reader, second_page,
                                                          strict_2)

        text = ''.join([page.extract_text() for page in reader.pages[current_page_1:current_page_2 + 1]])
        return self.extract_text_between_delimiters_for_string(ref, text, pattern_delimiter_1, pattern_delimiter_2,
                                                               flags)

    def extract_text_between_delimiters_for_string(self, ref, text, delimiter_1, delimiter_2, flags, strict_2=False):
        if delimiter_2 is None:
            pattern_delimiter = re.compile(delimiter_1 + r'(.*)', flags)
        else:
            pattern_delimiter = re.compile(delimiter_1 + r'(.*)' + delimiter_2, flags)
        match = pattern_delimiter.search(text)

        if match:
            return match.group(0).strip()
        else:
            if delimiter_2 is None or strict_2:
                raise DataNotFoundException(data=self.label, ref=ref, message="Delimiters not found in text")
            else:
                return self.extract_text_between_delimiters_for_string(ref, text, delimiter_1, None, flags)

    def __descending_search(self, ref, delimiter, first_page, reader, second_page, strict):
        current_page = second_page
        while current_page >= first_page:
            # Vérifier si le premier délimiteur est présent dans le texte
            current_text = reader.pages[current_page].extract_text()
            if delimiter.search(current_text) is None:
                current_page = current_page - 1
            else:
                break
        if current_page < first_page:
            if strict:
                raise DataNotFoundException(data=self.label, ref=ref,
                                            message="delimiter: \"{delimiter}\" not found in the text".format(
                                                delimiter=delimiter.pattern))
            else:
                current_page = first_page
        return current_page

    def __ascending_search(self, ref, delimiter, first_page, reader, second_page, strict):
        current_page = first_page
        while current_page <= second_page:
            # Vérifier si le premier délimiteur est présent dans le texte
            current_text = reader.pages[current_page].extract_text()
            if delimiter.search(current_text) is None:
                current_page = current_page + 1
            else:
                break
        if current_page > second_page:
            if strict:
                raise DataNotFoundException(data=self.label, ref=ref,
                                            message="delimiter: \"{delimiter}\" not found in the text".format(
                                                delimiter=delimiter.pattern))
            else:
                current_page = first_page
        return current_page

    @staticmethod
    def __get_pages_search(page_1, page_2, last_page):
        first_page = page_1
        second_page = page_2
        if page_1 is None:
            first_page = 0
        if page_2 is None:
            second_page = last_page
        return first_page, second_page

    @staticmethod
    def __check_page_range(ref, last_page, first_page, second_page):
        if first_page < 0:
            raise IndexError("{ref}, first_page: {page} < 0".format(ref=ref, page=first_page))
        if second_page < 0:
            raise IndexError("{ref}, second_page: {page} < 0".format(ref=ref, page=second_page))
        if first_page > last_page:
            raise IndexError(
                "{ref}, first_page: {page} > last_page: {last_page}".format(ref=ref, page=first_page,
                                                                            last_page=last_page))
        if second_page > last_page:
            raise IndexError(
                "{ref}, second_page: {page} > last_page: {last_page}".format(ref=ref, page=second_page,
                                                                             last_page=last_page))
        if first_page > second_page:
            raise IndexError(
                "{ref}, first_page: {first_page} > second_page: {second_page}".format(ref=ref, first_page=first_page,
                                                                                      second_page=second_page))
