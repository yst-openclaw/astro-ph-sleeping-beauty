# Astro-ph Sleeping Beauty Study

A meta-science investigation of "sleeping beauty" papers in astrophysics — papers that received few citations initially but became influential over time.

## What is a Sleeping Beauty Paper?

A sleeping beauty (SB) is a paper whose importance is not recognized until years or decades after publication. In bibliometrics, this is measured by:
- **Initial obscurity**: Low citation count in early years
- **Delayed recognition**: Citation peak occurs years later
- **Beauty coefficient**: Ratio of delayed to early citations

## Research Questions

1. **Identification**: What defines a clean sample of SB papers in astro-ph?
2. **Causation**: Why do some papers become SBs? 
3. **Classification**: Can we group SBs by their "awakening" rationale?

## Methodology

### Naive Approach (Initial)

Simple citation ratio thresholds gave inflated results (~1% of papers), which is unrealistically high compared to literature estimates (~0.01%).

### Refined Approach: Piecewise Slope Fitting

We fit linear slopes to early (0-4 years) vs late (8+ years) citation trajectories:

**Criteria for true SB:**
- Early citations (years 0-4): < 5 total
- Late citations > 3× early citations  
- Late slope > 5× early slope

This identifies papers with **flat early curves** that transition to **steep late growth** — the hallmark of true sleeping beauties.

## Results

- **Dataset**: ~400,000 astro-ph papers
- **True SB candidates**: 24 papers (0.006%)
- **Max slope ratio**: 34× (2008arXiv0802.0716H)
- **Expected rate**: ~0.01% (literature benchmark) ✓

**Key Finding**: Simple citation ratio methods overestimate SB prevalence by ~100×. Slope fitting is essential for clean identification.

## Outputs

| File | Description |
|------|-------------|
| `sb_final.json` | 24 true SB candidates with citation curves |
| `sb_curves.json` | Full citation trajectory data |
| `paper/draft.md` | Manuscript draft |
| `index.html` | Interactive visualization (GitHub Pages) |

**Live Dashboard**: https://yst-openclaw.github.io/astro-ph-sleeping-beauty/

## Next Steps

1. [ ] Obtain ADS data for more complete citation records
2. [ ] Manual classification by awakening reason
3. [ ] Compare with known famous SBs in literature
4. [ ] Analyze correlation with paper characteristics (field, novelty, etc.)

## Data Limitations

- arXiv citation data may miss citations from non-arXiv sources
- ADS API would provide more complete coverage
- Early career papers (2015+) may not have had time to "awaken"

## Team

- **YST (YS)** — Principal Investigator
- **Clio** — AI Research Assistant

## License

MIT
