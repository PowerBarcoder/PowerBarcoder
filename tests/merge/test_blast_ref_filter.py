import os
import sys

from pathlib import Path

# Add the project root directory to the PYTHONPATH
project_root = Path(__file__).resolve().parents[2]
sys.path.append(str(project_root))

from main.merge.blastRefFilter import blast_ref_filter


def test_blast_ref_filter():
    """Test the blast_ref_filter function with real data."""
    load_dir = r"C:\Users\kwz50\IdeaProjects\PowerBarcoder\tests\data\result\202412281411"
    loci_name = "trnLF"
    blast_parsing_mode = "0"

    result = blast_ref_filter(load_dir, loci_name, blast_parsing_mode)

    # Verify the output files
    blast_result_dir = os.path.join(load_dir, f"{loci_name}_result", "blastResult")
    intersection_file_path = os.path.join(blast_result_dir, f"{loci_name}_refResult_intersection.txt")
    filtered_file_path = os.path.join(blast_result_dir, f"{loci_name}_refResult_filtered.txt")

    assert os.path.exists(intersection_file_path)
    assert os.path.exists(filtered_file_path)

    # Verify the content of the filtered file
    with open(filtered_file_path, "r") as file:
        lines = file.readlines()
        assert len(lines) > 0
