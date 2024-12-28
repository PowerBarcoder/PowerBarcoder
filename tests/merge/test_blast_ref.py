import os
import sys
import logging
import pytest
from pathlib import Path

# Add the project root directory to the PYTHONPATH
project_root = Path(__file__).resolve().parents[2]
sys.path.append(str(project_root))

from main.merge.BlastRef import BlastRef

# Configure test logging
logging.basicConfig(level=logging.INFO)


@pytest.fixture
def blast_ref_instance():
    """Create a BlastRef instance for testing."""
    return BlastRef()


def test_blast_ref_initialization(blast_ref_instance):
    """Test that BlastRef is properly initialized with empty lists."""
    assert len(blast_ref_instance.qseqid_list) == 0
    assert len(blast_ref_instance.sseqid_list) == 0


def test_blast_ref_processing(blast_ref_instance):
    """Test the full BLAST result processing workflow."""
    load_dir = r"C:\Users\kwz50\IdeaProjects\PowerBarcoder\tests\data\result\202412281411"
    loci_name = "trnLF"
    blast_parsing_mode = "0"

    result = blast_ref_instance.blast_ref(load_dir, loci_name, blast_parsing_mode)

    # Verify processing was successful
    assert result is not None
    assert len(blast_ref_instance.qseqid_list) > 0
    assert len(blast_ref_instance.sseqid_list) > 0
    assert len(blast_ref_instance.pident_list) > 0
    assert len(blast_ref_instance.length_list) > 0


def test_blast_result_class():
    """Test with real data path."""
    test_load_dir = r"C:\Users\kwz50\IdeaProjects\PowerBarcoder\tests\data\result\202412281411"
    test_loci_name = "trnLF"
    test_blast_parsing_mode = "0"

    logging.info("Starting BlastRef processing")
    blast_ref_instance = BlastRef()
    result = blast_ref_instance.blast_ref(test_load_dir, test_loci_name, test_blast_parsing_mode)

    if result:
        logging.info("Processing completed successfully")
    else:
        logging.error("Processing failed")

    print(blast_ref_instance.qseqid_list)
    print(blast_ref_instance.sseqid_list)
    print(blast_ref_instance.pident_list)
    print(blast_ref_instance.length_list)
    print(blast_ref_instance.mismatch_list)
    print(blast_ref_instance.gapopen_list)
    print(blast_ref_instance.qstart_list)
    print(blast_ref_instance.qend_list)
    print(blast_ref_instance.sstart_list)
    print(blast_ref_instance.send_list)
    print(blast_ref_instance.evalue_list)
    print(blast_ref_instance.bitscore_list)
    print(blast_ref_instance.qstart_minus_qend_list)
    print(blast_ref_instance.sstart_minus_send_list)
    print(blast_ref_instance.rwho_list)
