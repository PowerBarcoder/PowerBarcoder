"""
BLAST Reference Filter Module

This module implements filtering of BLAST results for paired-end sequences (r1/r2).
The filtering process consists of several steps:

1. Intersection Filtering:
   - Identifies pairs where both r1 and r2 match the same reference

2. Overlap and Identity Calculation:
   - For each pair, calculates:
     a) Overlap length between r1 and r2 sequences
     b) Identity score based on mismatches
   - Direction handling:
     - r1/r2 direction is consistent after 10Ncat, no rc needed
     - Reference direction cases:
       * If (r1.send - r1.sstart > 0): forward direction
         overlap = (r1.send - r2.sstart)
       * If (r1.send - r1.sstart < 0): reverse direction
         overlap = (r1.send - r2.sstart) * -1

3. Maximum Overlap Selection:
   - Retains only the pairs with maximum overlap length for each ASV

4. Maximum Identity Selection:
   - Among pairs with equal overlap, keeps those with highest identity scores

Data Structure Example:
    {
        "ASV_name": {
            "reference_name": [
                [r1_line_number],
                [r2_line_number],
                [overlap_length],
                [identity_score]
            ]
        }
    }

Example:
    {
        "Pronephrium_parishii_Wade5807_KTHU2139_02_0.398_abundance_840": {
            "Diplazium_fraxinifolium": [
                [9430],
                [200411],
                [185],
                [9147.859749000001]
            ], ...
        }
    }
"""

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# File encoding constants
DEFAULT_ENCODING = 'utf-8'

# Constants for refResult indices
QSSEQID_INDEX = 0
SSEQID_INDEX = 1
IDENTITY_INDEX = 2
LENGTH_INDEX = 3
MISMATCH_INDEX = 4
GAPOPEN_INDEX = 5
QSTART_INDEX = 6
QEND_INDEX = 7
SEND_INDEX = 8
SSTART_INDEX = 9
EVALUE_INDEX = 10
BITSCORE_INDEX = 11

# Constants for file paths
BLAST_RESULT_DIR = "blastResult"
REF_RESULT_SUFFIX = "_refResult.txt"
INTERSECTION_SUFFIX = "_refResult_intersection.txt"
FILTERED_SUFFIX = "_refResult_filtered.txt"


@dataclass
class BlastEntry:
    """Represents a single BLAST result entry."""
    query: str
    subject: str
    identity: float
    mismatch: int
    qstart: int
    qend: int
    sstart: int
    send: int


@dataclass
class BlastPairMetrics:
    """Stores metrics for a pair of r1/r2 blast results."""
    r1_line_number: int
    r2_line_number: int
    overlap_length: Optional[float] = None
    identity_score: Optional[float] = None


@dataclass
class RefPair:
    """Holds reference sequence pair information."""
    ref_name: str
    metrics: BlastPairMetrics


@dataclass
class AsvBlastResults:
    """Manages blast results for an ASV sequence."""
    asv_name: str
    ref_pairs: Dict[str, BlastPairMetrics] = field(default_factory=dict)

    def add_pair(self, ref_name: str, r_who: str, line_number: int):
        """Add a new r1/r2 line number to the reference pair."""
        if ref_name not in self.ref_pairs:
            self.ref_pairs[ref_name] = BlastPairMetrics(r1_line_number=-1, r2_line_number=-1)

        if r_who == "r1":
            self.ref_pairs[ref_name].r1_line_number = line_number
        elif r_who == "r2":
            self.ref_pairs[ref_name].r2_line_number = line_number

    def update_metrics(self, ref_name: str, overlap: float, identity: float):
        """Update metrics for a reference pair."""
        if ref_name in self.ref_pairs:
            self.ref_pairs[ref_name].overlap_length = overlap
            self.ref_pairs[ref_name].identity_score = identity


def read_blast_results(file_path: Path, encoding: str = DEFAULT_ENCODING) -> List[str]:
    """Read and filter empty lines from blast results file."""
    try:
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        with file_path.open(encoding=encoding) as f:
            return [line for line in f.readlines() if line.strip()]
    except Exception as e:
        logging.error(f"Error reading file {file_path}: {str(e)}")


def parse_blast_line(line: str) -> BlastEntry:
    """Convert tab-separated blast result line to BlastEntry."""
    columns = line.strip().split("\t")
    return BlastEntry(
        query=columns[QSSEQID_INDEX],
        subject=columns[SSEQID_INDEX],
        identity=float(columns[IDENTITY_INDEX]),
        mismatch=int(columns[MISMATCH_INDEX]),
        qstart=int(columns[QSTART_INDEX]),
        qend=int(columns[QEND_INDEX]),
        sstart=int(columns[SSTART_INDEX]),
        send=int(columns[SEND_INDEX]),
    )


def filter_intersection(lines: List[str]) -> Tuple[set, set]:
    """Build r1 and r2 reference pair sets."""
    r1_set, r2_set = set(), set()
    for line in lines:
        if not line.strip():
            continue
        entry = parse_blast_line(line)
        query_r_who = entry.query.split("_")[-1]
        query_name = "_".join(entry.query.split("_")[:-1])
        ref_pair = f"{query_name}_{entry.subject}"
        if query_r_who == "r1":
            r1_set.add(ref_pair)
        elif query_r_who == "r2":
            r2_set.add(ref_pair)
    return r1_set, r2_set


