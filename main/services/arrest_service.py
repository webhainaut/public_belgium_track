import io

from pypdf import PdfReader

from main.Models.Models import ArrestModel, RulingModel, CaseModel, KeywordModel, ErrorModel
from main.arrest_finder.ArrestFinder import ArrestFinder


class ArrestService:

    def __init__(self):
        self.io = io
        self.finder = ArrestFinder()

    def get_arrest_from_pdf(self, ref, pdf):
        pdf_reader = PdfReader(self.io.BytesIO(pdf))
        arrest = ArrestModel(ref=ref)
        arrest.pages = self.find_n_pages(pdf_reader)
        arrest.language = self.find_language(ref, pdf_reader, arrest)
        arrest.is_rectified = self.is_rectified(ref, pdf_reader, arrest)
        arrest.chamber = self.find_chamber(ref, pdf_reader, arrest)
        arrest.arrest_date = self.find_arrest_date(ref, pdf_reader, arrest)
        arrest.cases = self.find_cases(ref, pdf_reader, arrest)
        arrest.rulings = self.find_rulings(ref, pdf_reader, arrest)
        arrest.keywords = self.find_keywords("Mots clés", ["Exigences minimals", "Signatures", "prix anormaux",
                                                           "motivation formelle"], ref, pdf_reader, arrest)
        # arrest.procedures = self.find_procedure(ref, pdf_reader, arrest)
        # arrest.contract_type = self.find_contract_type(ref, pdf_reader, arrest)
        # arrest.avis = self.find_avis(ref, pdf_reader, arrest)
        # arrest.en_causes = self.find_avis(ref, pdf_reader, arrest)
        # arrest.contres = self.find_avis(ref, pdf_reader, arrest)
        # arrest.intervenants = self.find_avis(ref, pdf_reader, arrest)
        arrest.set_path()

        return arrest

    @staticmethod
    def check_errors(e, arrest):
        if e is not None:
            arrest.errors.append(ErrorModel(message=e))

    @staticmethod
    def find_n_pages(reader):
        return len(reader.pages)

    def find_language(self, ref, pdf_reader, arrest):
        # TODO
        return "fr"

    def is_rectified(self, ref, reader, arrest):
        is_rectified, e = self.finder.isRectifiedFinder.find(ref, reader)
        self.check_errors(e, arrest)
        return is_rectified

    def find_chamber(self, ref, pdf_reader, arrest):
        # TODO
        return 6

    def find_arrest_date(self, ref, reader, arrest):
        arrest_date, e = self.finder.arrestDateFinder.find(ref, reader, {
            self.finder.arrestDateFinder.IS_RECTIFIED_LABEL: arrest.is_rectified})
        self.check_errors(e, arrest)
        return arrest_date

    def find_rulings(self, ref, reader, arrest):
        rulings_model = []
        rulings_find, e = self.finder.rulingsFinder.find(ref, reader, {
            self.finder.rulingsFinder.IS_RECTIFIED_LABEL: arrest.is_rectified})
        rulings, surplus = rulings_find
        for ruling in rulings:
            rulings_model.append(RulingModel(ruling=ruling, surplus=surplus))
        self.check_errors(e, arrest)
        return rulings_model

    def find_cases(self, ref, reader, arrest):
        cases = []
        roles_numbers, e = self.finder.roleNumberFinder.find(ref, reader, {
            self.finder.roleNumberFinder.IS_RECTIFIED_LABEL: arrest.is_rectified})
        for roles_number in roles_numbers:
            cases.append(CaseModel(numRole=roles_number))
        self.check_errors(e, arrest)
        return cases

    def find_keywords(self, title, keywords, ref, reader, arrest):
        keywords_model = []
        keywords_find, e = self.finder.keywordsFinder.find(ref, reader, {
            self.finder.keywordsFinder.KEYWORDS: keywords})
        for keyword in keywords_find:
            keywords_model.append(KeywordModel(word=keyword, title=title))
        self.check_errors(e, arrest)
        return keywords_model

    def find_ask_process(self, ref, reader, arrest):
        # TODO Part of the procedures
        ask_procedures, e = self.finder.askProcessFinder.find(ref, reader, {
            self.finder.askProcessFinder.IS_RECTIFIED_LABEL: arrest.is_rectified})
        if ask_procedures is None: ask_procedures = []
        self.check_errors(e, arrest)
        return ask_procedures

    def find_procedure(self, ref, pdf_reader, arrest):
        # TODO
        # procedures = []
        # ask_procedures = self.find_ask_process(ref, pdf_reader, arrest)
        # resolvd_procedures =
        # arrest.arrest_date
        # for ask_procedure in ask_procedures:
        #     procedure_model = ProcedureModel(process=ask_procedure, request_date=ask_procedure_date,
        #                            urgence=ask_procedure_urgence)
        #     if ask_procedure in resolvd_procedures:
        #         procedure_model.decision_date = arrest.arrest_date
        #     procedures.append(procedure_model)
        pass
