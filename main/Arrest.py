from main.arrest_finder.ArrestFinder import ArrestFinder


class Arrest:
    REF = 'Réf.'
    N_PAGES = 'Pages'
    PUBLISH_DATE = 'Date publication'
    CONTRACT_TYPE = 'Type de contrat'

    def __init__(self, ref, reader, publish_date, contract_type):
        self.ref = ref
        self.reader = reader
        self.publish_date = publish_date
        self.contract_type = contract_type
        self.finder = ArrestFinder()
        self.isRectified = False
        self.arrest_date = None
        self.ask_procedures = None
        self.roles = []
        self.n_pages = 0

    def as_dict(self):
        return {self.REF: self.ref,
                self.N_PAGES: self.n_pages,
                self.finder.roleNumberFinder.label: '\n'.join(self.roles_numbers),
                self.finder.isRectifiedFinder.label: self.isRectified.real,
                self.PUBLISH_DATE: self.publish_date,
                self.CONTRACT_TYPE: self.contract_type,
                self.finder.arrestDateFinder.label: self.arrest_date,
                self.finder.askProcessFinder.label: ', '.join([process.label for process in self.ask_procedures])
                }

    @classmethod
    def from_dic(cls, dic):
        arrest = cls(ref=dic[cls.REF], reader=None, publish_date=dic[cls.PUBLISH_DATE],
                     contract_type=dic[cls.CONTRACT_TYPE])
        return arrest

    def find_all(self):
        return (self.is_rectified()
                .find_arrest_date()
                .find_ask_process()
                .find_role_number()
                .find_n_pages()
                )

    def is_rectified(self):
        self.isRectified = self.finder.isRectifiedFinder.find(self.ref, self.reader)
        return self

    def find_arrest_date(self):
        self.arrest_date = self.finder.arrestDateFinder.find(self.ref, self.reader, {
            self.finder.arrestDateFinder.IS_RECTIFIED_LABEL: self.isRectified})
        return self

    def find_ask_process(self):
        self.ask_procedures = self.finder.askProcessFinder.find(self.ref, self.reader, {
            self.finder.askProcessFinder.IS_RECTIFIED_LABEL: self.isRectified})
        return self

    def find_role_number(self):
        self.roles_numbers = self.finder.roleNumberFinder.find(self.ref, self.reader, {
            self.finder.roleNumberFinder.IS_RECTIFIED_LABEL: self.isRectified})
        return self

    def find_n_pages(self):
        self.n_pages = len(self.reader.pages)
        return self
