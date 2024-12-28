"""
This module defines the `BlastRef` class for processing BLAST result files.

The `BlastRef` class:
- Reads BLAST output files.
- Extracts relevant data based on parsing modes.
- Stores processed results in attributes for further analysis.

### Class:
- `BlastRef`: Represents a processor for handling BLAST result files.

### Example Usage:
    load_dir = "path/to/blast/results"
    loci_name = "gene_region"
    parsing_mode = "2"  # Parsing modes: 0, 1, 2, or 3
    blast_ref = BlastRef()
    blast_ref.secondary_blast_ref_filter(load_dir, loci_name, parsing_mode)

### Data Fields:
Field Name      | Input Format            | Output Attribute       | Description                            |
----------------|-------------------------|------------------------|----------------------------------------|
qseqid          | Tab-separated field     | qseqid_list            | Query sequence ID (e.g., gene name)    |
sseqid          | Tab-separated field     | sseqid_list            | Subject sequence ID (reference genome) |
pident          | Float value             | pident_list            | Percentage of identical matches (0~100)|
length          | Integer value           | length_list            | Alignment length                       |
mismatch        | Integer value           | mismatch_list          | Number of mismatches                   |
gapopen         | Integer value           | gapopen_list           | Number of gap openings                 |
qstart          | Integer value           | qstart_list            | Start position in query                |
qend            | Integer value           | qend_list              | End position in query                  |
sstart          | Integer value           | sstart_list            | Start position in subject              |
send            | Integer value           | send_list              | End position in subject                |
evalue          | Float value             | evalue_list            | Expect value                           |
bitscore        | Float value             | bitscore_list          | Alignment bit score                    |
-               | Calculated              | qstart_minus_qend_list | |qstart - qend|                        |
-               | Calculated              | sstart_minus_send_list | |sstart - send|                        |
-               | Determined              | rwho_list              | Read origin (r1/r2/cat)                |

### Parsing Modes:
- **Mode 0**: Prioritizes highest identity; ties resolved by maximum alignment length (`qstart-qend`).
- **Mode 1**: Prioritizes maximum alignment length; ties resolved by highest identity.
- **Mode 2**: Combines identity and alignment length as a product.
- **Mode 3**: Prioritizes smallest e-value below 0.01 (high-confidence alignments).

"""

import logging
import os
from dataclasses import dataclass
from typing import Dict, List, Optional

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# File related constants
TARGET_FILE_NAME = "_refResult_filtered.txt"
DEFAULT_ENCODING = 'utf-8'  # Changed from iso-8859-1

# BLAST result column indices
QSEQID_IDX = 0
SSEQID_IDX = 1
PIDENT_IDX = 2
LENGTH_IDX = 3
MISMATCH_IDX = 4
GAPOPEN_IDX = 5
QSTART_IDX = 6
QEND_IDX = 7
SSTART_IDX = 8
SEND_IDX = 9
EVALUE_IDX = 10
BITSCORE_IDX = 11
QSTART_MINUS_QEND_IDX = 12
SSTART_MINUS_SEND_IDX = 13
RWHO_IDX = 14

# Parsing mode constants
MODE_IDENTITY_FIRST = "0"
MODE_LENGTH_FIRST = "1"
MODE_COMBINED = "2"
MODE_EVALUE = "3"

# Threshold values
MAX_EVALUE_THRESHOLD = 0.01


@dataclass
class BlastResult:
    """Data class for storing BLAST result values."""
    qseqid: str
    sseqid: str
    pident: float
    length: int
    mismatch: int
    gapopen: int
    qstart: int
    qend: int
    sstart: int
    send: int
    evalue: float
    bitscore: float
    qstart_minus_qend: int
    sstart_minus_send: int
    rwho: str


