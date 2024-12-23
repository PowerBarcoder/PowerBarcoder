OVERALL_INFO_STEP_LIST = [
    "Raw data r1",
    "Raw data r2",
    "Fastp quality trim r1",
    "Fastp quality trim r2",
    "Cutadapt demultiplex by locus primer r1",
    "Cutadapt demultiplex by locus primer r2"
]

FILE_SET_PARAMETER_LIST = [
    "Cutadapt demultiplex by sample barcode r1",
    "Cutadapt demultiplex by sample barcode r2",
    "Cutadapt trim the primer sites r1",
    "Cutadapt trim the primer sites r2",
    "DADA2 filter r1",
    "DADA2 filter r2",
    "DADA2 denoise r1",
    "DADA2 denoise r2",
    "DADA2 merge",
    "DADA2 10N concat",
    "Merger blast r1",
    "Merger blast r2",
    "Merger merge"
]

STEPS = [
    ("Cutadapt demultiplex by sample barcode", "r1"),
    ("", "r2"),
    ("Cutadapt trim the primer sites", "r1"),
    ("", "r2"),
    ("DADA2 filter", "r1"),
    ("", "r2"),
    ("DADA2 denoise", "r1"),
    ("", "r2"),
    ("DADA2 merge", "-"),
    ("DADA2 10N concat", "-"),
    ("Merger blast", "r1"),
    ("Merger blast", "r2"),
    ("Merger merge", "-")
]  # Create the illusion of merged cells
