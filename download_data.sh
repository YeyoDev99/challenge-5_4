#!/bin/bash
cd /workspaces/challenge-5_4/data

echo "Downloading CCD data files..."

wget -q "https://nces.ed.gov/ccd/data/zip/ccd_sch_029_2223_w_1a_083023.zip" -O tmp.zip && unzip -o tmp.zip && rm tmp.zip && echo "✓ Directory"

wget -q "https://nces.ed.gov/ccd/data/zip/ccd_sch_033_2223_l_1a_083023.zip" -O tmp.zip && unzip -o tmp.zip && rm tmp.zip && echo "✓ Lunch"

wget -q "https://nces.ed.gov/ccd/data/zip/ccd_sch_059_2223_l_1a_083023.zip" -O tmp.zip && unzip -o tmp.zip && rm tmp.zip && echo "✓ Staff"

wget -q "https://nces.ed.gov/ccd/data/zip/ccd_sch_129_2223_w_1a_083023.zip" -O tmp.zip && unzip -o tmp.zip && rm tmp.zip && echo "✓ Characteristics"

wget -q "https://nces.ed.gov/ccd/data/zip/ccd_sch_052_2223_l_1a_083023.zip" -O tmp.zip && unzip -o tmp.zip && rm tmp.zip && echo "✓ Membership"

echo "Done. All files ready."
