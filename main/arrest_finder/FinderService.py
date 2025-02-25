import logging
import re

from pypdf import PdfReader

from main.Exceptions.DataNotFoundException import DataNotFoundException


class FinderService:
    IS_RECTIFIED_LABEL = 'isRectified'
    DATE_EXTRACT_PATTERN = r'(\d{1,2})\s*([^\d\s]+)\s*(\d{4})'
    DATE_PATTERN = r'(\d{1,2}\s*[\wé]+\s*\d{4})'

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def _get_first_page(self, args):
        index_page = 0 if not args[self.IS_RECTIFIED_LABEL] else 1
        return index_page

    def args_contain_is_rectified(self, args):
        if args is None or self.IS_RECTIFIED_LABEL not in args:
            raise NotADirectoryError("{rectified} no in the dic".format(rectified=self.IS_RECTIFIED_LABEL))

    def normalize_date_string(self, service, date_line, ref):
        """
        Normalise une chaîne de date mal formatée en un format standard.
        Exemples: "1ermars2025" -> "1 mars 2025", "9 février2024" -> "9 février 2024".
        Gère "1er" et supprime "du".
        Raises: DataNotFoundException si aucune date n'est trouvée.
        """
        date_line_clean = " ".join(date_line.split()).lower()
        date_line_clean = date_line_clean.replace('1er', '1').replace('du', '')

        date_part = re.search(self.DATE_PATTERN, date_line_clean)
        if not date_part:
            raise DataNotFoundException(data=service, ref=ref)

        date_str = date_part.group(1)
        return re.sub(self.DATE_EXTRACT_PATTERN, lambda m: f"{m.group(1)} {m.group(2)} {m.group(3)}", date_str)

    def extract_text_between_delimiters_for_reader(self, service, ref, reader: PdfReader, pattern_delimiter_1=None,
                                                   pattern_delimiter_2=None, page_1=None, page_2=None,
                                                   strict=True, reverse_1=False, reverse_2=False,
                                                   flags=re.IGNORECASE + re.DOTALL):
        """Extract text between 2 delimiters (the text contain the delimiters)"""
        delimiter_1 = None
        if pattern_delimiter_1 is not None:
            delimiter_1 = re.compile(pattern_delimiter_1, flags)
        delimiter_2 = None
        if pattern_delimiter_2 is not None:
            delimiter_2 = re.compile(pattern_delimiter_2, flags)
        last_page = len(reader.pages) - 1

        first_page, second_page = self.__get_pages_search(page_1, page_2, last_page)

        self.__check_page_range(ref, last_page, first_page, second_page)
        if delimiter_1 is None:
            current_page_1 = first_page
        else:
            if not reverse_1:
                current_page_1 = self.__ascending_search(service, ref, delimiter_1, first_page, reader, second_page,
                                                         True)
            else:
                current_page_1 = self.__descending_search(service, ref, delimiter_1, first_page, reader, second_page,
                                                          True)

        if delimiter_2 is None:
            current_page_2 = second_page
        else:
            if not reverse_2:
                current_page_2 = self.__ascending_search(service, ref, delimiter_2, current_page_1, reader, second_page,
                                                         strict)
            else:
                current_page_2 = self.__descending_search(service, ref, delimiter_2, current_page_1, reader,
                                                          second_page, strict)
        text = ''.join([page.extract_text() for page in reader.pages[current_page_1:current_page_2 + 1]])
        return self.extract_text_between_delimiters_for_string(service, ref, text, pattern_delimiter_1,
                                                               pattern_delimiter_2,
                                                               flags, strict)

    def search_word(self, service, ref, reader: PdfReader, word, pattern_delimiter_1=None,
                    pattern_delimiter_2=None, page_1=None, page_2=None,
                    strict=True, reverse_1=False, reverse_2=False, flags=re.IGNORECASE + re.DOTALL):
        """ Recherche un mot 'word' """
        extract_text = self.extract_text_between_delimiters_for_reader(service, ref, reader, pattern_delimiter_1,
                                                                       pattern_delimiter_2, page_1, page_2, strict,
                                                                       reverse_1, reverse_2, flags)

        pattern_delimiter = re.compile(r'\W' + word + r'\W', flags)
        match = pattern_delimiter.search(extract_text)
        return match

    def extract_text_between_delimiters_for_string(self, service, ref, text, delimiter_1, delimiter_2,
                                                   flags=re.IGNORECASE + re.DOTALL, strict=False):
        pattern_1 = self.__get_pattern(delimiter_1)
        pattern_2 = self.__get_pattern(delimiter_2)
        pattern_delimiter = re.compile(pattern_1 + r'(.*)' + pattern_2, flags)
        match = pattern_delimiter.search(text)

        if match:
            return match.group(0).strip()
        else:
            if delimiter_2 is None or strict:
                raise DataNotFoundException(data=service, ref=ref, message="Delimiters not found in text")
            else:
                return self.extract_text_between_delimiters_for_string(service, ref, text, delimiter_1, None, flags,
                                                                       strict)

    @staticmethod
    def __get_pattern(delimiter):
        if delimiter is None:
            return ""
        else:
            return delimiter

    @staticmethod
    def __descending_search(service, ref, delimiter, first_page, reader, second_page, strict):
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
                raise DataNotFoundException(data=service, ref=ref,
                                            message="delimiter: \"{delimiter}\" not found in the text".format(
                                                delimiter=delimiter.pattern))
            else:
                current_page = first_page
        return current_page

    @staticmethod
    def __ascending_search(service, ref, delimiter, first_page, reader, second_page, strict):
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
                raise DataNotFoundException(data=service, ref=ref,
                                            message="delimiter: \"{delimiter}\" not found in the text".format(
                                                delimiter=delimiter.pattern))
            else:
                current_page = second_page
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
