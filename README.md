# 🧪 Funky.py — Nanodrop Dilution Calculator

A Python script to process CSV files exported from the **Nanodrop**, clean the data, and automatically calculate dilution parameters for nucleic acid samples.

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

## 📁 Project Structure

```
your-project/
│
├── Funky.py          # Core functions
├── Workbook.ipynb    # Main working notebook (run your analyses here)
└── *.csv             # Nanodrop export files
```

---

## 🚀 How to Use

All analysis is done through **`Workbook.ipynb`**. Open it  and follow these steps:

**1. List available CSV files**
The notebook scans your folder and prints the available Nanodrop files:
```python
path = "*.csv"
files = glob.glob(path, recursive=True)
```

**2. Select your file**
```python
archivo = "archivo.csv"
```

**3. Call the function you need**
```python
df = volumen_inicial(archivo, vol_final=50, concentración_final=10)
print(df)
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

> 💡 `vol_inicial` and `vol_final` are set to `10` and `50` µL by default, but you can pass any values that fit your experiment:
> ```python
> # Using defaults
> df = concentración_final(archivo)
>
> # Custom volumes
> df = concentración_final(archivo, vol_inicial=5, vol_final=100)
> ```

**Output columns:** `Sample ID`, `C1`, `Unit`, `C2_Final`, `Vol_inicial`, `Vol_final`, `Vol_diluyente`

---

### 2. `volumen_inicial(archivo_csv, vol_final, concentración_final)`

Calculates the **sample volume (V1)** you need to take in order to reach a desired final concentration in a fixed total volume.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `archivo_csv` | str | — | Path to the Nanodrop CSV file |
| `vol_final` | float | `50` | Desired total dilution volume (µL) |
| `concentración_final` | float | `10` | Target concentration C2 (ng/µL) |

> 💡 `vol_final` and `concentración_final` are set to `50` µL and `10` ng/µL by default. Adjust them to match your target:
> ```python
> # Using defaults
> df = volumen_inicial(archivo)
>
> # Custom target: 25 µL total at 20 ng/µL
> df = volumen_inicial(archivo, vol_final=25, concentración_final=20)
> ```

> ⚠️ If a sample is already more dilute than the target, `Vol_diluyente` will be set to `NaN`.

**Output columns:** `Sample ID`, `C1`, `Unit`, `Vol_inicial`, `Vol_diluyente`, `C2`

---

### 3. `volumen_final(archivo_csv, vol_inicial, concentración_final)`

Calculates the **final volume (V2)** to which you must bring the sample to reach a desired concentration, always taking the same initial volume.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `archivo_csv` | str | — | Path to the Nanodrop CSV file |
| `vol_inicial` | float | `10` | Fixed sample volume taken (µL) |
| `concentración_final` | float | `10` | Target concentration C2 (ng/µL) |

> 💡 `vol_inicial` and `concentración_final` are set to `10` µL and `10` ng/µL by default. Change them to suit your protocol:
> ```python
> # Using defaults
> df = volumen_final(archivo)
>
> # Custom: take 5 µL and dilute to 2 ng/µL
> df = volumen_final(archivo, vol_inicial=5, concentración_final=2)
> ```

> ⚠️ If the original sample (C1) is already less concentrated than the target (C2), volumes are set to `NaN` — you cannot concentrate a sample by adding liquid.

**Output columns:** `Sample ID`, `C1`, `Unit`, `Vol_final`, `Vol_diluyente`, `Vol_inicial`, `C2`

---

## 📁 Expected CSV Format

The CSV file must contain at least the following columns (standard Nanodrop export format):

| Sample ID | Nucleic Acid | Unit |
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
