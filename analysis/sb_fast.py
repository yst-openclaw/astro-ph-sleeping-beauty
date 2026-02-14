"""
Sleeping Beauty Analysis - Optimized for Speed
"""

import pandas as pd
import numpy as np
import json
import gzip
from pathlib import Path
from collections import defaultdict

# Paths
KG_PATH = Path("/root/.openclaw/workspace/astro-ph-kg-full")
PROJECT_PATH = Path("/root/.openclaw/workspace/astro-ph-sleeping-beauty")

print("=" * 70)
print("SLEEPING BEAUTY ANALYSIS - OPTIMIZED")
print("=" * 70)

# Load years
print("\n[1] Loading years...")
years = np.load(KG_PATH / "papers_years.npy")
print(f"    {len(years)} papers, years {years.min()}-{years.max()}")

# Load citations in streaming mode
print("\n[2] Processing citations (streaming)...")

# Accumulate statistics
paper_stats = {}  # paper_idx -> {total_citations, num_refs, year}

count = 0
with gzip.open(KG_PATH / "citations_indexed.jsonl.gz", 'rt') as f:
    for line in f:
        item = json.loads(line)
        paper_idx = item['paper_idx']
        
        if paper_idx >= len(years):
            continue
            
        pub_year = years[paper_idx]
        num_citations = len(item.get('citations', []))
        num_refs = item.get('num_references', 0)
        
        paper_stats[paper_idx] = {
            'year': pub_year,
            'total_citations': num_citations,
            'num_references': num_refs
        }
        
        count += 1
        if count % 50000 == 0:
            print(f"    Processed {count} papers...")

print(f"    Total: {len(paper_stats)} papers with citation data")

# Convert to DataFrame
print("\n[3] Computing SB metrics...")
records = []
for paper_idx, stats in paper_stats.items():
    pub_year = stats['year']
    num_citations = stats['total_citations']
    paper_age = 2025 - pub_year
    
    if paper_age >= 5:  # At least 5 years old
        cpy = num_citations / (paper_age + 1)
        early = min(3, paper_age) * cpy
        late = (paper_age - min(3, paper_age)) * cpy
        
        if early > 0:
            beauty = late / early
        else:
            beauty = float('inf') if late > 0 else 0
            
        records.append({
            'paper_idx': paper_idx,
            'year': pub_year,
            'age': paper_age,
            'citations': num_citations,
            'refs': stats['num_references'],
            'cpy': cpy,
            'early_est': early,
            'late_est': late,
            'beauty_ratio': beauty
        })

df = pd.DataFrame(records)
print(f"    Analyzed {len(df)} papers (5+ years old)")

# SB Criteria
print("\n[4] Identifying SBs...")

# Various thresholds
sb_10 = df[(df['age'] >= 10) & (df['citations'] >= 10)]
sb_15 = df[(df['age'] >= 15) & (df['citations'] >= 20)]
sb_ratio = df[(df['age'] >= 10) & (df['beauty_ratio'] > 3) & (df['citations'] >= 20)]
sb_abs = df[(df['age'] >= 10) & (df['early_est'] < 10) & (df['late_est'] > 30)]

print(f"    SB-10 (10+yr, 10+cit): {len(sb_10)}")
print(f"    SB-15 (15+yr, 20+cit): {len(sb_15)}")
print(f"    SB-ratio (ratio>3x): {len(sb_ratio)}")
print(f"    SB-absolute: {len(sb_abs)}")

# Save
print("\n[5] Saving...")
df.to_csv(PROJECT_PATH / "data" / "all_papers_citations.csv", index=False)
sb_ratio.head(200).to_csv(PROJECT_PATH / "data" / "top_sb_candidates.csv", index=False)

# Show top
print("\n[6] TOP 30 SB CANDIDATES:")
print("-" * 70)
top = sb_ratio.head(30)
for _, row in top.iterrows():
    print(f"  arXiv:{row['paper_idx']:06d} ({int(row['year'])}): "
          f"age={int(row['age'])}y, cit={int(row['citations'])}, "
          f"beauty={row['beauty_ratio']:.1f}x")

print("\n[7] DONE!")
