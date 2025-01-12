**Introduction to PowerBarcoder**

PowerBarcoder is a **NGS data cleaning solution** specifically designed for data generated from the Illumina Miseq
platform. The primary goals of PowerBarcoder are to **save users time and money** while providing **high-performance**
data processing capabilities. This tool is a **GUI-based software**, making it user-friendly. It is **free and
open-source**, and it is also a **cross-platform software**, compatible with Windows, Linux, and Mac OS. PowerBarcoder
is primarily intended for processing DNA barcode data for biodiversity research.

**Why PowerBarcoder?**

- Save your time and money with PowerBarcoder.
- PowerBarcoder is a NGS data cleaning solution for Illumina Miseq.
- It is designed to clean NGS data with high performance.
- PowerBarcoder is a GUI-based software, which is easy to use.
- PowerBarcoder is a free software, which is open source.
- PowerBarcoder is a cross-platform software, which can be used in Windows, Linux, and Mac OS.

More details
in [this presentation](https://docs.google.com/presentation/d/19bZbIb3AJ-kiar02kEzdDUU-y5KkmoGy/edit?usp=sharing&ouid=107280427804502451722&rtpof=true&sd=true).

**Key Features of PowerBarcoder**

- **NGS Data Cleaning Solution (Miseq):** Specifically tailored for Illumina Miseq data.
- **High Performance:** Achieved through the use of coroutines, multi-threading, and multiprocessing designs.
- **Graphical User Interface (GUI):** Provides an easy-to-use interface.
- **Docker Deployment:** Facilitates easy deployment via Docker.
- **Flexible BLAST Mode Options:** Offers versatile options for sequence alignment.
- **QC Report in a Single CSV File:** Generates a comprehensive quality control report in CSV format.
- **Overcoming Pre-Merging Limitations:** PowerBarcoder merges reads after ASV inference, ensuring that paired-end ASVs
  are not lost when there are few or no overlapping bases.
- **Reference-Guided Merging Strategy:** Uses BLAST alignment to align paired reads with reference sequences, enabling
  effective merging even with minimal or no overlap.

**Functionalities of PowerBarcoder**

PowerBarcoder includes the following major functionalities for efficient NGS data processing:

1. **Data Input:** Accepts paired-end sequencing data from the MiSeq platform, stored in .gz format.
2. **Data Decompression:** Decompresses .gz format paired-end sequence files into individual FASTQ format files.
3. **Reads Quality Filtering and Adapter Trimming:** Uses the `fastp` tool for initial quality filtering and generates a
   preliminary quality report.
4. **Sequences Demultiplexing and Primer Sites Removing:** Employs the `Cutadapt` tool for demultiplexing and primer
   trimming, with adjustable minimum length and parallel processing.
5. **Reads Filtering, Error Learning, and Denoising:** Integrates the `DADA2` package for ASV denoising to resolve
   sequencing errors and accurately delineate unique genetic variants.
    - **Filtering Reads:** Uses the `fastqPairedFilter` function from `DADA2` to ensure matching IDs for paired-end
      reads.
    - **Error Learning:** Utilizes the `learnErrors` function from `DADA2` to build an error learning mechanism.
    - **Denoising**: Denoising using the `dada` function in `DADA2`, outputting denoised sequences, clustering
      information, and error matrices.
6. **ASV Merging:** Offers two merging strategies:
    - **DADA2 Merging:** Uses the `mergePairs` function from `DADA2` to merge paired-end reads, with a default minimum
      overlap of 12 bases and zero mismatches.
    - **Assembling with a reference:**
        - **Concatenation with 10Ns:** Concatenate ASVs with 10 Ns in cases where DADA2 cannot merge, ensuring the same
          direction of sequences.
        - **BLAST Alignment:** Uses `BLASTn` to align reads with reference sequences, selecting the best reference based
          on sequence length, identity, and E-value.
        - **MAFFT Alignment:** Uses the `MAFFT` tool to perform local pairwise alignment of the reference sequence with
          paired-end ASVs, with parallel processing.
        - **Sequence Merging:** Merges ASVs based on reference sequence information, and performs sequence degapping to
          ensure sequences are ready for subsequent use.
7. **Quality Control:**
    - Generates preliminary quality reports from `fastp`.
    - Generates error learning plots from `DADA2` to assess denoising performance.
    - Produces a comprehensive quality control report summarizing ASV performance, including read counts and merging
      results.
    - Optionally generates validation FASTA files per sample, containing well-aligned FASTA reads from each processing
      step.

**Parameter Tuning in PowerBarcoder**

PowerBarcoder allows users to adjust multiple parameters to optimize performance:

- **BLASTn:** Adjustable parameters for selecting the best reference sequence, with a default to BLASTn alignment of r1
  and r2 sequences separately.
- **Denoising:** Adjustable training dataset for `DADA2` error learning and parameters for the `mergePairs` function,
  including minimum overlap and maximum mismatch.
- **Alignment:** Adjustable parameters for `MAFFT`, such as localpairs and globalpairs, as well as gap penalties.
- **Quality and Quantity of Input Reads:** Evaluate the impact of read quantity on final ASV sequences and test the
  number of reads needed for accurate ASVs.

**Deployment of PowerBarcoder**

### With Docker (CLI & GUI):

```bash
# clone the repository
git clone https://github.com/PowerBarcoder/PowerBarcoder.git

# build the docker image (amd64)
docker build -t powerbarcoder .
# build the docker image (arm64)
docker build -t powerbarcoder --platform linux/arm64 .

# run the docker container
docker run -d -p 15000:15000 -v ${PWD}:/PowerBarcoder --name powerbarcoder powerbarcoder

# open the GUI in browser
open 127.0.0.1:15000

# (optional) enter the container for CLI
docker exec -it powerbarcoder bash
```

### Without Docker (CLI only):

```bash
1. install dependencies
2. prepare config.yml
3. git clone
4. cd {{PATH}}
5. bash powerbarcode.sh {{yyyyMMddhhmm}}
```

**QC Report Indices**

1. **Cutadapt:**
    - Cutadapt Demultiplex by Sample Barcode
    - Cutadapt Trim the Primer Sites
2. **DADA2:**
    - DADA2 Filter
    - DADA2 Denoise (r1)
    - DADA2 Denoise (r2)
    - DADA2 Merge
    - DADA2 10N Concat
3. **Merger Operations:**
    - Merger Blast
    - Merger Merge
4. **Best ASV Quality Control Metrics:**
    - Header
    - Sequence
    - Length
    - Ambiguous Sites Number
    - Lowercase Sites Number
    - BLAST SubjectID
    - BLAST Identity
    - BLAST qstart-qend
    - Identical to DADA2 Merge
5. **ASV Counts and Properties:**
    - Highest Abundance ASV
    - ASV Count
    - Best ASV Proportion
    - Best ASV Number
    - Hash Value (for different steps: DADA2 Denoise, DADA2 Merge, DADA2 10N Concat)

**Result Directory Structure**

```
└── PowerBarcoder                            # Root directory
    └── data                                 # Data directory
        └── result                           # Result directory
            └── 202402131807                 # Run Serial Number
                ├── config.sh                # Configuration file
                ├── error_rate_F.png         # Learn error matrix
                ├── error_rate_R.png         # Learn error matrix
                └── trnL_result              # trnL results
                    ├── blastResult          # Blast results
                    ├── demultiplexResult    # Demultiplexing results
                    │   ├── filtered            # Intermediate files
                    │   ├── trimmed             # Intermediate files
                    │   └── untrimmed           # Intermediate files
                    ├── denoiseResult        # Denoising results
                    │   ├── r1                  # Intermediate files
                    │   └── r2                  # Intermediate files
                    ├── mergeResult          # Merging results
                    │   ├── dada2               # Intermediate files
                    │   └── merger              # Intermediate files
                    └── qcResult             # Quality control results
                        ├── qcReport.csv        # Quality control report
                        └── validator           # Validation results
                            ├── all                # Retrieve all results
                            ├── best               # Retrieve ASV with highest abundance, prioritized: DADA2 merged > merger merged
                            ├── denoise            # Intermediate files
                            └── merge              # Intermediate files
```

