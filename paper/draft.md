# Sleeping Beauty Papers in Astrophysics: A Meta-Science Study

**Authors**: YS, Clio  
**Project**: https://github.com/yst-openclaw/astro-ph-sleeping-beauty  
**Last Updated**: 2026-02-14

---

## Abstract

We present a systematic study of "sleeping beauty" (SB) papers in astrophysics using the astro-ph knowledge graph. SB papers are defined as publications that receive few citations in their early years but become influential over time. We analyze the citation trajectories of over 400,000 astro-ph papers to identify SB candidates, investigate the reasons for their delayed recognition, and propose a taxonomy for classifying SBs by their "awakening rationale."

---

## 1. Introduction

The phenomenon of delayed recognition in science — where important papers go unnoticed for years before being appreciated — was first systematically studied by Price (1965) and later termed "sleeping beauty" by van Raan (2004). Understanding why some papers experience delayed recognition provides insight into the sociology of science, the role of technological breakthroughs in validating earlier discoveries, and the mechanisms of scientific progress.

In this study, we focus on astrophysics, a field characterized by:
- Rapid growth in the era of arXiv (1992–present)
- Strong interdependence between theory and observation
- Major paradigm shifts (e.g., dark energy, exoplanet revolution)
- Large-scale surveys and data releases

Our research questions:
1. What defines a clean sample of SB papers in astro-ph?
2. Why do some papers become SBs?
3. Can we classify SBs by their awakening rationale?

---

## 2. Data

### 2.1 Astro-ph Knowledge Graph

We use the astro-ph knowledge graph compiled by Ting et al. (2025), containing:
- **408,590 astro-ph papers** (1992–July 2025)
- **~10 concepts per paper** clustered into 9,999 concept classes
- **21.3M reference relationships** and **16.8M citation relationships**
- Publication years, titles, abstracts

### 2.2 Citation Data

For each paper, we construct a citation trajectory: $c(t)$ = citations in year $t$ since publication.

---

## 3. Methods

### 3.1 Identifying Sleeping Beauties

We implement multiple SB identification criteria:

| Method | Definition |
|--------|------------|
| **SB-10** | Peak citations occur ≥10 years after publication |
| **SB-15** | Peak citations occur ≥15 years after publication |
| **SB-ratio** | Beauty coefficient $B = C_{peak} / C_{early} > 10$ |
| **SB-absolute** | $C_{early} < 5$ but $C_{late} > 50$ |

Where:
- $C_{early}$ = citations in first 3 years
- $C_{peak}$ = maximum citations in any year
- $C_{late}$ = citations after year 3

### 3.2 Analysis Framework

For each SB candidate, we analyze:
- **Field**: Using extracted concepts
- **Topic novelty**: Concept uniqueness score
- **Cross-field connections**: Number of concept domains involved
- **Citation network position**: Predecessors/successors

### 3.3 Classification by Rationale

Proposed taxonomy:
1. **Premature discovery**: Results ahead of observational/technological capability
2. **Methodological innovation**: New analysis techniques
3. **Data release**: Papers accompanying major surveys
4. **Theoretical framework**: Foundational theory later confirmed
5. **Observational discovery**: Serendipitous findings confirmed later
6. **Negative results**: Showing something doesn't work
7. **Review/synthesis**: Consolidating works

---

## 4. Preliminary Results

*[To be populated]*

---

## 5. Discussion

*[To be populated]*

---

## 6. Conclusions

*[To be populated]*

---

## References

- Price, D. J. D. (1965). Networks of Scientific Papers. *Science*, 149(3683), 510-515.
- van Raan, A. F. J. (2004). Sleeping Beauties in Science. *Scientometrics*, 59(3), 467-472.
- Ting, Y.-S. et al. (2025). Astro-ph Knowledge Graph. *In preparation*.

---

## Appendix: Project Log

### 2026-02-14
- Project initiated
- GitHub repository created
- SB identification pipeline coded
- Pending: Full citation data (needs LFS or API access)
