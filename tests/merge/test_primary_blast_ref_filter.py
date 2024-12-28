import logging
import sys
from pathlib import Path

import pytest

# Add the project root directory to the PYTHONPATH
project_root = Path(__file__).resolve().parents[2]
sys.path.append(str(project_root))

from main.merge.blast.primary_blast_ref_filter import (
    primary_blast_ref_filter,
    BlastEntry,
    BlastPairMetrics,
    AsvBlastResults,
    calculate_overlap_and_identity,
    process_intersection_results,
)


@pytest.fixture
def sample_blast_entries():
    """Provide sample blast entries for testing."""
    r1_entry = BlastEntry(
        query="sample_asv_r1",
        subject="sample_ref",
        identity=98.0,
        mismatch=2,
        qstart=1,
        qend=100,
        sstart=50,
        send=150
    )
    r2_entry = BlastEntry(
        query="sample_asv_r2",
        subject="sample_ref",
        identity=97.0,
        mismatch=3,
        qstart=1,
        qend=100,
        sstart=140,
        send=240
    )
    return r1_entry, r2_entry


def test_calculate_overlap_and_identity(sample_blast_entries):
    """Test overlap and identity calculation."""
    r1_entry, r2_entry = sample_blast_entries
    overlap, identity = calculate_overlap_and_identity(r1_entry, r2_entry)

    assert overlap > 0
    assert 0 <= identity <= 1


def test_process_intersection_results():
    """Test processing of intersection results."""
    test_lines = [
        "asv1_r1\tref1\t98.0\t100\t2\t0\t1\t100\t50\t150\t0\t200\n",
        "asv1_r2\tref1\t97.0\t100\t3\t0\t1\t100\t140\t240\t0\t200\n"
    ]

    results = process_intersection_results(test_lines)

    assert len(results) == 1  # One ASV
    assert "asv1" in results
    assert len(results["asv1"].ref_pairs) == 1  # One reference
    assert "ref1" in results["asv1"].ref_pairs


def test_blast_ref_filter_integration():
    """Test the complete blast_ref_filter function with real data."""
    load_dir = Path(project_root) / "tests/data/result/202412281411"
    loci_name = "trnLF"
    blast_parsing_mode = "0"

    results = primary_blast_ref_filter(str(load_dir), loci_name, blast_parsing_mode)

    # Verify results structure
    assert isinstance(results, dict)
    for asv_result in results.values():
        assert isinstance(asv_result, AsvBlastResults)
        for metrics in asv_result.ref_pairs.values():
            assert isinstance(metrics, BlastPairMetrics)
            assert metrics.overlap_length is not None
            assert metrics.identity_score is not None

    # Verify output files
    result_dir = load_dir / f"{loci_name}_result" / "blastResult"
    intersection_file = result_dir / f"{loci_name}_refResult_intersection.txt"
    filtered_file = result_dir / f"{loci_name}_refResult_filtered.txt"

    assert intersection_file.exists()
    assert filtered_file.exists()

    # Verify filtered results content
    with filtered_file.open("r") as f:
        filtered_lines = f.readlines()
        assert len(filtered_lines) > 0
        # Each ASV should have paired entries (r1 and r2)
        assert len(filtered_lines) % 2 == 0


def test_primary_blast_result_class():
    main_load_dir = r"C:\Users\kwz50\IdeaProjects\PowerBarcoder\data\result\202412272019"
    main_loci_name = "trnLF"
    main_blast_parsing_mode = "2"
    logging.info(f"Executing directly with path: {main_load_dir}")
    primary_blast_ref_filter(main_load_dir, main_loci_name, main_blast_parsing_mode)
