import os
import sys

import pytest
from pathlib import Path

# Add the project root directory to the PYTHONPATH
project_root = Path(__file__).resolve().parents[2]
sys.path.append(str(project_root))

from main.merge.blastResultParser import main as blast_result_parser_main


def test_blast_result_parser(monkeypatch):
    """Test the blast_result_parser main function."""
    amplicon_info = "test_amplicon_info"
    result_data_path = r"C:\Users\kwz50\IdeaProjects\PowerBarcoder\tests\data\result\202412281411"
    blast_parsing_mode = "0"
    name_of_loci = "trnLF"

    # Mock command line arguments
    monkeypatch.setattr('sys.argv',
                        ['blastResultParser.py', amplicon_info, result_data_path, blast_parsing_mode, name_of_loci])

    # Run the main function
    blast_result_parser_main()

    # Verify the output file
    output_file_path = os.path.join(result_data_path, f"{name_of_loci}_result", "blastResult",
                                    f"{name_of_loci}_blastResult.txt")
    assert os.path.exists(output_file_path)

    # Verify the content of the output file
    with open(output_file_path, "r") as file:
        lines = file.readlines()
        assert len(lines) > 0
