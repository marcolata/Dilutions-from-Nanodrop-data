# 🧪 Funky.py — Nanodrop Dilution Calculator

A Python script to process CSV files exported from the **Nanodrop**, clean the data, and automatically calculate dilution parameters for nucleic acid and protein samples.

---

## 📋 Requirements

- Python 3.7+
- pandas
- numpy

Install dependencies:

```bash
pip install pandas numpy
```

---

## 🔧 Available Functions

The script contains **three functions**, each solving a different dilution scenario based on the formula **C1·V1 = C2·V2**.

---

### 1. `concentración_final(archivo_csv, vol_inicial, vol_final)`

Calculates the **final concentration (C2)** you will obtain by diluting a fixed sample volume into a fixed final volume.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `archivo_csv` | str | — | Path to the Nanodrop CSV file |
| `vol_inicial` | float | `10` | Sample volume taken (µL) |
| `vol_final` | float | `50` | Total dilution volume (µL) |

**Output columns:** `Sample ID`, `C1`, `Unit`, `C2_Final`, `Vol_inicial`, `Vol_final`, `Vol_diluyente`

```python
from Funky import concentración_final

df = concentración_final("results.csv", vol_inicial=10, vol_final=50)
print(df)
```

---

### 2. `volumen_inicial(archivo_csv, vol_final, concentración_final)`

Calculates the **sample volume (V1)** you need to take in order to reach a desired final concentration in a fixed total volume.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `archivo_csv` | str | — | Path to the Nanodrop CSV file |
| `vol_final` | float | `50` | Desired total dilution volume (µL) |
| `concentración_final` | float | `10` | Target concentration C2 (ng/µL) |

> ⚠️ If a sample is already more dilute than the target, `Vol_diluyente` will be set to `NaN`.

**Output columns:** `Sample ID`, `C1`, `Unit`, `Vol_inicial`, `Vol_diluyente`, `C2`

```python
from Funky import volumen_inicial

df = volumen_inicial("results.csv", vol_final=50, concentración_final=10)
print(df)
```

---

### 3. `volumen_final(archivo_csv, vol_inicial, concentración_final)`

Calculates the **final volume (V2)** to which you must bring the sample to reach a desired concentration, always taking the same initial volume.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `archivo_csv` | str | — | Path to the Nanodrop CSV file |
| `vol_inicial` | float | `10` | Fixed sample volume taken (µL) |
| `concentración_final` | float | `10` | Target concentration C2 (ng/µL) |

> ⚠️ If the original sample (C1) is already less concentrated than the target (C2), volumes are set to `NaN` — you cannot concentrate a sample by adding liquid.

**Output columns:** `Sample ID`, `C1`, `Unit`, `Vol_final`, `Vol_diluyente`, `Vol_inicial`, `C2`

```python
from Funky import volumen_final

df = volumen_final("results.csv", vol_inicial=10, concentración_final=10)
print(df)
```

---

## 📁 Expected CSV Format

The CSV file must contain at least the following columns (standard Nanodrop export format):

| Sample ID | Nucleic Acid/protein | Unit (ng/µL , µg/µL) |
|---|---|---|
| B | 0.5 | ng/µL |
| M1 | 245.3 | ng/µL |
| M2 | 180.1 | ng/µL |

> Blanks (`Sample ID == 'B'`) are automatically removed from the analysis.

---

## 📐 Base Formula

All functions are based on the dilution equation:

```
C1 × V1 = C2 × V2
```

Depending on the scenario, the unknown variable (`C2`, `V1`, or `V2`) is solved for.

---

## 💡 Full Workflow Example

```python
import pandas as pd
from Funky import volumen_inicial

# Calculate how much to take from each sample to get 10 ng/µL in 50 µL total
df = volumen_inicial("nanodrop.csv", vol_final=50, concentración_final=10)

```
