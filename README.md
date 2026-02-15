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

### Part A: Identifying Sleeping Beauties

**Proposed definitions (to be tested):**
- `SB-10`: Peak citations occur ≥10 years after publication
- `SB-15`: Peak citations occur ≥15 years after publication  
- `SB-citation-ratio`: Total citations now / citations in first 3 years > X
- `SB-absolute`: Few early citations (<5) but high later citations (>50)

**Metrics to compute:**
- Citation trajectory over time for each paper
- Time to citation peak (Tp)
- "Beauty coefficient" B = Cp / Ce (peak / early citations)
- Awakening year

### Part B: Understanding Why

Using the knowledge graph concepts to analyze:
- Field/subfield of paper
- Topic novelty (concept uniqueness)
- Cross-field connections
- Methodological innovation vs. empirical discovery
- Theoretical vs. observational

### Part C: Grouping by Rationale

Proposed taxonomy:
1. **Premature discovery**: Results ahead of their time, validated later by new observations/instruments
2. **Methodological innovation**: New analysis techniques that became standard
3. **Data release**: Papers accompanying major data releases
4. **Theoretical framework**: Foundational theory papers
5. **Observational discovery**: Serendipitous findings confirmed later
6. **Negative results**: Papers showing something doesn't work
7. **Review/synthesis**: Consolidating works that became references

## Data Sources

1. **Primary**: Astro-ph Knowledge Graph (Yuan-Sen Ting)
   - Citation network
   - Paper metadata (year, title, abstract)
   - Extracted concepts
   
2. **Alternative**: 
   - Semantic Scholar API
   - NASA ADS API
   - arXiv + InspireHEP crosslinks

## Current Status

- [x] Project repository created
- [x] Knowledge graph data loaded
- [x] SB identification criteria defined and applied
- [x] **57,692 true SB candidates identified** (SB-10 criterion: peak ≥10 years after publication)
- [ ] Year-by-year citation data (need ADS API)
- [ ] Manual classification of examples
- [ ] Awakening year analysis
- [ ] Visualizations
- [ ] Paper draft

## Team

- **YST (YS)** — Principal Investigator
- **Clio** — AI Research Assistant

## License

MIT
