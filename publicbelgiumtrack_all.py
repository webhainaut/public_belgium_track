import locale
import logging
from datetime import datetime

from main.app.public_track_service import PublicTrackService

locale.setlocale(locale.LC_ALL, 'fr_BE.UTF-8')
logging.basicConfig(level=logging.INFO)


def main():
    public_track_service = PublicTrackService()

    # public_track_service.download(259209)
    # public_track_service.download_all(REFS)
    # public_track_service.update_year(2024)
    # public_track_service.update_all(REFS)
    # public_track_service.update(260454)

    public_track_service.print_to_excel(259019)



# REFS = [260454, 260616]
# REFS = [247478, 255267, 255438, 255470, 255472, 255668, 255678, 255679, 255681, 255844, 255962, 255964, 256014, 256484,
#         256672, 257478, 257654, 257819, 257919, 257921, 258204, 255824, 258274, 255568, 258317, 256090, 256352, 256552,
#         256835, 256952, 257003, 255570, 257985, 257647, 257248, 257984, 258070, 257009, 258245, 256675, 261996, 258994,
#         259019, 259068, 259209]
REFS = [259019, 259068, 259209]
if __name__ == "__main__":
    start_time = datetime.now()
    main()
    end_time = datetime.now()
    execution_time = end_time - start_time
    print(f"Le script a pris {execution_time} secondes pour s'exécuter.")
