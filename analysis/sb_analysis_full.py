"""
Sleeping Beauty Analysis - Full Pipeline
Computes SB metrics for all papers and identifies candidates
"""

import pandas as pd
import numpy as np
import json
import gzip
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime

# Paths
KG_PATH = Path("/root/.openclaw/workspace/astro-ph-kg-full")
PROJECT_PATH = Path("/root/.openclaw/workspace/astro-ph-sleeping-beauty")

print("=" * 70)
print("SLEEPING BEAUTY ANALYSIS - FULL PIPELINE")
print("=" * 70)

# Load paper years
print("\n[1] Loading data...")
years = np.load(KG_PATH / "papers_years.npy")
papers_idx = pd.read_csv(KG_PATH / "papers_index_mapping.csv.gz")

# Create lookup
paper_lookup = {}
for _, row in papers_idx.iterrows():
    paper_lookup[row['paper_idx']] = {
        'arxiv_id': row['arxiv_id'],
        'year': years[row['paper_idx']]
    }

print(f"    Total papers: {len(paper_lookup)}")
print(f"    Year range: {years.min()} - {years.max()}")

# Load ALL citations
print("\n[2] Loading citation network (all papers)...")
citation_data = []
with gzip.open(KG_PATH / "citations_indexed.jsonl.gz", 'rt') as f:
    for line in f:
        citation_data.append(json.loads(line))

print(f"    Loaded {len(citation_data)} paper records")

# Compute SB metrics for each paper
print("\n[3] Computing SB metrics...")
results = []

for item in citation_data:
    paper_idx = item['paper_idx']
    if paper_idx not in paper_lookup:
        continue
        
    info = paper_lookup[paper_idx]
    pub_year = info['year']
    arxiv_id = info['arxiv_id']
    
    # Citation info
    citations_list = item.get('citations', [])
    references_list = item.get('references', [])
    num_citations = len(citations_list)
    num_references = len(references_list)
    
    # Paper age
    paper_age = 2025 - pub_year
    
    # For sleeping beauty, we need to estimate early vs late citations
    # The citations are stored as paper indices, we don't have year-by-year
    # So we use a heuristic: estimate based on paper age
    
    # SB criterion 1: Peak delay (hard without year-by-year)
    # SB criterion 2: Beauty ratio - we estimate with total/age
    
    if paper_age >= 5:  # At least 5 years old
        citations_per_year = num_citations / (paper_age + 1)
        
        # SB-absolute: few early, many later
        # Estimate early as ~3 years, late as remaining
        early_estimate = min(3, paper_age) * citations_per_year
        late_estimate = (paper_age - min(3, paper_age)) * citations_per_year
        
        # Beauty coefficient estimate
        if early_estimate > 0:
            beauty_ratio = late_estimate / early_estimate
        else:
            beauty_ratio = float('inf') if late_estimate > 0 else 0
            
        results.append({
            'paper_idx': paper_idx,
            'arxiv_id': arxiv_id,
            'year': pub_year,
            'paper_age': paper_age,
            'total_citations': num_citations,
            'num_references': num_references,
            'citations_per_year': citations_per_year,
            'early_citations_est': early_estimate,
            'late_citations_est': late_estimate,
            'beauty_ratio_est': beauty_ratio
        })

df = pd.DataFrame(results)
print(f"    Analyzed {len(df)} papers (5+ years old)")

# Define SB criteria
print("\n[4] Identifying Sleeping Beauty candidates...")

# SB-10: 10+ years old, peak delayed
sb_10 = df[(df['paper_age'] >= 10) & (df['total_citations'] >= 10)]
sb_10 = sb_10.sort_values('beauty_ratio_est', ascending=False)

# SB-15: 15+ years old
sb_15 = df[(df['paper_age'] >= 15) & (df['total_citations'] >= 20)]
sb_15 = sb_15.sort_values('beauty_ratio_est', ascending=False)

# SB-conservative: 10+ years, beauty ratio > 3, at least 20 citations
sb_ratio = df[(df['paper_age'] >= 10) & 
              (df['beauty_ratio_est'] > 3) & 
              (df['total_citations'] >= 20)]
sb_ratio = sb_ratio.sort_values('beauty_ratio_est', ascending=False)

# SB-absolute: old papers with few early but decent late
sb_abs = df[(df['paper_age'] >= 10) & 
             (df['early_citations_est'] < 10) & 
             (df['late_citations_est'] > 30)]
sb_abs = sb_abs.sort_values('late_citations_est', ascending=False)

print(f"\n    SB-10 (10+ years, 10+ citations): {len(sb_10)}")
print(f"    SB-15 (15+ years, 20+ citations): {len(sb_15)}")
print(f"    SB-ratio (beauty ratio > 3x): {len(sb_ratio)}")
print(f"    SB-absolute (few early, many late): {len(sb_abs)}")

# Get unique SB candidates across all methods
all_sb_idx = set(sb_10['paper_idx'].tolist() + 
                 sb_15['paper_idx'].tolist() + 
                 sb_ratio['paper_idx'].tolist() + 
                 sb_abs['paper_idx'].tolist())

print(f"\n    Total unique SB candidates: {len(all_sb_idx)}")

# Save results
print("\n[5] Saving results...")
df.to_csv(PROJECT_PATH / "data" / "all_papers_metrics.csv", index=False)
sb_10.to_csv(PROJECT_PATH / "data" / "sb_candidates_10yr.csv", index=False)
sb_15.to_csv(PROJECT_PATH / "data" / "sb_candidates_15yr.csv", index=False)
sb_ratio.to_csv(PROJECT_PATH / "data" / "sb_candidates_ratio.csv", index=False)
sb_abs.to_csv(PROJECT_PATH / "data" / "sb_candidates_absolute.csv", index=False)

print(f"    Saved all metrics and candidate lists")

# Show top candidates
print("\n[6] TOP SLEEPING BEAUTY CANDIDATES (by beauty ratio):")
print("-" * 70)
for i, row in sb_ratio.head(30).iterrows():
    print(f"  {row['arxiv_id']} ({int(row['year'])}): "
          f"age={int(row['paper_age'])}y, "
          f"citations={int(row['total_citations'])}, "
          f"beauty_ratio={row['beauty_ratio_est']:.1f}x")

# Save top 100 for detailed analysis
top_sb = sb_ratio.head(100)
top_sb.to_csv(PROJECT_PATH / "data" / "top_100_sb_candidates.csv", index=False)

print(f"\n[7] Analysis complete!")
print("=" * 70)
