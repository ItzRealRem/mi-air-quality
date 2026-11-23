import csv
from collections import Counter

from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.tree import DecisionTreeClassifier

from tirisana import MERKIS, ROOT, SENSORI


def main():
    with (ROOT / "tirs.csv").open(encoding="utf-8", newline="") as fails:
        rindas = list(csv.DictReader(fails))

    # Modelis saņem piecus sensoru rādījumus un mācās no CO pārsnieguma klases.
    x = [[float(rinda[kolonna]) for kolonna in SENSORI] for rinda in rindas]
    y = [int(rinda[MERKIS]) for rinda in rindas]

    # Pirmās 80% stundu izmantojam treniņam, atlikušās stundas atstājam testam.
    robeža = len(rindas) * 4 // 5
    x_treniņš, x_tests = x[:robeža], x[robeža:]
    y_treniņš, y_tests = y[:robeža], y[robeža:]

    # Ierobežojam koka dziļumu, lai tas veidotu dažus secīgus sensoru sliekšņu likumus.
    modelis = DecisionTreeClassifier(max_depth=4, random_state=42)
    modelis.fit(x_treniņš, y_treniņš)
    prognozes = modelis.predict(x_tests)

    # Biežāko klasi nosakām treniņa datos, pirms salīdzinām prognozes ar testa atbildēm.
    biežākā_klase = Counter(y_treniņš).most_common(1)[0][0]
    bāzes_prognozes = [biežākā_klase] * len(y_tests)
    precizitāte = accuracy_score(y_tests, prognozes)
    bāzes_precizitāte = accuracy_score(y_tests, bāzes_prognozes)
    tn, fp, fn, tp = confusion_matrix(y_tests, prognozes, labels=[0, 1]).ravel()

    print(f"Treniņa stundas: {len(y_treniņš)} | Testa stundas: {len(y_tests)}")
    print(f"Testa periods: {rindas[robeža]['Datums_laiks']} līdz {rindas[-1]['Datums_laiks']}")
    print(f"Bāzes līnijas klase: {biežākā_klase}")
    print(f"Modeļa precizitāte: {precizitāte:.2%} | Bāzes līnija: {bāzes_precizitāte:.2%}")
    print(f"Starpība: {(precizitāte - bāzes_precizitāte) * 100:+.2f} procentpunkti")
    if precizitāte <= bāzes_precizitāte:
        print("Modelis nepārspēj bāzes līniju.")
    print(f"Pareizi bez pārsnieguma: {tn} | Pareizi ar pārsniegumu: {tp}")
    print(f"Nepamatotas trauksmes: {fp} | Nepamanīti pārsniegumi: {fn}")


if __name__ == "__main__":
    main()
