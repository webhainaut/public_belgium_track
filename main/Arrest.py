from datetime import datetime

from main.arrest_finder.ArrestFinder import ArrestFinder


# @TODO Remove
class Arrest:
    REF = 'Réf.'
    N_PAGES = 'Pages'
    PUBLISH_DATE = 'Date publication'
    CONTRACT_TYPE = 'Type de contrat'
    ERRORS = 'Erreurs'

    def __init__(self, ref, reader, publish_date: datetime, contract_type):
        self.finder = ArrestFinder()

        self.ref = ref
        self.reader = reader
        self.publish_date = publish_date
        self.contract_type = contract_type
        self.n_pages = 0

        self.roles_numbers = []
        self.isRectified = False
        self.arrest_date = None
        self.ask_procedures = []
        self.rulings = []
        self.surplus = False
        self.keywords_find = {}
        self.keywords = {}
        self.errors = []

    def as_dict(self):
        ruling_label = ', '.join([ruling.label for ruling in self.rulings])
        if self.surplus:
            ruling_label = ruling_label + " (rejet surplus)"
        dic = {self.REF: self.ref,
               self.ERRORS: '\n'.join(self.errors),
               self.N_PAGES: self.n_pages,
               self.finder.roleNumberFinder.service: '\n'.join(self.roles_numbers),
               self.finder.isRectifiedFinder.service: self.isRectified.real,
               self.PUBLISH_DATE: self.publish_date,
               self.CONTRACT_TYPE: self.contract_type,
               self.finder.arrestDateFinder.service: self.arrest_date,
               self.finder.askProcessFinder.service: ', '.join([process.label for process in self.ask_procedures]),
               self.finder.rulingsFinder.service: ruling_label,
               }
        for keyword_title in self.keywords.keys():
            dic = dic | {keyword_title: '\n'.join(self.keywords_find[keyword_title])}
        for keyword_title in self.keywords.keys():
            for keyword in self.keywords[keyword_title]:
                dic = dic | {keyword_title + ": " + keyword: keyword in self.keywords_find[keyword_title]}
        return dic

    @classmethod
    def from_dic(cls, dic):
        arrest = cls(ref=dic[cls.REF], reader=None, publish_date=dic[cls.PUBLISH_DATE],
                     contract_type=dic[cls.CONTRACT_TYPE])
        return arrest

    def find_all(self):
        return (self.is_rectified()
                .find_arrest_date()
                .find_ask_process()
                .find_rulings()
                .find_role_number()
                .find_n_pages()
                .find_keywords("Mots clés", ["Exigences minimals" , "Signatures", "prix anormaux", "motivation formelle"])
                )

    def check_errors(self, errors):
        if errors is not None:
            self.errors.append(errors)

    def is_rectified(self):
        self.isRectified, errors = self.finder.isRectifiedFinder.find(self.ref, self.reader)
        self.check_errors(errors)
        return self

    def find_arrest_date(self):
        self.arrest_date, errors = self.finder.arrestDateFinder.find(self.ref, self.reader, {
            self.finder.arrestDateFinder.IS_RECTIFIED_LABEL: self.isRectified})
        self.check_errors(errors)
        return self

    def find_ask_process(self):
        self.ask_procedures, errors = self.finder.askProcessFinder.find(self.ref, self.reader, {
            self.finder.askProcessFinder.IS_RECTIFIED_LABEL: self.isRectified})
        if self.ask_procedures is None: self.ask_procedures = []
        self.check_errors(errors)
        return self

    def find_role_number(self):
        self.roles_numbers, errors = self.finder.roleNumberFinder.find(self.ref, self.reader, {
            self.finder.roleNumberFinder.IS_RECTIFIED_LABEL: self.isRectified})
        self.check_errors(errors)
        return self

    def find_rulings(self):
        rulings, errors = self.finder.rulingsFinder.find(self.ref, self.reader, {
            self.finder.rulingsFinder.IS_RECTIFIED_LABEL: self.isRectified})
        if rulings is not None:
            self.rulings, self.surplus = rulings
        self.check_errors(errors)
        return self

    def find_keywords(self, title, keywords):
        keywords_find, errors = self.finder.keywordsFinder.find(self.ref, self.reader, {
            self.finder.keywordsFinder.KEYWORDS: keywords})
        self.keywords[title] = keywords
        self.keywords_find[title] = keywords_find
        self.check_errors(errors)
        return self

    def find_n_pages(self):
        self.n_pages = len(self.reader.pages)
        return self
