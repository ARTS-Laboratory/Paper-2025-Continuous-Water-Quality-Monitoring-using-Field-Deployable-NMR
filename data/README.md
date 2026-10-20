# Data

Every T2 curve comes from the same flow-through NMR system; each curve is one CPMG echo-peak train at 0.75 ms echo spacing.

## Creek data

`creek_data/` — field deployment at Rocky Branch Creek, downtown Columbia, SC, one continuous ~17.6 h run starting 13 March 2025.

- **Raw:** 2,788 T2 curves in four back-to-back acquisition sessions (`T2 Raw Data from creek/SPIE4`–`SPIE7`), one curve every ~19 s with a ~40 s Larmor re-tune after every 10th curve. `scan_index.csv` gives every raw file its elapsed time.
- **Processed:** the 1,064 curves used in the paper (`processed_t2_data/`), their elapsed time, nine time-domain features, fitted T2, and the matched water-quality sensor values (pH, temperature, turbidity, conductivity).

## Lab data

`lab_data/` — bench tests with Cu(II) (copper sulfate) in distilled water, four sessions from 25 February to 10 March 2025, 3,910 curves.

- **Static:** 5–1,000 mg/L standards over three sessions (training data in the paper).
- **Continuous flow:** a 0 → ~25 mg/L fill on 10 March (test data in the paper).
- Features, fitted T2, concentration labels, and matched sensor values only; raw lab curves are not in the repository.

## Shared conventions

- All feature and sensor files are single-column CSVs with no header; row i is the same curve across every file in a folder.
- Feature definitions are identical in both folders (see `spie_paper_code.py`).
- `time.csv` differs: elapsed hours in `creek_data/`, Unix epoch seconds in `lab_data/`.

## Known issues

- `creek_data/T2.csv` has 12 extra rows and is misaligned after row 47 (details in `creek_data/README.md`).
- `creek_data/t2_curves.csv` is empty.
- `lab_data/concentration.csv` labels for the 10 March continuous-flow session are out of time order (details in `lab_data/README.md`).
