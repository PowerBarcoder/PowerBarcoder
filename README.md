# PowerBarcoder

## Why PowerBarcoder ? 
- Save your time and money with PowerBarcoder. 
- PowerBarcoder is a NGS data cleaning solution for Illumina Miseq. 
- It is designed to clean NGS data with high performance. 
- PowerBarcoder is a GUI based software, which is easy to use. 
- PowerBarcoder is a free software, which is open source. 
- PowerBarcoder is a cross-platform software, which can be used in Windows, Linux, and Mac OS.
  
- More details in https://docs.google.com/presentation/d/19bZbIb3AJ-kiar02kEzdDUU-y5KkmoGy/edit?usp=sharing&ouid=107280427804502451722&rtpof=true&sd=true

## Features
1. NGS Data Cleaning Solution (Miseq)
2. High performance with coroutines, multi-threading, and multiprocessing design
3. GUI for easy use
4. Docker for easy deployment
5. Flexible Blast mode options
6. QC report in single CSV file

## Flow Chart

![pipeline](https://github.com/PowerBarcoder/PowerBarcoder/blob/main/pipeline.png)


## Installation
- With Docker (CLI & GUI):
```
1. git clone
2. run docker container
  - docker build -t powerbarcoder .
  - docker run -d -p 5000:5000 -v ${PWD}:/PowerBarcoder --name powerbarcoder powerbarcoder
3. open 127.0.0.1:5000 in browser
```

- Without Docker (CLI only):
```
1. install dependencies
2. prepare config.yml
3. git clone
4. cd {{PATH}}
5. bash powerbarcode.sh {{yyyyMMddhhmm}}
```

## QC Report indices
1. Cutadapt:
    - Cutadapt Demultiplex by Sample Barcode
    - Cutadapt Trim the Primer Sites
2. DADA2:
    - DADA2 Filter
    - DADA2 Denoise (r1)
    - DADA2 Denoise (r2)
    - DADA2 Merge
    - DADA2 10N Concat
3. Merger Operations:
    - Merger Blast
    - Merger Merge
4. Best ASV Quality Control Metrics:
    - Header
    - Sequence
    - Length
    - Ambiguous Sites Number
    - Lowercase Sites Number
    - BLAST SubjectID
    - BLAST Identity
    - BLAST qstart-qend
    - Identical to DADA2 Merge
5. ASV Counts and Properties:
    - Highest Abundance ASV
    - ASV Count
    - Best ASV Proportion
    - Best ASV Number
    - Hash Value (for different steps: DADA2 Denoise, DADA2 Merge, DADA2 10N Concat)

## Result Directory Structure
   ```
   └── PowerBarcoder
       └── data
           └── result
               └── 202402131807
                   ├── config.sh            # Configuration file
                   ├── error_rate_F.png     # Learn error matrix
                   ├── error_rate_R.png     # Learn error matrix
                   └── trnL_result
                       ├── blastResult        # Blast results
                       ├── demultiplexResult
                       │   ├── filtered      # Intermediate files
                       │   ├── trimmed       # Intermediate files
                       │   └── untrimmed     # Intermediate files
                       ├── denoiseResult
                       │   ├── r1            # Intermediate files
                       │   └── r2            # Intermediate files
                       ├── mergeResult
                       │   ├── dada2         # Intermediate files
                       │   └── merger        # Intermediate files
                       └── qcResult
                           ├── qcReport.csv   # Quality control report
                           └── validator
                               ├── all        # Retrieve all results
                               ├── best       # Retrieve ASV with highest abundance, prioritized: DADA2 merged > merger merged
                               ├── denoise    # Intermediate files
                               └── merge      # Intermediate files