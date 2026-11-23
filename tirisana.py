import csv
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SENSORI = (
    "PT08.S1(CO)",
    "PT08.S2(NMHC)",
    "PT08.S3(NOx)",
    "PT08.S4(NO2)",
    "PT08.S5(O3)",
)
MERKIS = "CO_virs_2"


def main():
    rindas = []
    tukšas = 0
    trūkst = 0
    with (ROOT / "dati" / "AirQualityUCI.csv").open(
        encoding="utf-8-sig", newline=""
    ) as fails:
        # UCI failā kolonnas atdala semikols, un abas nenosauktās kolonnas neizmantojam.
        lasītājs = csv.DictReader(fails, delimiter=";")
        for rinda in lasītājs:
            # Faila beigās ir tukšas rindas bez datuma un laika.
            if not rinda["Date"] and not rinda["Time"]:
                tukšas += 1
                continue

            # Aizstājam decimālo komatu ar punktu, lai vērtības varētu nolasīt kā skaitļus.
            lauki = [rinda[kolonna] for kolonna in ("CO(GT)", *SENSORI)]
            vērtības = [float(lauks.replace(",", ".")) if lauks else None for lauks in lauki]

            # Izlaižam stundas, kurās trūkst CO references vērtības vai kāda sensora rādījuma.
            if any(vērtība in (None, -200) for vērtība in vērtības):
                trūkst += 1
                continue

            # Apvienojam datumu un laiku, lai stundas varētu sakārtot hronoloģiski.
            laiks = datetime.strptime(
                rinda["Date"] + " " + rinda["Time"], "%d/%m/%Y %H.%M.%S"
            )
            co, *sensori = vērtības
            # References CO pārvēršam klasē, jo uzdevums ir noteikt pārsniegumu virs 2 mg/m³.
            rindas.append((laiks, *sensori, int(co > 2.0)))

    # Sakārtojam stundas, lai modeļa tests izmantotu jaunākos novērojumus.
    rindas.sort(key=lambda rinda: rinda[0])
    with (ROOT / "tirs.csv").open("w", encoding="utf-8", newline="") as fails:
        rakstītājs = csv.writer(fails)
        rakstītājs.writerow(("Datums_laiks", *SENSORI, MERKIS))
        rakstītājs.writerows(rindas)

    print(f"Rindas sākumā (bez galvenes): {len(rindas) + tukšas + trūkst}")
    print(f"Tukšas rindas: {tukšas}")
    print(f"Rindas ar trūkstošām nepieciešamajām vērtībām: {trūkst}")
    print(f"Rindas beigās: {len(rindas)}")


if __name__ == "__main__":
    main()
