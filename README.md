# CO pārsnieguma noteikšana no pieciem sensoriem

Projekts izmanto piecu gāzu sensoru stundas vidējos rādījumus, lai noteiktu, vai tajā pašā stundā CO koncentrācija pārsniedza 2 mg/m³. References analizatora mērījums nosaka pareizo klasi. Vērtība tieši 2 mg/m³ atbilst klasei 0.

## Palaišana

Projekts pārbaudīts ar Python 3.12 un scikit-learn 1.9.1. Projekta mapē izpildi šīs komandas.

```sh
python -m pip install scikit-learn==1.9.1
python tirisana.py
python modelis.py
```

- `dati/AirQualityUCI.csv` ir oriģinālais CSV no UCI. Informācija par avotu un lejupielādi ir failā `dati/AVOTS.txt`.
- `tirisana.py` izmanto Python standarta bibliotēku, izvada rindu skaitu pirms un pēc tīrīšanas un izveido `tirs.csv`.
- `modelis.py` apmāca lēmumu koku uz agrākajām 80% sakārtoto stundu un pārbauda to uz vēlākajām 20%. Terminālī redzama modeļa un bāzes līnijas precizitāte un abu veidu kļūdu skaits.
- `rezultati.md` apkopo rezultātus un apskata, kā varētu izmantot modeļa atbildi.

Datu avots ir Saverio Vito datu kopa *Air Quality* (2008). [UCI Machine Learning Repository](https://doi.org/10.24432/C59K5F)
