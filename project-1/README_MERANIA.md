# AS – Task Manager: porovnanie architektúr

Balík obsahuje tri implementácie **rovnakého REST API**: layered, modular-monolith, hexagonal.
Modulárny monolit má dva moduly **tasks** a **reporting**, reporting číta úlohy cez verejné rozhranie `tasks.public`.
Hexagonálne riešenie má doménový model, port `TaskRepository`, aplikačnú službu a dva adaptéry na ukladanie: SQLite a pamäťový.

## 1. Príprava (PowerShell vo Windows)

```powershell
cd project-1
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r layered/requirements.txt
python -m pip install -r modular-monolith/requirements.txt
python -m pip install -r hexagonal/requirements.txt
```

Ak sa PowerShell bráni aktivácii, používajte priamo `..\.venv\Scripts\python.exe` z podpriečinkov.

## 2. Spustenie všetkých testov a vytvorenie CSV

```powershell
python measure.py --label baseline
```

Výsledok: `results_baseline.csv` (12 API testov na architektúru, percentá pokrytia). Každá verzia sa testuje samostatným procesom s dočasnou SQLite databázou. **Nezamieňajte coverage za kvalitu architektúry.**

## 3. API a screenshoty

V priečinku konkrétnej verzie, napr. `layered`:
```powershell
python -m uvicorn app.main:app --reload
```
Otvor `http://127.0.0.1:8000/docs`, vykonaj `POST /tasks`, `GET /tasks`, `GET /tasks/summary`. Urob zábery (Swagger UI + odpoveď).

## 4. Zmena A: priorita úlohy

**Pred začiatkom experimentu urob kópiu celého `project-1`** (napr. `project-1-baseline`) mimo upravovaného priečinka alebo zaznamenaj Git commit.
Vo všetkých architektúrach zaveď `priority` s hodnotami `LOW`, `MEDIUM`, `HIGH`, default `MEDIUM` na úrovni schémy/API, modelu, ukladania a aplikačnej logiky. API kontrakt a testy musia byť vo všetkých troch prípadoch rovnaké. Testujte v novej prázdnej SQLite DB (existujúce tasks.db nemajú novú kolónku).
Potom spusti v zmenenom `project-1`:
```powershell
python measure.py --label priority --baseline ..\project-1-baseline
```
V `results_priority.csv` získate **reálne** počty upravených súborov, pridaných a odstránených riadkov (Git diff --no-index) aj testy a coverage. Zaznamenaj tiež architektonické časti: napr. API, doména, úložisko, reporting; spočítaj len tie, ktorých zdrojový kód sa skutočne zmenil.

## 5. Zmena B: výmena úložiska

Hexagonálny variant: v `hexagonal/app/main.py` zvoľ pred spustením `TASK_BACKEND=memory` pomocou PowerShell `$env:TASK_BACKEND = 'memory'`. Potom sa aplikačná služba nemení. Pre férový experiment priprav aj pre zvyšné architektúry pamäťové úložisko, zaznamenaj reálne zmeny v kóde a funkčné API testy. Výsledok **nevymýšľaj** a nemiešaj s experimentom A.

## 6. Evidencia výsledkov do prezentácie

- **Upravené súbory**: `changed_files` z CSV pri rovnakom scenári (nie baseline).
- **Riadky zmien (+/-)**: `added_lines` a `deleted_lines` z CSV.
- **Úspešné API testy**: `passed_tests` / 12; ak testy zlyhajú, uveď to.
- **Zasiahnuté moduly**: ručné zdokumentované vyhodnotenie podľa `git diff`, nejde o automaticky namerané číslo.
- **Screenshot**: terminál po measure.py, report CSV, Swagger a vybrané diffy.

## Metodické obmedzenia

Rozdiely v riadkoch a súboroch môžu súvisieť s implementáciou a pomenovaním komponentov; nie sú univerzálnou mierou kvality. Rovnaké API testy overujú správnosť správania, nie nezávisle všetky architektonické vlastnosti. Vyhodnocujte kvalitatívne aj smer závislostí a jednoduchosť výmeny infraštruktúry.