def calculate_overlap_and_identity(r1_entry: BlastEntry, r2_entry: BlastEntry) -> Tuple[int, float]:
    """Calculate overlap range and identity score."""
    identity_score = 1 - (r1_entry.mismatch + r2_entry.mismatch) / (
            abs(r1_entry.qstart - r1_entry.qend) + 1 +
            abs(r2_entry.qstart - r2_entry.qend) + 1)

    if r1_entry.send - r1_entry.sstart > 0:
        overlap_range = (r1_entry.send - r2_entry.sstart)
    elif r1_entry.send - r1_entry.sstart < 0:
        overlap_range = (r1_entry.send - r2_entry.sstart) * -1
    else:
        overlap_range = 0
    return overlap_range, identity_score


def write_filtered_results(output_path: Path, filtered_lines: List[str]) -> None:
    """Write filtered results to output file."""
    try:
        with output_path.open("w", encoding=DEFAULT_ENCODING) as f:
            f.writelines(filtered_lines)
    except Exception as e:
        logging.error(f"Error writing filtered results: {str(e)}")


def process_intersection_results(lines: List[str]) -> Dict[str, AsvBlastResults]:
    """Process results and organize by ASV."""
    results: Dict[str, AsvBlastResults] = {}

    for line_number, line in enumerate(lines):
        entry = parse_blast_line(line)
        query_name = "_".join(entry.query.split("_")[:-1])
        r_who = entry.query.split("_")[-1]

        if query_name not in results:
            results[query_name] = AsvBlastResults(asv_name=query_name)

        results[query_name].add_pair(entry.subject, r_who, line_number)

    return results


def calculate_metrics_for_pairs(results: Dict[str, AsvBlastResults], lines: List[str]) -> Dict[str, AsvBlastResults]:
    """Calculate overlap and identity metrics for all pairs."""
    for asv_result in results.values():
        for ref_name, metrics in asv_result.ref_pairs.items():
            r1_entry = parse_blast_line(lines[metrics.r1_line_number])
            r2_entry = parse_blast_line(lines[metrics.r2_line_number])

            overlap_range, identity_score = calculate_overlap_and_identity(r1_entry, r2_entry)
            asv_result.update_metrics(ref_name, overlap_range, identity_score)

    return results


def filter_by_max_overlap(results: Dict[str, AsvBlastResults]) -> Dict[str, AsvBlastResults]:
    """Keep only pairs with maximum overlap."""
    for asv_result in results.values():
        max_overlap = max(metrics.overlap_length or 0 for metrics in asv_result.ref_pairs.values())

        # Remove pairs with less than max overlap
        asv_result.ref_pairs = {
            ref_name: metrics
            for ref_name, metrics in asv_result.ref_pairs.items()
            if metrics.overlap_length == max_overlap
        }

    return results


def filter_by_max_identity(results: Dict[str, AsvBlastResults]) -> Dict[str, AsvBlastResults]:
    """Keep only pairs with maximum identity among equal overlaps."""
    for asv_result in results.values():
        max_identity = max(metrics.identity_score or 0 for metrics in asv_result.ref_pairs.values())

        # Remove pairs with less than max identity
        asv_result.ref_pairs = {
            ref_name: metrics
            for ref_name, metrics in asv_result.ref_pairs.items()
            if metrics.identity_score == max_identity
        }

    return results


def primary_blast_ref_filter(load_dir: str, loci_name: str, blast_parsing_mode: str) -> Dict[str, AsvBlastResults]:
    """Execute BLAST reference filtering pipeline."""
    try:
        load_dir = Path(load_dir)
        result_dir = load_dir / f"{loci_name}_result" / BLAST_RESULT_DIR

        input_path = result_dir / f"{loci_name}{REF_RESULT_SUFFIX}"
        intersection_path = result_dir / f"{loci_name}{INTERSECTION_SUFFIX}"
        filtered_file_path = result_dir / f"{loci_name}{FILTERED_SUFFIX}"

        logging.info(f"Starting blast filtering for loci {loci_name} in mode {blast_parsing_mode}")

        # Read and process input
        lines = read_blast_results(input_path, DEFAULT_ENCODING)
        original_line_count = len(lines)

        # Filter 1: Use sets for r1_set, r2_set, and r1r2_set
        r1_set, r2_set = filter_intersection(lines)
        intersection_set = r1_set.intersection(r2_set)

        # Write intersection results
        intersection_lines = [
            line for line in lines
            if "_".join(parse_blast_line(line).query.rsplit("_", 1)[:-1]) + "_" +
               parse_blast_line(line).subject in intersection_set
        ]
        write_filtered_results(intersection_path, intersection_lines)

        # Filter 2: Calculate overlap length and identity ratio for each pair
        results = process_intersection_results(intersection_lines)
        results = calculate_metrics_for_pairs(results, lines)

        # Filter 3: Retain the entry with the maximum overlap for each ASV name, deleting the rest
        results = filter_by_max_overlap(results)

        # Filter 4: Retain the entry with the maximum identity if multiple entries have the same maximum overlap, deleting the rest
        results = filter_by_max_identity(results)

        # Write filtered results
        with filtered_file_path.open("w") as file:
            for asv_result in results.values():
                for metrics in asv_result.ref_pairs.values():
                    file.write(lines[metrics.r1_line_number])
                    file.write(lines[metrics.r2_line_number])

        # Count lines
        with open(filtered_file_path, encoding='iso-8859-1') as f:
            lines = f.readlines()
            final_line_count = len(lines)

        logging.info(
            f"primary_blast_ref_filter.py filtered file from {original_line_count} lines of reads to {final_line_count} lines on loci: {loci_name}"
        )
        return results

    except Exception as e:
        logging.error(f"Error in primary_blast_ref_filter: {str(e)}")
        return {}


