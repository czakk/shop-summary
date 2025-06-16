# 🛒 Shop‑Summary

Aplikacja CLI do generowania podsumowań sprzedaży.

---

### 📝 Opis

„Shop‑Summary” to narzędzie do agregowania i wizualizowania danych sprzedażowych.

- analizę przychodów w wybranym przedziale czasowym,
- identyfikację najcenniejszych produktów,
- eksport wygenerowanych raportów do pliku xlsx

---

### ✅ Funkcjonalności

- import danych sprzedażowych z plików,
- generowanie wykresów i tabel podsumowujących,
- eksport wyników do XLSX i PDF

---

## 🛠️ Instalacja

#### Wymagane wersje
- Python 3.13
- Poetry >2.0

1. Sklonuj repozytorium:
   ```bash
   git clone https://github.com/czakk/shop-summary.git
   cd shop-summary
   ```
2. Instalacja zależności:
   ```bash
   poetry install
   ```

---

## 🚀 Użycie

### CLI

Uruchomienie aplikacji
```bash
shop-summary$ poetry run generate
```
W folderze `reports/` pojawią się raporty dla poszczególnych dni,
natomaist w głównym folderze pojawi się plik `Summary.pdf` zawierający podsumowanie wszystkich danych


Generowanie danych testowych
```bash
shop-summary$ poetry run dummy
```

---

### 🧪 Testy

Uruchom zestaw testów:
```bash
poetry run pytest
```

---

### 🏗️ Architektura

- **src**: moduł `src/`
- **data**: `data/` – przechowywanie danych wejściowych
- **validation_errors**: `data/validation_error/` – lokalizacja plików json zawierających błędy podczas walidacji 
  danych wejściowych
- **reports**: `reports/` – raporty dla poszczególnych dni

---
