# Rezultāti

## Datu izcelsme

UCI datu kopā *Air Quality* ir stundas vidējie rādījumi no pieciem metālu oksīdu sensoriem, kas atradās ielas līmenī kādā Itālijas pilsētā. Tajā pašā vietā sertificēts references analizators mērīja CO koncentrāciju. Šajā darbā tā rādījumi kalpo par pareizajām atbildēm. [Saverio Vito, Air Quality (2008), UCI Machine Learning Repository](https://doi.org/10.24432/C59K5F)

## Datu sagatavošana

Oriģinālajā CSV bija 9471 rinda bez galvenes. No tām 114 bija tukšas. Vēl 2013 stundās vismaz viens no pieciem nepieciešamajiem sensora rādījumiem vai references CO mērījums nebija pieejams. UCI trūkstošās vērtības apzīmē ar `-200`. Šīs rindas izlaidu, lai modelis mācītos no pilniem piemēriem ar zināmu atbildi. Palika 7344 stundas.

Nolasot CSV, izmantoju semikolu kā lauku atdalītāju un skaitļos aizstāju decimālo komatu ar punktu. No datuma un laika izveidoju vienu laika lauku un sakārtoju rindas hronoloģiski. No references CO vērtības izveidoju klasi 1, ja CO bija virs 2 mg/m³, un klasi 0, ja CO bija 2 mg/m³ vai mazāk. Oriģinālais fails ir saglabāts bez izmaiņām.

## Modeļa rezultāts

Lēmumu koks ar maksimālo dziļumu 4 izmanto tikai piecus sensoru rādījumus no tās pašas stundas. Apmācībai izmantoju pirmās 5875 stundas pēc tīrīšanas. Testā bija 1469 vēlākas stundas no 2005. gada 28. janvāra plkst. 12.00 līdz 4. aprīlim plkst. 14.00.

| Pieeja | Testa precizitāte |
| --- | ---: |
| Lēmumu koks | 89,86 % |
| Bāzes līnija, kas vienmēr prognozē treniņā biežāko klasi 0 | 62,29 % |

Modelis pārspēja bāzes līniju par 27,57 procentpunktiem. Tas pareizi atpazina 486 no 554 pārsniegumiem un 834 no 915 stundām bez pārsnieguma. Precizitāte raksturo šī perioda stundas ar pilniem rādījumiem. Citā vietā vai pēc sensoru novecošanas modelis var kļūdīties biežāk.

## Darbība reālā sistēmā

Ja modelis prognozētu pārsniegumu, sistēma izveidotu pārbaudes uzdevumu tehniķim. Tehniķis pārbaudītu norādītās stundas CO mērījumu ar kalibrētu references analizatoru, ja šāds mērījums ir pieejams.

- **Nepamatota trauksme (81 gadījums).** Tehniķis patērē laiku pārbaudei, lai gan references mērījums ir 2 mg/m³ vai mazāks. Biežas nepamatotas trauksmes var aizkavēt citu uzdevumu izpildi.
- **Nepamanīts pārsniegums (68 gadījumi).** Pārbaude netiek ierosināta, lai gan references mērījums ir virs 2 mg/m³. Šī kļūda ir sliktāka, jo tā var aizkavēt piesārņojuma avota atklāšanu un rīcību, ja paaugstināta koncentrācija turpinās.

## Lietojuma ierobežojums

Šo modeli nedrīkst izmantot kā vienīgo automātiskās evakuācijas signāla avotu. Modelis izlaida 68 pārsniegumus, izmanto stundas vidējos rādījumus un var palaist garām īslaicīgu koncentrācijas kāpumu.

## Pašvērtējums

Man izdevās sakārtot sensoru datus un apmācīt modeli, kas testā CO pārsniegumus noteica precīzāk par bāzes līniju. Modelis tomēr nepamanīja 68 pārsniegumus, tāpēc dažās stundās tehniķis nesaņemtu signālu, ka vajadzīga pārbaude. Nākamreiz es apskatītu, kas kopīgs stundām, kurās modelis kļūdījās, lai saprastu, kā samazināt nepamanīto pārsniegumu skaitu.
