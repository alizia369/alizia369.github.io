# RyeChron project website

Public project page: https://alizia369.github.io/ryechron/

A self-contained, responsive static project page for an industry audience. It introduces the study, presents cohort-limited results, and outlines proposed partnership opportunities. Its photographs are original crops from Figure 2 of the user-supplied RyeChron manuscript. The hyperspectral illustration is an original crop from Figure 3.

## Contents

- index.html: page, responsive styles and visit selector.
- assets/plant-r*.png and plant-s*.png: representative observations at scheduled visits 1, 10 and 23.
- assets/hyperspectral.png: source method illustration.
- assets/ryechron-qr.png: 820 × 820 QR code with a four-module quiet zone.
- assets/ryechron-qr.svg: scalable QR code.

The QR code encodes https://alizia369.github.io/ryechron/ with error correction Q. Its matrix was independently decoded with jsQR before publication. It is static and does not use a tracking or redirect service.

## Evidence and content

Source: RyeChron: Learning Longitudinal Multimodal Spectral Representations for Early Herbicide Resistance Prediction, supplied as Herbicide_CVPR2027 (8).pdf.

- Table 2: 54 physical pots, 36 treated, 18 controls and 23 scheduled visits.
- Table 3: mean balanced accuracy of 95.2% for CCRA and 89.5% for the early-fusion GRU, and 98.4% AUROC for CCRA. These are means over three outer folds and 23 scheduled times.
- Abstract and limitations: one source population per class; independent-population generalisation and pre-symptom detection remain to be established.
- Section 3: planned release of dataset, masks, metadata and evaluation splits upon acceptance.

No publication acceptance, external partner involvement, product recommendation capability, commercial savings or field deployment is claimed. Partnership roles are proposed development opportunities. No confidential manuscript PDF is distributed by this page.

## Editing

Edit index.html and commit to the website repository's main branch. GitHub Pages serves the folder directly; no build or external JavaScript dependencies are needed. Keep filenames stable when updating images. If the project URL changes, regenerate both QR assets before printing slides.
