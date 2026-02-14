"""
Sleeping Beauty Analysis Pipeline v2
Using full astro-ph knowledge graph data
"""

import pandas as pd
import numpy as np
import json
import gzip
from pathlib import Path
from collections import defaultdict
from datetime import datetime

# Paths
KG_PATH = Path("/root/.openclaw/workspace/astro-ph-kg-full")
PROJECT_PATH = Path("/root/.openclaw/workspace/astro-ph-sleeping-beauty")

print("=" * 60)
print("Sleeping Beauty Analysis - Loading Data")
print("=" * 60)

# Load paper years
print("\n[1] Loading paper years...")
years = np.load(KG_PATH / "papers_years.npy")
print(f"    Papers with years: {len(years)}")
print(f"    Year range: {years.min()} - {years.max()}")

# Load paper index mapping
print("\n[2] Loading paper index mapping...")
papers_idx = pd.read_csv(KG_PATH / "papers_index_mapping.csv.gz")
print(f"    Total papers: {len(papers_idx)}")

# Create paper lookup
paper_info = {}
for _, row in papers_idx.iterrows():
    paper_info[row['paper_idx']] = {
        'arxiv_id': row['arxiv_id'],
        'year': years[row['paper_idx']]
    }

# Load citations - this is the key data
print("\n[3] Loading citation network...")
citations_by_paper = {}
paper_citation_counts_by_year = defaultdict(lambda: defaultdict(int))

# We need to parse the citation data to get year-by-year citations
# The citations are given as lists of paper_idx that cite this paper
# We don't have year info for each citation directly, so we'll estimate

# Let's load a sample first to understand structure
print("    Loading citation data (this may take a few minutes)...")
citation_data = []
with gzip.open(KG_PATH / "citations_indexed.jsonl.gz", 'rt') as f:
    for i, line in enumerate(f):
        if i >= 10000:  # Start with first 10k for pilot
            break
        citation_data.append(json.loads(line))

print(f"    Loaded {len(citation_data)} papers for pilot analysis")

# For now, let's compute a simpler metric: total citations and estimate "delayed recognition"
# using the ratio of citations received vs papers published in that year

print("\n[4] Computing citation statistics...")

# Get citation counts
total_citations = []
for item in citation_data:
    paper_idx = item['paper_idx']
    num_citations = len(item.get('citations', []))
    year = years[paper_idx] if paper_idx < len(years) else 2000
    total_citations.append({
        'paper_idx': paper_idx,
        'arxiv_id': paper_info.get(paper_idx, {}).get('arxiv_id', f'idx_{paper_idx}'),
        'year': year,
        'total_citations': num_citations,
        'num_references': item.get('num_references', 0)
    })

df = pd.DataFrame(total_citations)
print(f"    Papers analyzed: {len(df)}")

# Compute metrics
current_year = 2025
df['paper_age'] = current_year - df['year']
df['citations_per_year'] = df['total_citations'] / (df['paper_age'] + 1)

print("\n[5] Identifying potential Sleeping Beauties...")

# Method 1: Old papers with relatively few citations but significant age
# These are candidates for delayed recognition

# Papers published 15+ years ago
old_papers = df[df['paper_age'] >= 15].copy()
print(f"    Papers >=15 years old: {len(old_papers)}")

# Among old papers, find those with moderate citations (not famous, not ignored)
# But potential "sleeping beauties" - they have some citations but not super famous
# Criteria: 20-200 citations, 15+ years old
sb_candidates = old_papers[
    (old_papers['total_citations'] >= 20) & 
    (old_papers['total_citations'] <= 200)
].sort_values('total_citations', ascending=False)

print(f"    SB candidates (15+ years, 20-200 citations): {len(sb_candidates)}")

# Let's look at some specific examples
print("\n[6] Sample SB candidates (old papers with moderate citations):")
print("-" * 80)
for i, row in sb_candidates.head(20).iterrows():
    print(f"  {row['arxiv_id']} ({row['year']}): {row['total_citations']} citations, {row['paper_age']} years old")

# Save results
sb_candidates.to_csv(PROJECT_PATH / "data" / "sb_candidates_pilot.csv", index=False)
print(f"\nSaved {len(sb_candidates)} candidates to data/sb_candidates_pilot.csv")
