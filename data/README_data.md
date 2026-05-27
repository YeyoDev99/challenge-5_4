# Data Directory

## ⚠️ Files NOT included in this repository

The CCD data files are publicly available from NCES but are not committed to git
(they range from 12 MB to ~500 MB uncompressed).

## Download Instructions

1. Go to: https://nces.ed.gov/ccd/files.asp
2. Select:
   - **Fiscal/Nonfiscal:** Nonfiscal
   - **Level:** School
   - **School Year:** 2022 - 2023
3. Under "Public Elementary/Secondary School Universe Survey Data, (v.1a)"
   download and **unzip** the following 5 Data Files:

| Survey component | Download label | Expected filename after unzip |
|---|---|---|
| Directory | `DIRECTORY — Flat and SAS Files (12.0 MB)` | `ccd_sch_029_2223_w_1a_083023.csv` |
| Lunch Eligibility | `LUNCH PROGRAM ELIGIBILITY — Flat and SAS Files (14.2 MB)` | `ccd_sch_033_2223_l_1a_083023.csv` |
| Membership | `MEMBERSHIP — Flat and SAS Files (198 MB)` | `ccd_sch_052_2223_l_1a_083023.csv` |
| Staff | `STAFF — Flat and SAS Files (5.35 MB)` | `ccd_sch_059_2223_l_1a_083023.csv` |
| School Characteristics | `SCHOOL CHARACTERISTICS — Flat and SAS Files (5.09 MB)` | `ccd_sch_129_2223_w_1a_083023.csv` |

4. Place all 5 `.csv` files in this `data/` directory.
5. Run `notebooks/best_run.ipynb` — it expects exactly these filenames.

## License
NCES public-use data. Per NCES policy, data may only be used for statistical purposes.
See: https://nces.ed.gov/statprog/instruct.asp
