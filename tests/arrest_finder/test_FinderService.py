from main.Exceptions.DataNotFoundException import DataNotFoundException
from main.arrest_finder.FinderService import FinderService
from tests.arrest_finder.testAbstract_Finder import TestAbstractFinder


class TestFinderService(TestAbstractFinder):

    def setUp(self):
        self.finder = FinderService()

    def test_kwargs_contain_arg_no_dic(self):
        with self.assertRaises(NotADirectoryError) as context:
            self.finder.args_contain_is_rectified(None)
        self.assertEqual("isRectified no in the dic", str(context.exception))

    def test_kwargs_contain_arg_bad_dic(self):
        with self.assertRaises(NotADirectoryError) as context:
            self.finder.args_contain_is_rectified({"coucou": 1})
        self.assertEqual("isRectified no in the dic", str(context.exception))

    def test_kwargs_contain_arg_ok(self):
        self.finder.args_contain_is_rectified({self.finder.IS_RECTIFIED_LABEL: True})

    def test_get_first_age_1(self):
        self.assertEqual(1, self.finder._get_first_page({self.finder.IS_RECTIFIED_LABEL: True}))

    def test_get_first_age_0(self):
        self.assertEqual(0, self.finder._get_first_page({self.finder.IS_RECTIFIED_LABEL: False}))

    def test_extract_text_between_delimiters_only_one_delimiter(self):
        arrest_ref = "255267"
        reader = self.read_pdf(arrest_ref)
        delimiter_1 = r"PAR CES MOTIFS,\s*LE CONSEIL D’ÉTAT DÉCIDE :"
        text = self.finder.extract_text_between_delimiters_for_reader("finder", arrest_ref, reader, delimiter_1)
        self.assertEqual("""PAR CES MOTIFS,  
LE CONSEIL D’ÉTAT DÉCIDE :  
 
 
Article 1er. 
 VIexturg - 22.440 - 21/22 
     La suspension de l’exécution de la décision prise par la Société du 
Logement de la Région de Bruxelles -capitale  d'attribuer le marché public de services 
d'études et de suivi des travaux de construction d'environ 70 logements (80 % de 
logements sociaux et 2 0 % de logements moyens) et un équipement collectif sis 
avenue des Cailles à 1170 Watermael -Boitsfort dans le cadre de l'Alliance Habitat à 
l'Association Pierre Blondel Architectes + Alt -O + COSEAS + BESP  est ordonnée.  VIexturg - 22.440 - 22/22 
 Article 2. 
 
    L’exécution immédiate du présent arrêt est ordonnée.  
 
Article 3. 
     
    Les pièces 6.1 à 6.7 du dossier des requérantes et les pièces 5 à 11 et 22 
à 26 du dossier administratif  sont, à ce stade de la procédure, tenues pour 
confidentielles.  
 
Article 4. 
 
    Conformément à l’article 3, § 1er, alinéa 2, de l’arrêté royal du 
5 décembre 1991 déterminant la procédure en référé devant le Conseil d’État, le 
présent arrêt sera notifié par télécopieur  aux partie s requérante s qui n’ont pas choisi 
la procédure  électroni que. 
 
Article 5. 
 
    Les dépens, en ce compris l’indemnité de procédure, sont réservés.  
 
 
    Ainsi prononcé à Bruxelles, en audience publique de la VIe chambre 
siégeant en référé, le 14 décembre  2022, par : 
 
  Imre Kovalovszky,   président de chambre,  
 Vincent Durieux,   greffier.  
 
 Le Greffier,  Le Président,  
 
 
 
 
 Vincent Durieux  Imre Kovalovszky""", text)

    def test_extract_text_between_delimiters_2_delimiter(self):
        arrest_ref = "255267"
        reader = self.read_pdf(arrest_ref)
        delimiter_1 = r"Par une requête"
        delimiter_2 = r"la société"
        text = self.finder.extract_text_between_delimiters_for_reader("finder", arrest_ref, reader, delimiter_1,
                                                                      delimiter_2)
        self.assertEqual("""Par une requête introduite le  27 octobre 2022 , la société à responsabilité 
limitée DXA.Archi,  la société à responsabilité limitée Atelier Caneva -s, Sami  
Kamar , la société à responsabilité limitée Ney & Partners WOW  et la société à 
responsabilité limitée XCO Engineering  demande nt la suspension , selon la 
procédure d’extrême urgence , de l’exécution  de « la décision prise par le Conseil 
d'administration de la Société""", text)

    def test_extract_text_between_delimiters_page_1(self):
        arrest_ref = "255267"
        reader = self.read_pdf(arrest_ref)
        delimiter_1 = r"Par une requête"
        delimiter_2 = r"la société"
        text = self.finder.extract_text_between_delimiters_for_reader("finder", arrest_ref, reader, delimiter_1,
                                                                      delimiter_2,
                                                                      page_1=1)
        self.assertEqual("""Par une requête introduite le 8 décembre 2022, les requérants demandent 
l’annulation de la décision précitée.  
 
II. Procédure  
 
    Par une ordonnance du  28 octobre 2022 , l’affaire a été fixée à l’audience 
du 21 novembre 2022.  
     
    La contribution et le s droit s visés respectivement aux articles 66, 6°, et 
70, du règlement général de procédure ont été acquittés.  
 
    La partie adverse a déposé une note d’observations et le dossier 
administratif.  
 
    M. Imre Kovalo vszky, président de chambre,  a exposé son rapport.  
 
    Mes Valentin Moury et Marie -Laure Jordens, avocats , et Mr Benoît 
Frisson, gérant, comparaissant  pour l es partie s requérante s, et Mes Virginie Dor et 
Mathilde Vilain XIIII , avocat s, comparaissant pour la partie adverse, ont été 
entendus en leurs observations.  
 
    M. Constantin Nikis , premier auditeur au Conseil d’État, a été entendu 
en son avis con traire . 
 
    Il est fait application des dispositions relatives à l’emploi des langues, 
inscrites au titre VI, chapitre II, des lois sur le Conseil d’État, coordonnées 
le 12 janvier 1973.  
 
III. Faits  utiles à l’examen de la demande  
 
    La partie adverse expose comme suit les faits de la cause  : 
 
«  1. La partie adverse, la Société""", text)

    def test_extract_text_between_delimiters_page_1_and_2(self):
        arrest_ref = "255267"
        reader = self.read_pdf(arrest_ref)
        delimiter_1 = r"Conformément"
        delimiter_2 = r"réservés"
        text = self.finder.extract_text_between_delimiters_for_reader("finder", arrest_ref, reader, delimiter_1,
                                                                      delimiter_2,
                                                                      page_1=21, page_2=21)
        self.assertEqual("""Conformément à l’article 3, § 1er, alinéa 2, de l’arrêté royal du 
5 décembre 1991 déterminant la procédure en référé devant le Conseil d’État, le 
présent arrêt sera notifié par télécopieur  aux partie s requérante s qui n’ont pas choisi 
la procédure  électroni que. 
 
Article 5. 
 
    Les dépens, en ce compris l’indemnité de procédure, sont réservés""", text)

    def test_extract_text_between_delimiters_page_2(self):
        arrest_ref = "255267"
        reader = self.read_pdf(arrest_ref)
        delimiter_1 = r"suspension"
        text = self.finder.extract_text_between_delimiters_for_reader("finder", arrest_ref, reader, delimiter_1,
                                                                      page_2=0)
        self.assertEqual("""suspension , selon la 
procédure d’extrême urgence , de l’exécution  de « la décision prise par le Conseil 
d'administration de la Société du Logement de la Région de Bruxelles -capitale (en 
abrégé SLRB) en date du 6 octobre 2022, notifiée officiellement par courrier 
recommandé daté du 10 octobre 2022 au groupement d'opérate urs économiques de 
la CIT É JARDICOLE, d'attribuer le marché public de services d'études et de suivi 
des travaux de construction d'environ 70 logements (80  % de logements sociaux et 
20 % de logements moyens) et un équipement collectif sis avenue des Cailles  à 1170 
Watermael -Boitsfort dans le cadre de l'Alliance Habitat à l'Association Pierre 
Blondel Architectes + Alt -O + COSEAS + BESP  [....] ».""", text)

    def test_extract_text_between_delimiters_delimiter_1_not_found(self):
        arrest_ref = "255267"
        reader = self.read_pdf(arrest_ref)
        delimiter_1 = r"coucou"
        with self.assertRaises(DataNotFoundException) as context:
            self.finder.extract_text_between_delimiters_for_reader("finder", arrest_ref, reader, delimiter_1)
        self.assertEqual("finder non trouvée dans le pdf 255267 delimiter: \"coucou\" not found in the text",
                         str(context.exception))

    def test_extract_text_between_delimiters_delimiter_2_not_found(self):
        arrest_ref = "255267"
        reader = self.read_pdf(arrest_ref)
        delimiter_1 = r"suspension"
        delimiter_2 = r"coucou"
        with self.assertRaises(DataNotFoundException) as context:
            self.finder.extract_text_between_delimiters_for_reader("finder", arrest_ref, reader, delimiter_1,
                                                                   delimiter_2)
        self.assertEqual("finder non trouvée dans le pdf 255267 delimiter: \"coucou\" not found in the text",
                         str(context.exception))

    def test_extract_text_between_delimiters_delimiter_1_and_2_not_found_no_strict_2(self):
        arrest_ref = "255267"
        reader = self.read_pdf(arrest_ref)
        delimiter_1 = r"coucou 1"
        delimiter_2 = r"coucou"
        with self.assertRaises(DataNotFoundException) as context:
            self.finder.extract_text_between_delimiters_for_reader("finder", arrest_ref, reader, delimiter_1,
                                                                   delimiter_2, strict=False)
        self.assertEqual("finder non trouvée dans le pdf 255267 delimiter: \"coucou 1\" not found in the text",
                         str(context.exception))

    def test_extract_text_between_delimiters_delimiter_2_not_found_no_strict(self):
        arrest_ref = "255267"
        reader = self.read_pdf(arrest_ref)
        delimiter_1 = r"suspension"
        delimiter_2 = r"coucou"
        text = self.finder.extract_text_between_delimiters_for_reader("finder", arrest_ref, reader, delimiter_1,
                                                                      delimiter_2, strict=False, reverse_1=True)
        self.assertEqual("""suspension de l’exécution de la décision prise par la Société du 
Logement de la Région de Bruxelles -capitale  d'attribuer le marché public de services 
d'études et de suivi des travaux de construction d'environ 70 logements (80 % de 
logements sociaux et 2 0 % de logements moyens) et un équipement collectif sis 
avenue des Cailles à 1170 Watermael -Boitsfort dans le cadre de l'Alliance Habitat à 
l'Association Pierre Blondel Architectes + Alt -O + COSEAS + BESP  est ordonnée.  VIexturg - 22.440 - 22/22 
 Article 2. 
 
    L’exécution immédiate du présent arrêt est ordonnée.  
 
Article 3. 
     
    Les pièces 6.1 à 6.7 du dossier des requérantes et les pièces 5 à 11 et 22 
à 26 du dossier administratif  sont, à ce stade de la procédure, tenues pour 
confidentielles.  
 
Article 4. 
 
    Conformément à l’article 3, § 1er, alinéa 2, de l’arrêté royal du 
5 décembre 1991 déterminant la procédure en référé devant le Conseil d’État, le 
présent arrêt sera notifié par télécopieur  aux partie s requérante s qui n’ont pas choisi 
la procédure  électroni que. 
 
Article 5. 
 
    Les dépens, en ce compris l’indemnité de procédure, sont réservés.  
 
 
    Ainsi prononcé à Bruxelles, en audience publique de la VIe chambre 
siégeant en référé, le 14 décembre  2022, par : 
 
  Imre Kovalovszky,   président de chambre,  
 Vincent Durieux,   greffier.  
 
 Le Greffier,  Le Président,  
 
 
 
 
 Vincent Durieux  Imre Kovalovszky""", text)

    def test_extract_text_between_delimiters_reverse_1(self):
        arrest_ref = "255267"
        reader = self.read_pdf(arrest_ref)
        delimiter_1 = r"suspension"
        delimiter_2 = r"7"
        text = self.finder.extract_text_between_delimiters_for_reader("finder", arrest_ref, reader, delimiter_1,
                                                                      delimiter_2,
                                                                      reverse_1=True)
        self.assertEqual("""suspension de l’exécution de la décision prise par la Société du 
Logement de la Région de Bruxelles -capitale  d'attribuer le marché public de services 
d'études et de suivi des travaux de construction d'environ 70 logements (80 % de 
logements sociaux et 2 0 % de logements moyens) et un équipement collectif sis 
avenue des Cailles à 117""", text)

    def test_extract_text_between_delimiters_reverse_1_and_2(self):
        arrest_ref = "255267"
        reader = self.read_pdf(arrest_ref)
        delimiter_1 = r"suspension"
        delimiter_2 = r"7"
        text = self.finder.extract_text_between_delimiters_for_reader("finder", arrest_ref, reader, delimiter_1,
                                                                      delimiter_2,
                                                                      reverse_1=True,
                                                                      reverse_2=True)
        self.assertEqual("""suspension de l’exécution de la décision prise par la Société du 
Logement de la Région de Bruxelles -capitale  d'attribuer le marché public de services 
d'études et de suivi des travaux de construction d'environ 70 logements (80 % de 
logements sociaux et 2 0 % de logements moyens) et un équipement collectif sis 
avenue des Cailles à 1170 Watermael -Boitsfort dans le cadre de l'Alliance Habitat à 
l'Association Pierre Blondel Architectes + Alt -O + COSEAS + BESP  est ordonnée.  VIexturg - 22.440 - 22/22 
 Article 2. 
 
    L’exécution immédiate du présent arrêt est ordonnée.  
 
Article 3. 
     
    Les pièces 6.1 à 6.7""", text)

    def test_extract_text_between_delimiters_reverse_only_2(self):
        arrest_ref = "255267"
        reader = self.read_pdf(arrest_ref)
        delimiter_1 = r"suspension"
        delimiter_2 = r"7"
        text = self.finder.extract_text_between_delimiters_for_reader("finder", arrest_ref, reader, delimiter_1,
                                                                      delimiter_2,
                                                                      page_1=19,
                                                                      reverse_2=True)
        self.assertEqual("""suspension de l’exécution de l’acte attaqué, qui 
l’emporterait sur ses avantages.  
 
VI. Confidentialité  
 
    Les parties requérantes demandent que la confidentialité de leur offre, 
qu’elles déposent en pièces 6.1 à 6.7 de leur dossier, demeu re confidentielle.  
 
    La partie adverse précise, quant à elle, qu’elle dépose à titre confidentiel 
les demandes de participation des candidats (pièces n° 5 à 11  du dossier 
administratif ), et les  offres des soumissionnaires (pièces n° 22 à 26  du dossier 
administratif).  
 
    Ces demandes n’étant pas contestées, il y a lieu, à ce stade de la 
procédure, de maintenir la confidentialité des pièces concernées.  
 
 
PAR CES MOTIFS,  
LE CONSEIL D’ÉTAT DÉCIDE :  
 
 
Article 1er. 
 VIexturg - 22.440 - 21/22 
     La suspension de l’exécution de la décision prise par la Société du 
Logement de la Région de Bruxelles -capitale  d'attribuer le marché public de services 
d'études et de suivi des travaux de construction d'environ 70 logements (80 % de 
logements sociaux et 2 0 % de logements moyens) et un équipement collectif sis 
avenue des Cailles à 1170 Watermael -Boitsfort dans le cadre de l'Alliance Habitat à 
l'Association Pierre Blondel Architectes + Alt -O + COSEAS + BESP  est ordonnée.  VIexturg - 22.440 - 22/22 
 Article 2. 
 
    L’exécution immédiate du présent arrêt est ordonnée.  
 
Article 3. 
     
    Les pièces 6.1 à 6.7""", text)

    def test_extract_text_between_delimiters_page_1_neg(self):
        arrest_ref = "255267"
        reader = self.read_pdf(arrest_ref)
        delimiter_1 = r"suspension"
        with self.assertRaises(IndexError) as context:
            self.finder.extract_text_between_delimiters_for_reader("finder", arrest_ref, reader, delimiter_1, page_1=-2)
        self.assertEqual("255267, first_page: -2 < 0", str(context.exception))

    def test_extract_text_between_delimiters_page_1_error(self):
        arrest_ref = "255267"
        reader = self.read_pdf(arrest_ref)
        delimiter_1 = r"suspension"
        with self.assertRaises(IndexError) as context:
            self.finder.extract_text_between_delimiters_for_reader("finder", arrest_ref, reader, delimiter_1,
                                                                   page_1=500)
        self.assertEqual("255267, first_page: 500 > last_page: 21", str(context.exception))

    def test_extract_text_between_delimiters_page_2_neg(self):
        arrest_ref = "255267"
        reader = self.read_pdf(arrest_ref)
        delimiter_1 = r"suspension"
        with self.assertRaises(IndexError) as context:
            self.finder.extract_text_between_delimiters_for_reader("finder", arrest_ref, reader, delimiter_1, page_2=-2)
        self.assertEqual("255267, second_page: -2 < 0", str(context.exception))

    def test_extract_text_between_delimiters_page_2_error(self):
        arrest_ref = "255267"
        reader = self.read_pdf(arrest_ref)
        delimiter_1 = r"suspension"
        with self.assertRaises(IndexError) as context:
            self.finder.extract_text_between_delimiters_for_reader("finder", arrest_ref, reader, delimiter_1,
                                                                   page_2=500)
        self.assertEqual("255267, second_page: 500 > last_page: 21", str(context.exception))

    def test_extract_text_between_delimiters_page_1_sup_page2(self):
        arrest_ref = "255267"
        reader = self.read_pdf(arrest_ref)
        delimiter_1 = r"suspension"
        with self.assertRaises(IndexError) as context:
            self.finder.extract_text_between_delimiters_for_reader("finder", arrest_ref, reader, delimiter_1, page_1=10,
                                                                   page_2=5)
        self.assertEqual("255267, first_page: 10 > second_page: 5", str(context.exception))
