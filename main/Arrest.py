from main.arrest_finder.ArrestFinder import ArrestFinder


class Arrest:
    REF = 'Réf.'
    PUBLISH_DATE = 'Date publication'
    CONTRACT_TYPE = 'Type de contrat'
    # RECTIFIED = 'Rectifié'
    # ARREST_DATE = 'Date de l\'arrêt'
    # ASK_PROCESS = 'Demande de procédure'  # <> Procédure traitée -> voir Article 1er last page (ou presque - si "Les
    # dépens ... sont réservés" => procédure continue et dons annulation pas traitée et ou indemnité réparatrice ?.)
    PROCESS_HANDLED = 'Procédure traitée'  # TODO

    def __init__(self, ref, reader, publish_date, contract_type):
        self.ref = ref
        self.reader = reader
        self.publish_date = publish_date
        self.contract_type = contract_type
        self.finder = ArrestFinder()
        self.isRectified = False
        self.arrest_date = None
        self.ask_procedures = None

    def as_dict(self):
        return {self.REF: self.ref,
                self.PUBLISH_DATE: self.publish_date,
                self.CONTRACT_TYPE: self.contract_type,
                self.finder.arrestDateFinder.label: self.arrest_date,
                self.finder.isRectifiedFinder.label: self.isRectified.real,
                self.finder.askProcessFinder.label: ', '.join([process.name for process in self.ask_procedures])}

    @classmethod
    def from_dic(cls, dic):
        arrest = cls(ref=dic[cls.REF], reader=None, publish_date=dic[cls.PUBLISH_DATE],
                     contract_type=dic[cls.CONTRACT_TYPE])
        return arrest

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
