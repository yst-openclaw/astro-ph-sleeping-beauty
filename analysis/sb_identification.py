"""
Sleeping Beauty Identification Pipeline

This script defines and implements the identification of sleeping beauty 
papers in astrophysics (astro-ph) from arXiv.

Author: Clio (AI Assistant)
PI: YS
"""

import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime
import json

# =============================================================================
# CONFIGURATION
# =============================================================================

# Project paths
PROJECT_ROOT = Path("/root/.openclaw/workspace/astro-ph-sleeping-beauty")
DATA_DIR = PROJECT_ROOT / "data"
KG_DIR = PROJECT_ROOT.parent / "astro-ph_knowledge_graph"

# Sleeping Beauty thresholds (to be tuned)
SB_THRESHOLDS = {
    "SB-10": {"peak_delay_years": 10, "min_early_citations": 0, "min_late_citations": 10},
    "SB-15": {"peak_delay_years": 15, "min_early_citations": 0, "min_late_citations": 10},
    "SB-conservative": {"peak_delay_years": 10, "min_early_citations": 0, "min_late_citations": 50},
    "SB-ratio": {"ratio_threshold": 10, "min_early_citations": 1, "min_total_citations": 20},
}

# Year ranges for "early" and "late" periods
EARLY_YEARS = 3  # First N years for early citations
RECENT_CUTOFF = 2025  # Papers published up to this year

# =============================================================================
# DATA STRUCTURES
# =============================================================================

@dataclass
class Paper:
    """Represents an astro-ph paper with citation metadata."""
    arxiv_id: str
    year: int
    title: str
    abstract: str
    concepts: List[str]
    total_citations: int
    citations_by_year: Dict[int, int]  # year -> citation count
    
    @property
    def early_citations(self) -> int:
        """Citations in first EARLY_YEARS years."""
        return sum(self.citations_by_year.get(y, 0) 
                   for y in range(self.year, self.year + EARLY_YEARS + 1))
    
    @property
    def peak_year(self) -> Optional[int]:
        """Year with maximum citations."""
        if not self.citations_by_year:
            return None
        return max(self.citations_by_year.keys(), 
                   key=lambda y: self.citations_by_year[y])
    
    @property
    def peak_citations(self) -> Optional[int]:
        """Maximum citations in any year."""
        if not self.citations_by_year:
            return None
        return max(self.citations_by_year.values())
    
    @property
    def delay_to_peak(self) -> Optional[int]:
        """Years from publication to citation peak."""
        if self.peak_year is None:
            return None
        return self.peak_year - self.year
    
    @property
    def beauty_coefficient(self) -> Optional[float]:
        """Ratio of peak to early citations."""
        if self.early_citations == 0 or self.peak_citations is None:
            return None
        return self.peak_citations / self.early_citations


@dataclass
class SleepingBeautyCandidate:
    """A paper identified as a potential sleeping beauty."""
    paper: Paper
    method: str  # Which SB criteria it met
    score: float  # Composite score
    proposed_rationale: Optional[str] = None


# =============================================================================
# DATA LOADING
# =============================================================================

def load_knowledge_graph_data() -> Dict:
    """
    Load data from the astro-ph knowledge graph.
    Note: Requires LFS pull for full data.
    """
    data = {}
    
    # Try to load what we can
    kg_path = KG_DIR
    
    # Index files (should work even without full LFS)
    try:
        # These are small index files
        papers_idx = pd.read_csv(kg_path / "papers_index_mapping.csv.gz")
        data["papers_index"] = papers_idx
        print(f"Loaded papers_index: {len(papers_idx)} papers")
    except Exception as e:
        print(f"Warning: Could not load papers_index: {e}")
    
    try:
        years = np.load(kg_path / "papers_years.npy")
        data["years"] = years
        print(f"Loaded years: {len(years)} entries")
    except Exception as e:
        print(f"Warning: Could not load years: {e}")
    
    return data


