# Analiza pięciu największych lig piłkarskich w Europie (2015/16-2025/26)

Projekt analityczny na danych o 19 763 meczach Premier League, La Ligi, Serie A, Bundesligi i Ligue 1. Dane są czyszczone w Pythonie (pandas), ładowane do bazy SQLite i analizowane zapytaniami SQL w notatniku Jupyter.

## Pytania, na które odpowiada analiza

1. Jak duża jest przewaga własnego boiska w każdej lidze i czy zmienia się w czasie, w tym w sezonie 2020/21 granym bez kibiców?
2. Która liga jest najbardziej bramkowa i czy zawsze nią była?
3. Która liga ma najwięcej fauli i kartek i w której sędziowie karzą faule najsurowiej?

## Główne wyniki

Szczegóły, zapytania SQL i wykresy: [notebooks/02_analysis.ipynb](notebooks/02_analysis.ipynb).

### 1. Przewaga własnego boiska

- W każdej lidze gospodarz wygrywa wyraźnie częściej niż gość: od 42,3% meczów w Serie A do 45,7% w La Lidze (goście wygrywają od 28,2% do 32,2%).
- W sezonie 2020/21, granym w dużej części bez kibiców, odsetek wygranych gospodarzy spadł w każdej lidze poniżej średniej z pozostałych sezonów: o 7,1 pkt proc. w Premier League i Ligue 1, o 4,5 w La Lidze, o 2,2 w Bundeslidze i o 1,7 w Serie A.
- Wynik sugeruje, że obecność publiczności zwiększa przewagę gospodarza, ale nie dowodzi związku przyczynowego.

### 2. Średnie ilości bramek na mecz w poszczególnych ligach


- Najwięcej goli pada w Bundeslidze (3,07 na mecz), a najmniej w La Lidze (2,63). Premier League ma 2,82, Serie A 2,73, a Ligue 1 2,71.
- Bundesliga była najbardziej bramkową ligą w 8 z 11 sezonów. Wyjątki: 2016/17 (Serie A i La Liga), 2020/21 (Serie A) i 2023/24 (Premier League).
- Od sezonu 2018/19 Bundesliga ma ponad 3,0 gola na mecz w każdym sezonie, a w pierwszych trzech sezonach miała 2,79-2,87.

### 3. Faule i kartki

- Najwięcej fauli i żółtych kartek jest w La Lidze (26,5 faula i 4,90 żółtej kartki na mecz), a najmniej w Premier League (21,5 i 3,47).
- Najsurowiej faule karane są w La Lidze (18,5 żółtej kartki na 100 fauli), a najłagodniej w Ligue 1 (14,7). Ligue 1 ma jednocześnie najwięcej czerwonych kartek na mecz (0,256), ale różnica względem La Ligi i Serie A jest niewielka.
- Mało kartek w Premier League wynika głównie z małej liczby fauli, a nie z łagodnych sędziów (16,2 żółtej kartki na 100 fauli to wartość ze środka stawki).

## Dane

Źródło: pliki CSV z serwisu [football-data.co.uk](https://www.football-data.co.uk) (wyniki i statystyki meczów).

Zakres: pierwsze ligi Anglii, Hiszpanii, Włoch, Niemiec i Francji, sezony od 2015/16 do 2025/26 (11 sezonów). Trwający sezon 2026/27 został pominięty, bo jest niepełny.

### Czyszczenie danych

- zmiana skrótowych nazw kolumn na czytelne (np. `HS` na `home_shots`),
- zamiana dat zapisanych tekstem na prawdziwe daty,
- usunięcie wierszy bez kluczowych informacji (data, drużyny, wynik),
- sprawdzenie duplikatów (0 znalezionych),
- kontrola, czy wynik meczu (gospodarz, remis, gość) zgadza się z liczbą goli (0 niezgodności),
- dodanie kolumn z ligą i sezonem.

### Jakość danych

Po czyszczeniu w bazie jest 19 763 meczów. Braki występują tylko w 8 wartościach: 6 brakujących kursów (po 3 w Serie A i Ligue 1) oraz 2 brakujące liczby strzałów (po 1 w Bundeslidze i Ligue 1). Takie mecze są pomijane w obliczeniach, których dotyczą. Sezon 2019/20 w Ligue 1 został przerwany z powodu pandemii, więc ma mniej meczów niż pozostałe. Zapytanie kontrolujące dane: [sql/00_data_checks.sql](sql/00_data_checks.sql).

## Struktura projektu

```
├── Data/
│   ├── raw/                 surowe pliki CSV (po jednym na ligę i sezon)
│   └── processed/           oczyszczony plik matches_clean.csv
├── notebooks/
│   └── 01_analysis.ipynb    analiza, zapytania SQL i wykresy
├── sql/
│   └── 00_data_checks.sql   kontrola jakości danych
├── src/
│   ├── clean_data.py        czyszczenie danych
│   └── build_db.py          budowa bazy SQLite
└── requirements.txt
```


## Ograniczenia

- Analiza opisuje różnice między ligami i sezonami, ale nie wyjaśnia ich przyczyn.
- Faule i kartki zależą zarówno od stylu gry zawodników, jak i od podejścia sędziów oraz przepisów w danym kraju, a dane nie pozwalają tych dwóch rzeczy rozdzielić.
- Pojedyncze sezony mają po 306-380 meczów na ligę, więc różnice rzędu 1-2 punktów procentowych między sąsiednimi sezonami to normalne wahania.

## Użyte narzędzia

Python (pandas, matplotlib), SQL (SQLite), Jupyter Notebook, Git i GitHub.