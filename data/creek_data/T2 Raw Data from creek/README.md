# T2 raw data from creek (SPIE4–SPIE7)

non-AI note All the data in fodlers are from the same test day (13th Mar, 2025). However, each folder is time-delayed by a minute or so. Original files didn't have proper column names. That's why the "column_name_adder.py" program is there. 


Raw CPMG T2 decay curves from the Rocky Branch Creek deployment (downtown Columbia, SC). One continuous run of about 17.6 h starting 13 March 2025, split across four folders, 2,788 curves in total.

## One CSV = one complete T2 decay

**Each file holds one echo-peak train, one row per spin echo.** Echo spacing is 0.75 ms.

| Item | Value |
|---|---|
| Columns | `NMR signal (mV)`, `time (s)` (headers added after acquisition by `column_name_adder.py`; units as assigned there) |
| Rows | 20,001 per file |
| `time (s)` | 0 to 7.5 s in 0.75 ms steps (rows 0–10,000), then zero padding |
| `NMR signal (mV)` | nonzero to about 6.35 s (row ~8,470), then zero padding |
| Usable decay | rows 1 to ~5,001 (0–3.75 s) |
| Typical values | row-1 amplitude ~0.25 mV, fitted T2 ~1.9 s, noise floor ~0.034 mV |

**The echo signal ends at 3.75 s.** At rows 5,002–5,003 (3.7515 s) a ~1.3 mV two-sample spike appears in 96% of curves and the median signal steps from 0.045 mV straight down to a flat ~0.035 mV noise floor. Treat rows after ~5,003 as noise only. A second spike near 6.24 s (rows ~8,315–8,340) appears in 83% of curves.

**Paper processing** (`spie_paper_code.py`): drop row 0, take row 1 as M0, fit M(t) = M0·exp(−t/T2) up to a per-curve signal limit (noise level estimated from rows 7,000–7,500, capped at 5.8 s), and overwrite rows 4,999–5,005 with 0.024875 to remove the 3.75 s spike.

## File names

`<Larmor frequency in Hz, 8 digits><scan counter>.csv`

Example: `27672000251.csv` is 27.672000 MHz, scan 251.

**The scan counter is the acquisition order within a folder**, running 1…N with no gaps. Sort by the counter, never by file name, since the frequency prefix scrambles lexical order.

**The frequency prefix is the Larmor setpoint for that curve.** Before every block of 10 curves the LabVIEW code runs a Larmor-optimization step (measures at the current setpoint and ±5 kHz, keeps the strongest echo). The setpoint therefore moves in 5 kHz steps and changes only at scans 11, 21, 31, … It spans 27.667–27.712 MHz over the run.

## Timing between curves

| Interval | Value |
|---|---|
| Consecutive curves inside a 10-curve block | 19 s (18–20 s; source timestamps have 2 s resolution) |
| Across a block boundary (after every 10th curve) | 58–60 s, i.e. ~40 s of Larmor re-tuning |
| Average | 22.7 s per curve, ~158 curves/h |

## What separates the folders

**Same site, same day, same continuous run. Each folder is one acquisition session.** When the echoes were lost, the operator stopped the LabVIEW program, re-found the Larmor frequency, and restarted it into a new folder (procedure in `flow_through_nmr_doc.docx`). Each restart resets the scan counter to 1 and starts on a new frequency.

| Folder | Curves | Elapsed time (h) | Duration | Larmor range (MHz) | Start → end setpoint | In processed set |
|---|---|---|---|---|---|---|
| SPIE4 | 78 | 0.00–0.48 | 29 min | 27.695–27.700 | 27.700 → 27.695 | 33 |
| SPIE5 | 320 | 0.52–2.52 | 2.0 h | 27.687–27.702 | 27.692 → 27.687 | 120 |
| SPIE6 | 2,121 | 2.58–15.92 | 13.3 h | 27.667–27.697 | 27.677 → 27.677 | 854 |
| SPIE7 | 269 | 15.95–17.64 | 1.7 h | 27.697–27.712 | 27.707 → 27.712 | 57 |

Gaps between sessions: 2.6 min (SPIE4→5), 3.9 min (SPIE5→6), 2.1 min (SPIE6→7).

Elapsed time zero is the first curve in the processed set (SPIE4 scan 2), the same origin as `../time.csv`. SPIE4 scan 1 sits at −0.005 h.

## scan_index.csv

**One row per raw file, with its time and its link to the processed data.** Built by `build_scan_index.py` (run it from this folder).

| Column | Meaning |
|---|---|
| `folder`, `file`, `scan` | source folder, file name, scan counter |
| `larmor_hz` | Larmor setpoint from the file name |
| `tune_block` | 10-curve block number (one Larmor optimization per block) |
| `elapsed_h` | hours from the first processed curve |
| `elapsed_source` | `time.csv` (exact, 1,064 curves) or `estimated` (1,724 curves) |
| `processed_index` | row in `../processed_t2_data/` and every per-curve CSV in `../`; blank if not used |
| `amp_row1` | row-1 echo amplitude (mV) |
| `T2_fit_s` | T2 refit with the paper's rules (matches `../T2.csv` for processed curves) |

**How the times were recovered.** Git does not keep file modification times, which were the only timestamps. Every curve in `../processed_t2_data/` matches exactly one raw file, which carries its `../time.csv` value over. The remaining curves are placed with the measured cadence (19 s per curve plus ~40 s per block), interpolated between matched neighbours. Leave-one-out error is ≤2 s for SPIE5–SPIE7 and ≤10 s for SPIE4. SPIE7 scans 156–269 lie past the last matched curve and are extrapolated, so treat their times as ±1 min.

## Quality notes

- **174 curves (6%) carry no echo** (row-1 amplitude < 0.1 mV). They recur at 2.8 min spacing, usually in sets of three, consistent with the timed sample pump refreshing the cell during an acquisition. Pump timing was not logged. The paper's amplitude window (0.1–0.4 mV) removes them.
- **Noise floor rises from ~0.034 to ~0.045 mV at about 13.9 h** (SPIE6 scan ~1,800) and stays there through SPIE7. Row-1 amplitude also rises from ~0.25 to ~0.31 mV between 14.7 and 15.6 h.
- **SPIE7 scans 156–269 look normal but are not in the processed set.** The paper keeps only curves with a water-quality sonde sample within ±15 s, so the sonde record most likely ends at ~16.9 h.
- **2,508 of 2,788 curves pass the paper's T2 (1.25–4 s) and amplitude windows; 1,064 made the processed set.** Most of the reduction comes from the ±15 s sonde-matching step.

## Clock time

Absolute clock time is not in the repository. The original files on the acquisition PC (folder `spie_data/creek_2/` in `spie_paper_code.py`) still carry it. Inferred from the sonde data: water temperature peaks at ~4.4 h and bottoms out at ~16.8 h, consistent with a late-morning start running overnight.

## Other files here

- `column_name_adder.py`: one-time script that added the two column headers. Already applied to every file.
- `FFT.py`: quick FFT viewer for a single file.

## Acquisition setup (from the paper and `flow_through_nmr_doc.docx`)

Permanent-magnet NMR with a flow-through coil, electronics in a temperature-controlled enclosure (IncuFridge) under a tent at the creek. NI PXI-5421 generates the pulse sequence, NI PXI-5124 digitizes, NI PXIe-8821 runs LabVIEW. Pumps on a fixed Arduino on/off timer draw creek water through the coil. Each iteration of the main VI is one Larmor optimization followed by 10 saved T2 curves. The number of acquisitions averaged per curve was not recorded.



