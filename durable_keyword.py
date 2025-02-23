import locale
from datetime import datetime

from main.Arrest import Arrest
from publicbelgiumtrack_all import PublicBelgiumTrack

locale.setlocale(locale.LC_ALL, 'fr_BE.UTF-8')


# @TODO Remove
def main():
    public_belgium_track = PublicBelgiumTrack("result/traveaux {year}.xlsx")
    arrests = []
    for ref in REFS:
        start_time = datetime.now()
        pdf_reader = public_belgium_track.webscraper.find_public_procurement(ref, "motcle")
        arrest = (Arrest(ref, pdf_reader, datetime.strptime("01/01/2000", '%d/%m/%Y'), "durable")
                  .find_all().find_keywords("Durable fr", ["environnementales", "environnementale", "environnemental",
                                                           "environnementaux", "circularité",
                                                           "économie circulaire", "circulaire", "écologiques",
                                                           "écologique", "circulaires", "vert", "verts", "réemploi",
                                                           "déchet", "déchets", "valorisation", "valorisations",
                                                           "recyclage", "recycler", "recyclé", "recycle", "réutilise",
                                                           "réutilisation", "réutilisé", "réutiliser", "réemployé",
                                                           "réemployer", "valorise", "valorisé", "valoriser", "7bis",
                                                           "7 de la loi", "Biodiversité", "la nature", "naturel",
                                                           "collecte", "Total cost of ownership", "TCO", "BREEAM",
                                                           "LCA", "LCC", "émission de CO2", "CO2", "émission",
                                                           "émissions de CO2", "émissions", "GRO", "TOTEM"])
                  .find_keywords("Durable nl",
                                 ["milieu", "materialendecreet", "hergebruik", "hergebruiken", "inzamelen",
                                  "ingezameld", "ingezamelde", "Inzamel", "inzamelt", "zamel", "zamelt",
                                  "nuttig toepassen", "verwijderen", "verwijde", "verwijder", "verwijdert",
                                  "groen", "ecologisch", "ecologische", "natuur", "GRO", "GRO-criteria",
                                  "duurzaam", "duurzaamheden", "duurzaamheid", "circulaire", "circulariteit",
                                  "circulaire economie", "milieuvriendelijk", "milieuvriendelijke",
                                  "milieuvriendelijkheid", "milieuvriendelijkheden", "afvalstof",
                                  "afvalstoffen", "afval", "afvallen", "verwerking", "verwerkingen",
                                  "verwerken", "verwerk", "verwerkt", "voorkomen", "afval voorkomen",
                                  "afval voorkomt", "voorkomt", "total cost ownership", "levencyclus",
                                  "leven cyclus", "omgeving", "BREEAM", "LCC", "LCA", "biodiversiteit",
                                  "CO2 uitstoot", "uitstoot", "klimaat", "klimaatverandering", "recyclage",
                                  "ecologie", "gerecycleerd", "TOTEM", "7bis", "7 bis", "7 van de wet",
                                  "7 van de overheidsopdrachtenwet", "BREEAM", "GRO-criteria",
                                  "GRO criteria"]))
        
        # arrest = (Arrest(ref, pdf_reader, datetime.strptime("01/01/2000", '%d/%m/%Y'), "durable")
        #           .find_all().find_keywords("Durable fr", ["la nature"]))

        end_time = datetime.now()
        execution_time = end_time - start_time
        print("arrest : {ref} add to list en {execution_time} s".format(ref=arrest.ref, execution_time=execution_time))
        arrests.append(arrest)

    public_belgium_track.write_to_excel(arrests)


# REFS = [180222, 183810, 194417, 206351, 210191, 211549, 212703, 214718, 215784, 218356, 218804, 220563, 220813,
#         221663, 222343, 224527, 225728, 226499, 226542, 227575, 227771, 229830, 230386, 231447, 231498, 231696, 231939,
#         231989, 232789, 236508, 234160, 234881, 234899, 235176, 235612, 235624, 237014, 237198, 237283, 237577, 238562,
#         238840, 238885, 240322, 240473, 241821, 242085, 242094, 242133, 242147, 242167, 242377, 242390, 242423, 242755,
#         243215, 243352, 243353, 243479, 244455, 244865, 245379, 245766, 246569, 247291, 247967, 248055, 248143, 248265,
#         248312, 249180, 249218, 249332, 249530, 249624, 249639, 250271, 250624, 250815, 251280, 251330, 251599, 251896,
#         251902, 252822, 252899, 253439, 253621, 253860, 254465, 254752, 254959, 255182, 255226, 255245, 255291, 255545,
#         255707, 255878, 256007, 256129, 256143, 257117, 257248, 257797, 257918, 257985, 258595, 258613, 258762, 259209,
#         259289, 251666]
REFS = [145163, 176389, 183810, 210191, 212703, 214718, 218356, 220563, 220813, 224527, 227575, 230386, 231447, 231498,
        231939, 231989, 234160, 234881, 234899, 235612, 236508, 237014, 237283, 240322, 242133, 242390, 243352, 243353,
        244865, 245379, 245766, 246569, 247291, 248055, 248265, 249218, 249332, 250271, 250815, 251599, 251896, 251902,
        253621, 255291, 256129, 257797, 258595, 259289]
# REFS = [255878]
if __name__ == "__main__":
    start_time = datetime.now()
    main()
    end_time = datetime.now()
    execution_time = end_time - start_time
    print(f"Le script a pris {execution_time} secondes pour s'exécuter.")
