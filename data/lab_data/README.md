# Lab data

Bench tests of the flow-through NMR with Cu(II) (copper sulfate) in distilled water. Four sessions between 25 February and 10 March 2025, 3,910 T2 curves. Only per-curve features are stored here; the raw lab T2 curves are not in the repository.

## Sessions

| # | Local time (America/New_York) | Curves | Cu(II) concentration (mg/L) | Role in paper |
|---|---|---|---|---|
| 1 | 2025-02-25 19:47 → 02-26 07:56 | 1,158 | 5, 10, 12.5 (static) | training |
| 2 | 2025-02-28 18:12 → 03-01 10:45 | 2,004 | 25, 50, 75, 100 (static) | training |
| 3 | 2025-03-04 18:44 → 22:58 | 466 | 200, 400, 800, 1000 (static) | training |
| 4 | 2025-03-10 21:11 → 23:30 | 282 | continuous fill, 0 → ~25 | test |

Session 4 is the continuous-flow test: 0.925 L of 77.3 mg/L Cu(II) pumped into 2.86 L of distilled water while the same volume was drawn off, reaching ~25 mg/L. Curves are 18 s apart (median) within a session.

## Contents

| File | What it holds |
|---|---|
| `time.csv` | Unix epoch seconds (UTC) of each curve, from the raw file modification time |
| `concentration.csv` | Cu(II) concentration label (mg/L) |
| `T2.csv` | Fitted T2 (s), 0.079–2.31 s |
| `Amplitude.csv` | Row-1 echo amplitude (mV), used as M0 |
| `Mean.csv`, `RMS.csv`, `Standard Deviation.csv`, `Skewness.csv`, `Kurtosis.csv` | Statistics of rows 1 to the signal limit of each curve |
| `Shape Factor.csv`, `Crest Factor.csv`, `Impulse Factor.csv` | RMS/mean, amplitude/RMS, amplitude/mean |
| `pH.csv`, `Water Temperature.csv` (°C), `Turbidity.csv` (NTU), `Total Dissolved Solids.csv` | Sensor sample nearest each curve, within ±15 s. The last file is the conductivity channel (`Conductivity (µS)` in the source logs), 0–1,470 µS. |

All files are single-column, no header, 3,910 rows, row-aligned.

## Known issues

- **Session 4 concentration labels are out of time order.** The fill should rise from 0 to ~25 mg/L, and conductivity (0 → 35 µS) and T2 (1.77 → 1.30 s) both track that rise. The labels instead start at 25 mg/L and fall (rank correlation with time ≈ −0.74). `spie_paper_code.py` assigns the ramp value by directory-listing order before sorting curves by time, and the frequency-prefixed file names do not list in acquisition order. Re-deriving the labels needs the raw session-4 files (folder `SPIE3` in the code), which are not in this repository.
- **`time.csv` is epoch seconds here but elapsed hours in `../creek_data/time.csv`.**