def fetch_citations_from_ads(arxiv_ids: List[str], 
                             batch_size: int = 2000) -> Dict[str, Dict[int, int]]:
    """
    Fetch citation data from NASA ADS API.
    
    This is a placeholder - actual implementation needs ADS API key.
    """
    # TODO: Implement ADS API call
    # ADS API: https://ads.readthedocs.io/
    pass


def fetch_citations_from_semanticscholar(arxiv_ids: List[str]) -> Dict[str, Dict[int, int]]:
    """
    Fetch citation data from Semantic Scholar API.
    
    Free tier: 100 requests/minute, 100K/year
    """
    # TODO: Implement Semantic Scholar API
    # API: https://api.semanticscholar.org/
    pass


# =============================================================================
# IDENTIFICATION ALGORITHMS
# =============================================================================

def identify_sb_by_peak_delay(papers: List[Paper], 
                               threshold_years: int = 10,
                               min_late_citations: int = 10) -> List[SleepingBeautyCandidate]:
    """
    Identify SBs based on delayed citation peak.
    
    Paper is SB if peak citations occur >= threshold_years after publication.
    """
    candidates = []
    
    for paper in papers:
        if paper.delay_to_peak is None:
            continue
            
        # Check if peak is delayed enough
        if paper.delay_to_peak >= threshold_years:
            # Additional check: has meaningful late citations
            late_citations = sum(
                paper.citations_by_year.get(y, 0)
                for y in range(paper.year + EARLY_YEARS, 2026)
            )
            
            if late_citations >= min_late_candidates:
                score = paper.delay_to_peak * np.log1p(paper.peak_citations or 0)
                candidates.append(SleepingBeautyCandidate(
                    paper=paper,
                    method=f"peak-delay-{threshold_years}y",
                    score=score
                ))
    
    return sorted(candidates, key=lambda x: x.score, reverse=True)


def identify_sb_by_ratio(papers: List[Paper],
                         ratio_threshold: float = 10,
                         min_early: int = 1,
                         min_total: int = 20) -> List[SleepingBeautyCandidate]:
    """
    Identify SBs based on citation ratio (late/early).
    
    Paper is SB if beauty coefficient >= ratio_threshold.
    """
    candidates = []
    
    for paper in papers:
        if paper.beauty_coefficient is None:
            continue
            
        if (paper.beauty_coefficient >= ratio_threshold and
            paper.early_citations >= min_early and
            paper.total_citations >= min_total):
            
            score = paper.beauty_coefficient * np.log1p(paper.total_citations)
            candidates.append(SleepingBeautyCandidate(
                paper=paper,
                method=f"ratio-{ratio_threshold}x",
                score=score
            ))
    
    return sorted(candidates, key=lambda x: x.score, reverse=True)


def identify_sb_by_absolute(papers: List[Paper],
                            max_early: int = 5,
                            min_late: int = 50) -> List[SleepingBeautyCandidate]:
    """
    Identify SBs based on absolute citation counts.
    
    Paper is SB if: few early citations (< max_early) but many later (> min_late).
    """
    candidates = []
    
    for paper in papers:
        if paper.early_citations <= max_early:
            late_citations = sum(
                paper.citations_by_year.get(y, 0)
                for y in range(paper.year + EARLY_YEARS, 2026)
            )
            
            if late_citations >= min_late:
                score = late_citations / (paper.early_citations + 1)
                candidates.append(SleepingBeautyCandidate(
                    paper=paper,
                    method="absolute",
                    score=score
                ))
    
    return sorted(candidates, key=lambda x: x.score, reverse=True)


# =============================================================================
# ANALYSIS
# =============================================================================

def analyze_concept_correlation(candidates: List[SleepingBeautyCandidate]) -> Dict:
    """
    Analyze what concepts/fields are overrepresented in SBs.
    """
    from collections import Counter
    
    all_concepts = []
    for cand in candidates:
        all_concepts.extend(cand.paper.concepts)
    
    concept_counts = Counter(all_concepts)
    
    return {
        "total_sb_papers": len(candidates),
        "concept_frequency": concept_counts.most_common(20),
    }


