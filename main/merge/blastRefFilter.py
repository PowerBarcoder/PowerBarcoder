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
    query: str
    subject: str
    identity: float
    mismatch: int
    qstart: int
    qend: int
    sstart: int
    send: int


"""
r_who_ref_pair_dict = 
{
    "Pronephrium_parishii_Wade5807_KTHU2139_02_0.398_abundance_840":{
        "Diplazium_fraxinifolium":[
                                    [9430], # r1 line number
                                    [200411], # r2 line number
                                    [185] # overlap length
                                    [9147.859749000001] # r1 identity * r2 identity
                                ],...
    }
}
"""


@dataclass
class BlastPairMetrics:
    """Metrics for a pair of r1/r2 blast results."""
    r1_line_number: int
    r2_line_number: int
    overlap_length: Optional[float] = None
    identity_score: Optional[float] = None


@dataclass
class RefPair:
    """Reference sequence pair information."""
    ref_name: str
    metrics: BlastPairMetrics


@dataclass
class AsvBlastResults:
    """Collection of blast results for an ASV."""
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
    """Reads the blast results from a file with specified encoding."""
    try:
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        with file_path.open(encoding=encoding) as f:
            return [line for line in f.readlines() if line.strip()]
    except Exception as e:
        logging.error(f"Error reading file {file_path}: {str(e)}")


def parse_blast_line(line: str) -> BlastEntry:
    """Parses a single line of blast results into a BlastEntry."""
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
    """Filters and returns the intersection set of r1 and r2."""
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
    """Calculate overlap range and identity score for a pair of entries."""
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
    """Process intersection results using dataclass structure."""
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
    """Calculate metrics using dataclass structure."""
    for asv_result in results.values():
        for ref_name, metrics in asv_result.ref_pairs.items():
            r1_entry = parse_blast_line(lines[metrics.r1_line_number])
            r2_entry = parse_blast_line(lines[metrics.r2_line_number])

            overlap_range, identity_score = calculate_overlap_and_identity(r1_entry, r2_entry)
            asv_result.update_metrics(ref_name, overlap_range, identity_score)

    return results


def filter_by_max_overlap(results: Dict[str, AsvBlastResults]) -> Dict[str, AsvBlastResults]:
    """Filter using dataclass structure."""
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
    """Filter using dataclass structure."""
    for asv_result in results.values():
        max_identity = max(metrics.identity_score or 0 for metrics in asv_result.ref_pairs.values())

        # Remove pairs with less than max identity
        asv_result.ref_pairs = {
            ref_name: metrics
            for ref_name, metrics in asv_result.ref_pairs.items()
            if metrics.identity_score == max_identity
        }

    return results


def blast_ref_filter(load_dir: str, loci_name: str, blast_parsing_mode: str) -> Dict[str, AsvBlastResults]:
    """
    Filters the blast results based on specific criteria and writes the filtered results to a file.

    Args:
        load_dir (str): The directory where the blast results are stored.
        loci_name (str): The name of the loci.
        blast_parsing_mode (str): The mode of parsing to be used.

    Returns:
        dict: A dictionary containing the filtered blast results.
    """
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
        # 過濾步驟 2：根據交集結果，計算每個比對對應的 overlap長度 和 identity 比率，並存入字典。
        # (將共有的序列按ASV_ref的方式分類，整理每筆blast結果在檔案內的行數，並計算該配對的overlap長度、identity乘積，取出最佳者)
        # 計算方法：
        #     # r1 r2方向經過10Ncat後都一致了，不需要rc，
        #     # 按照ref的方向會有兩種情況
        #     # 先用r1 send - r1 sstart判斷方向，>0者，必為正向
        #     # overlapRange = (r1 send - r2 sstart)*1
        #     # 再用r1 send -r1 sstart判斷方向，<0者，乘負號轉正向
        #     # overlapRange = (r1 send - r2 sstart)*-1
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
            f"blastRefFilter.py filtered file from {original_line_count} lines of reads to {final_line_count} lines on loci: {loci_name}"
        )
        return results

    except Exception as e:
        logging.error(f"Error in blast_ref_filter: {str(e)}")
        return {}


if __name__ == "__main__":
    main_load_dir = "C:/Users/kwz50/IdeaProjects/PowerBarcoder/data/result/202312011906/"
    main_loci_name = "trnLF"
    main_blast_parsing_mode = "2"
    logging.info(f"Executing directly with path: {main_load_dir}")
    blast_ref_filter(main_load_dir, main_loci_name, main_blast_parsing_mode)
