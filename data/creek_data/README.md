# Creek data

Field deployment at Rocky Branch Creek, downtown Columbia, SC. One continuous run of about 17.6 h starting 13 March 2025: the flow-through NMR logged T2 curves while the [in-situ water-quality sensor](https://github.com/ARTS-Laboratory/In-Situ-Water-Quality-Sensor/tree/main/System_development/Jocassee/V0.6.0) logged pH, temperature, turbidity and conductivity.

## Contents

| Path | What it holds |
|---|---|
| `T2 Raw Data from creek/` | All 2,788 raw T2 curves in four session folders (SPIE4–SPIE7), plus `scan_index.csv` with per-curve time. See its README. |
| `processed_t2_data/N.csv` | The 1,064 curves used in the paper, time-ordered. Single column, no header, 20,001 rows, same as the raw signal column except rows 4,999–5,005 are set to 0.024875 (spike removal). |
| `time.csv` | Elapsed time (h) of each processed curve from the first one (0–16.92 h). |
| `Amplitude.csv` | Row-1 echo amplitude (mV), used as M0. |
| `Mean.csv`, `RMS.csv`, `Standard Deviation.csv`, `Skewness.csv`, `Kurtosis.csv` | Statistics of rows 1 to the signal limit of each curve (kurtosis is excess kurtosis). |
| `Shape Factor.csv`, `Crest Factor.csv`, `Impulse Factor.csv` | RMS/mean, amplitude/RMS, amplitude/mean. |
| `T2.csv` | Fitted T2 (s) from M(t) = M0·exp(−t/T2). See Known issues. |
| `pH.csv`, `Water Temperature.csv` (°C), `Turbidity.csv` (NTU), `Total Dissolved Solids.csv` | Sonde sample nearest each curve, within ±15 s. The last file is the sonde's conductivity channel (`Conductivity` in the source logs, µS). |
| `t2_curves.csv` | Empty. Use `processed_t2_data/` instead. |

**Row i of every per-curve CSV here refers to `processed_t2_data/i.csv`.** All files are single-column with no header. `T2 Raw Data from creek/scan_index.csv` maps each row back to its raw file (`processed_index` column).

## Ranges (1,064 processed curves)

| Quantity | Range |
|---|---|
| Elapsed time | 0–16.92 h, median 56 s between processed curves |
| T2 (after dropping the 12 extra rows) | 1.28–2.48 s, median 1.94 s |
| Row-1 amplitude | 0.149–0.334 mV |
| Water temperature | 14.6–17.8 °C |
| pH | 5.99–7.95 |
| Turbidity | 0–236 NTU (elevated from ~7.4 h to ~14.9 h) |
| Conductivity | 96.2–114 µS |

## Known issues

- **`T2.csv` has 1,076 rows; every other per-curve file has 1,064.** The 12 extra rows sit at 0-based positions 47, 771, 801, 818, 865, 880, 911, 931, 984, 1012, 1028, 1065. Dropping them realigns `T2.csv` with the other files (verified by refitting every processed curve). Values are wrapped in brackets, e.g. `[1.95476473]`.
- **`t2_curves.csv` is empty** (0 bytes).
- **The raw sonde log is not in the repository**, and the in-situ sensor repository has no creek log either. Only the values matched to processed curves are here.
- **`time.csv` is elapsed hours here but Unix epoch seconds in `../lab_data/time.csv`.**
