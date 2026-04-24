# Kode — K-Space Decode

> What if k-space itself is the answer — and image reconstruction is just one of many things you can do with it?

Kode is a Python toolkit for exploring raw MRI k-space data beyond standard image reconstruction. Instead of treating k-space as a stepping stone to a DICOM image, Kode treats it as a rich signal in its own right — one that contains diagnostic, structural, and motion information before a single pixel is rendered.

Built on the [fastMRI dataset](https://fastmri.med.nyu.edu/) from Meta AI / NYU Langone.

---

## Brain K-Space Fingerprint Atlas — 186 Scans, 5 Sequence Types

> Can k-space tell the difference between scan types — without ever reconstructing an image?

Computed k-space fingerprints (radial power profile, energy ratio, asymmetry score) across 186 real multicoil brain MRI scans spanning 5 clinical sequences: FLAIR, T1, T1POST, T1PRE, T2. Each dot below is one patient's brain.

**Mean fingerprint curve per sequence — distinct signatures emerge from raw frequency data alone**

![Brain Fingerprint Atlas](results/brain_fingerprint_atlas.png)

**Scatter plot — 186 patients mapped by energy ratio vs asymmetry score**

![Brain Fingerprint Scatter](results/brain_fingerprint_scatter.png)

Each sequence type clusters separately in k-space — without image reconstruction, without AI, without labels. This is the foundation of a **k-space diagnostic atlas**: a screening system that works upstream of the image, on the raw signal the scanner actually measures.

---

## The Gap This Addresses

Current diagnostic pipelines — both radiologists and AI models — work on reconstructed images. But reconstruction is lossy: phase information is discarded, coil sensitivity data is collapsed, and frequency-domain structure disappears into pixel values.

```
MRI Scanner
    → K-Space (raw frequency data)     ← Kode works here
        → IFFT → Reconstructed Image   ← radiologists and AI work here
```

Kode works upstream. The hypothesis: **some pathologies are more detectable in k-space than in the reconstructed image** — faster, with no training data, before any reconstruction choices are made.

---

## All Notebooks

| Notebook | What it shows |
|---|---|
| `05_brain_fingerprint_atlas` | K-space fingerprints across 186 brain scans — sequence clustering and outlier detection |
| `01_selective_reconstruct` | Tissue separation by frequency band — no segmentation algorithm |
| `02_fingerprint` | Radial power profile and asymmetry metrics on knee k-space |
| `03_progressive_reveal` | Knee MRI assembling from DC component to full resolution |
| `04_pseudo4d` | Motion phase recovery from k-space time structure |

---

**Progressive Reveal — knee MRI building from frequency data**

![Progressive Reveal](results/progressive_reveal.gif)

**Selective Frequency Reconstruction — isolating tissue layers without segmentation**

![Selective Reconstruct](results/selective_reconstruct.png)

**Pseudo-4D Motion Phases — motion states recovered from a static scan**

![Pseudo-4D Phases](results/pseudo4d_phases.png)

---

## Setup

```bash
git clone https://github.com/nadiapriyam/kode.git
cd kode
pip install -r requirements.txt
```

Data: request access at [fastmri.med.nyu.edu](https://fastmri.med.nyu.edu/). Place `.h5` files in `data/`.

---

## Project Structure

```
kode/
├── kode/
│   ├── io.py
│   ├── selective_reconstruct.py
│   ├── fingerprint.py
│   ├── progressive_reveal.py
│   └── pseudo4d.py
├── notebooks/
│   ├── 05_brain_fingerprint_atlas.ipynb
│   ├── 01_selective_reconstruct.ipynb
│   ├── 02_fingerprint.ipynb
│   ├── 03_progressive_reveal.ipynb
│   └── 04_pseudo4d.ipynb
├── data/
└── results/
```

---

## Status

Active development. Built as part of the Meridian medical imaging platform research.