class BlastRef:
    """
    A class to represent the BlastRef object which processes BLAST results.
    
    Example:
        >>> blast_ref = BlastRef()
        >>> result = blast_ref.secondary_blast_ref_filter("path/to/blast/results/", "trnLF", "0")
        >>> isinstance(result, BlastRef)
        True
    """

    def __init__(self) -> None:
        """
        Initialize BlastRef with empty result lists and configuration.
        """
        self.qseqid_list: List[str] = []
        self.sseqid_list: List[str] = []
        self.pident_list: List[float] = []
        self.length_list: List[int] = []
        self.mismatch_list: List[int] = []
        self.gapopen_list: List[int] = []
        self.qstart_list: List[int] = []
        self.qend_list: List[int] = []
        self.sstart_list: List[int] = []
        self.send_list: List[int] = []
        self.evalue_list: List[float] = []
        self.bitscore_list: List[float] = []
        self.qstart_minus_qend_list: List[int] = []
        self.sstart_minus_send_list: List[int] = []
        self.rwho_list: List[str] = []
        self._encoding: str = DEFAULT_ENCODING

    def set_encoding(self, encoding: str) -> None:
        """Sets the file encoding to use."""
        self._encoding = encoding

    def _get_qseqid_file_dirs(self, load_dir: str, loci_name: str) -> Dict[str, str]:
        """Returns qseqid file directory paths."""
        return {
            "r1": os.path.join(load_dir, f"{loci_name}_result/mergeResult/merger/r1/"),
            "r2": os.path.join(load_dir, f"{loci_name}_result/mergeResult/merger/r2/"),
            "cat": os.path.join(load_dir, f"{loci_name}_result/mergeResult/merger/nCatR1R2/forSplit/")
        }

    def _get_qseqid_file_path(self, query_name: str, file_dirs: dict) -> str:
        """Returns the appropriate file path based on query name."""
        if "_r1" in query_name:
            return os.path.join(file_dirs["r1"], query_name)
        elif "_r2" in query_name:
            return os.path.join(file_dirs["r2"], query_name)
        return os.path.join(file_dirs["cat"], query_name)

    def _read_file_safe(self, file_path: str) -> Optional[List[str]]:
        """Safely reads a file with error handling."""
        try:
            with open(file_path, encoding=self._encoding) as f:
                return f.readlines()
        except FileNotFoundError:
            logging.error(f"File not found: {file_path}")
            return None
        except UnicodeDecodeError:
            logging.warning(f"Unable to decode file with {self._encoding}, trying fallback encoding")
            try:
                with open(file_path, encoding='iso-8859-1') as f:
                    return f.readlines()
            except Exception as e:
                logging.error(f"Failed to read file with fallback encoding: {e}")
                return None
        except Exception as e:
            logging.error(f"Unexpected error reading file {file_path}: {e}")
            return None

    def _get_sequence_length(self, file_path: str) -> int:
        """Returns the length of the sequence from a FASTA file."""
        with open(file_path, encoding='utf-8') as f:
            lines = f.readlines()
            return len(lines[1].strip())

    def _determine_rwho(self, query_name: str) -> str:
        """Determines the read origin (r1, r2, or rWho)."""
        if "_r1" in query_name:
            return "r1"
        elif "_r2" in query_name:
            return "r2"
        return "rWho"

    def _parse_blast_line(self, line: str) -> Optional[BlastResult]:
        """Parses a BLAST result line into a BlastResult object."""
        try:
            text_list = line.strip().split("\t")
            if len(text_list) < 12:
                return None

            query_name = text_list[0] + ".fas"
            values = text_list[1:12]
            qstart_minus_qend = abs(int(values[5]) - int(values[6]))
            sstart_minus_send = abs(int(values[7]) - int(values[8]))
            rwho = self._determine_rwho(query_name)

            return BlastResult(
                qseqid=query_name,
                sseqid=values[0],
                pident=float(values[1]),
                length=int(values[2]),
                mismatch=int(values[3]),
                gapopen=int(values[4]),
                qstart=int(values[5]),
                qend=int(values[6]),
                sstart=int(values[7]),
                send=int(values[8]),
                evalue=float(values[9]),
                bitscore=float(values[10]),
                qstart_minus_qend=qstart_minus_qend,
                sstart_minus_send=sstart_minus_send,
                rwho=rwho
            )
        except (ValueError, IndexError) as e:
            logging.error(f"Error parsing BLAST line: {e}")
            return None

    def _apply_parsing_mode(self, current: BlastResult, new: BlastResult, mode: str) -> BlastResult:
        """Applies the parsing mode logic to determine which result to keep."""
        if mode == MODE_IDENTITY_FIRST:
            if new.pident > current.pident:
                return new
            elif new.pident == current.pident and new.qstart_minus_qend > current.qstart_minus_qend:
                return new
        elif mode == MODE_LENGTH_FIRST:
            if new.qstart_minus_qend > current.qstart_minus_qend:
                return new
            elif new.qstart_minus_qend == current.qstart_minus_qend and new.pident > current.pident:
                return new
        elif mode == MODE_COMBINED:
            if (new.qstart_minus_qend * new.pident) > (current.qstart_minus_qend * current.pident):
                return new
        elif mode == MODE_EVALUE:
            if new.evalue < MAX_EVALUE_THRESHOLD and new.evalue < current.evalue:
                return new
        return current

    def _update_attributes_from_results(self, results: Dict[str, BlastResult]) -> None:
        """Updates object attributes from the results dictionary."""
        self.qseqid_list = [r.qseqid for r in results.values()]
        self.sseqid_list = [r.sseqid for r in results.values()]
        self.pident_list = [r.pident for r in results.values()]
        self.length_list = [r.length for r in results.values()]
        self.mismatch_list = [r.mismatch for r in results.values()]
        self.gapopen_list = [r.gapopen for r in results.values()]
        self.qstart_list = [r.qstart for r in results.values()]
        self.qend_list = [r.qend for r in results.values()]
        self.sstart_list = [r.sstart for r in results.values()]
        self.send_list = [r.send for r in results.values()]
        self.evalue_list = [r.evalue for r in results.values()]
        self.bitscore_list = [r.bitscore for r in results.values()]
        self.qstart_minus_qend_list = [r.qstart_minus_qend for r in results.values()]
        self.sstart_minus_send_list = [r.sstart_minus_send for r in results.values()]
        self.rwho_list = [r.rwho for r in results.values()]

    def _process_blast_results(self, lines: List[str], blast_parsing_mode: str) -> Dict[str, BlastResult]:
        """Process BLAST result lines into a dictionary of BlastResult objects."""
        results: Dict[str, BlastResult] = {}

        for line in lines:
            if not line.strip():
                continue

            result = self._parse_blast_line(line)
            if not result:
                continue

            if result.qseqid not in results:
                results[result.qseqid] = result
            else:
                results[result.qseqid] = self._apply_parsing_mode(
                    results[result.qseqid], result, blast_parsing_mode
                )

        return results

    def secondary_blast_ref_filter(self, load_dir: str, loci_name: str, blast_parsing_mode: str) -> Optional['BlastRef']:
        """
        Process BLAST results and populate object attributes.

        Returns:
            Optional[BlastRef]: The populated BlastRef object, or None if processing fails
        """
        logging.info(f"Starting BLAST processing with mode: {blast_parsing_mode}")

        file_dirs = self._get_qseqid_file_dirs(load_dir, loci_name)
        input_file_path = os.path.join(load_dir, f"{loci_name}_result", "blastResult", f"{loci_name}{TARGET_FILE_NAME}")

        # Step 1: Read file
        lines = self._read_file_safe(input_file_path)

        if not lines:
            logging.error("Failed to read input file")
            return None

        try:
            # Step 2: Process the lines and update the category dictionary
            results = self._process_blast_results(lines, blast_parsing_mode)
            # Step 3: Assemble the results into object attributes
            self._update_attributes_from_results(results)
            logging.info(f"Successfully processed {len(results)} BLAST results")
            return self
        except Exception as e:
            logging.error(f"Error processing BLAST results: {e}")
            return None
