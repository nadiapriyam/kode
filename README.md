# Kode — K-Space Decode

> **The physics of spatial frequency encoding does the work — not an algorithm guessing from grayscale values.**

---

## The Problem With How MRI Is Read Today

Every radiologist and every AI diagnostic model works on the same thing: a reconstructed grayscale image. But that image is a mathematical derivative — it's what you get *after* the raw signal has been processed, compressed, and transformed. By the time a pixel exists, information has already been lost.

The raw signal is called **k-space**. It's what the scanner actually measures.

### Why K-Space Is Fundamentally Different

In image space, a pixel tells you the local intensity at one point. A tumor affects only the pixels it occupies.

In k-space, **every single point encodes a global property of the entire image**. A tumor — no matter how small — changes the frequency distribution of the entire k-space. Its cellular density, its boundary sharpness, its internal structure all leave a measurable frequency signature across the full k-space grid.

```
Image space:  tumor occupies ~1% of pixels  →  AI sees local patch
K-space:      tumor changes 100% of k-space →  signal is everywhere, always
```

This means:
- Subtle early-stage changes that are invisible in image space may be detectable in k-space
- Tumor margins — which are notoriously imprecise in image space — are encoded as specific phase and amplitude patterns in high-frequency k-space
- A classifier operating in k-space works on the raw physics, not on a derived approximation

**The bigger idea: instead of using AI to read images, use AI to read k-space directly.**

---

## Brain K-Space Fingerprint Atlas — 186 Scans, 5 Sequence Types

Can k-space tell the difference between scan types — without ever reconstructing an image?

Kode computes k-space fingerprints (radial power profile, energy ratio, asymmetry score) across 186 real multicoil brain MRI scans spanning 5 clinical sequences: FLAIR, T1, T1POST (contrast-enhanced), T1PRE, T2.

**Mean fingerprint curve per sequence — distinct signatures from raw frequency data alone**

![Brain Fingerprint Atlas](results/brain_fingerprint_atlas.png)

FLAIR's fluid suppression is visible as a measurably lower power curve — detectable before any image is constructed. The physics of the acquisition show up directly in k-space shape.

**T1PRE vs T1POST — the k-space signature of gadolinium enhancement**

![T1 Contrast Comparison](results/t1_contrast_comparison.png)

T1POST (post-contrast) shows systematically different high-frequency content than T1PRE (pre-contrast). The difference between these curves is the k-space signature of blood-brain barrier breakdown — the mechanism by which tumors appear on contrast MRI. No image required to see it.

**186 patients mapped by energy ratio vs asymmetry score**

![Brain Fingerprint Scatter](results/brain_fingerprint_scatter.png)

Outliers — patients whose k-space deviates from their sequence-type cluster — are flagged automatically. These are the candidates for radiologist review.

---

## All Notebooks

| Notebook | What it shows |
|---|---|
| `05_brain_fingerprint_atlas` | 186-scan atlas, T1PRE/T1POST contrast comparison, outlier detection |
| `01_selective_reconstruct` | Tissue separation by frequency band — no segmentation algorithm |
| `02_fingerprint` | Radial power profile and asymmetry metrics |
| `03_progressive_reveal` | MRI assembling from DC component to full resolution |
| `04_pseudo4d` | Motion phase recovery from k-space time structure |

---

**Progressive Reveal — MRI assembling from frequency data**

![Progressive Reveal](results/progressive_reveal.gif)

**Selective Frequency Reconstruction — tissue layers without segmentation**

![Selective Reconstruct](results/selective_reconstruct.png)

**Pseudo-4D Motion Phases — motion states from a static scan**

![Pseudo-4D Phases](results/pseudo4d_phases.png)

---

## Why This Matters Clinically

Current tumor margin delineation in radiation therapy adds 1-2cm margins around visible tumor boundaries to compensate for uncertainty. That margin irradiates healthy tissue.

If tumor margins can be characterized more precisely in k-space — where boundary information is encoded in the phase and amplitude of high-frequency components — those margins shrink. Smaller margins mean less healthy tissue irradiated per treatment fraction.

The same principle applies to surgical planning, treatment response monitoring, and early detection.

---

## Setup

```bash
git clone https://github.com/nadiapriyam/kode.git
cd kode
pip install -r requirements.txt
```

Data: request access at [fastmri.med.nyu.edu](https://fastmri.med.nyu.edu/). Place `.h5` files in `data/`.

---

## Related

- [Meridian](https://github.com/nadiapriyam/meridian) — HIPAA-aware mobile annotation platform for sharing scan findings with patients.

---

## Status

Active development. Research into k-space as a primary diagnostic signal — upstream of image reconstruction.