def classify_by_rationale(candidates: List[SleepingBeautyCandidate]) -> Dict[str, List]:
    """
    Classify SBs by their proposed awakening rationale.
    
    This requires manual curation + NLP analysis.
    """
    # Placeholder - to be implemented with text analysis
    classifications = {
        "premature_discovery": [],
        "methodological_innovation": [],
        "data_release": [],
        "theoretical_framework": [],
        "observational_discovery": [],
        "negative_results": [],
        "review_synthesis": [],
        "unclassified": []
    }
    
    return classifications


# =============================================================================
# VISUALIZATION
# =============================================================================

def plot_citation_trajectory(paper: Paper, save_path: Optional[Path] = None):
    """
    Plot citation trajectory over time.
    """
    import matplotlib.pyplot as plt
    
    years = sorted(paper.citations_by_year.keys())
    citations = [paper.citations_by_year.get(y, 0) for y in years]
    
    plt.figure(figsize=(10, 5))
    plt.bar(years, citations, alpha=0.7)
    plt.axvline(x=paper.year, color='green', linestyle='--', label='Published')
    plt.axvline(x=paper.peak_year, color='red', linestyle='--', label=f'Peak ({paper.peak_year})')
    
    plt.xlabel('Year')
    plt.ylabel('Citations')
    plt.title(f'{paper.arxiv_id}: {paper.title[:50]}...')
    plt.legend()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()


def plot_sb_distribution(candidates: List[SleepingBeautyCandidate], 
                         save_path: Optional[Path] = None):
    """
    Plot distribution of SB candidates by year and method.
    """
    import matplotlib.pyplot as plt
    
    years = [c.paper.year for c in candidates]
    methods = [c.method for c in candidates]
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Year distribution
    axes[0].hist(years, bins=range(1992, 2026), alpha=0.7)
    axes[0].set_xlabel('Publication Year')
    axes[0].set_ylabel('Number of SB Candidates')
    axes[0].set_title('SB Candidates by Year')
    
    # Method distribution
    method_counts = pd.Series(methods).value_counts()
    axes[1].bar(method_counts.index, method_counts.values, alpha=0.7)
    axes[1].set_xlabel('Method')
    axes[1].set_ylabel('Count')
    axes[1].set_title('SB by Identification Method')
    plt.xticks(rotation=45)
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()


# =============================================================================
# MAIN PIPELINE
# =============================================================================

def run_pipeline():
    """
    Main pipeline to identify and analyze sleeping beauties.
    """
    print("=" * 60)
    print("Astro-ph Sleeping Beauty Pipeline")
    print("=" * 60)
    
    # Step 1: Load data
    print("\n[1/5] Loading knowledge graph data...")
    kg_data = load_knowledge_graph_data()
    
    # Step 2: Fetch citations (placeholder)
    print("\n[2/5] Fetching citation data...")
    # citations = fetch_citations_from_ads(...) 
    
    # Step 3: Identify SBs
    print("\n[3/5] Identifying sleeping beauties...")
    # papers = build_paper_list(...)
    # sb_peak = identify_sb_by_peak_delay(papers)
    # sb_ratio = identify_sb_by_ratio(papers)
    # sb_abs = identify_sb_by_absolute(papers)
    
    # Step 4: Analyze
    print("\n[4/5] Analyzing concepts and rationale...")
    # concept_analysis = analyze_concept_correlation(all_sb)
    
    # Step 5: Visualize
    print("\n[5/5] Generating visualizations...")
    # plot_sb_distribution(...)
    
    print("\n" + "=" * 60)
    print("Pipeline complete!")
    print("=" * 60)
    
    return {
        "status": "needs_data",
        "message": "Full pipeline requires citation data from ADS/Semantic Scholar"
    }


if __name__ == "__main__":
    run_pipeline()
