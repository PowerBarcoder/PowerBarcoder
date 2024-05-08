# PowerBarcoder

## Why PowerBarcoder ?

- Save your time and money with PowerBarcoder.
- PowerBarcoder is a NGS data cleaning solution for Illumina Miseq.
- It is designed to clean NGS data with high performance.
- PowerBarcoder is a GUI based software, which is easy to use.
- PowerBarcoder is a free software, which is open source.
- PowerBarcoder is a cross-platform software, which can be used in Windows, Linux, and Mac OS.

- More details
  in https://docs.google.com/presentation/d/19bZbIb3AJ-kiar02kEzdDUU-y5KkmoGy/edit?usp=sharing&ouid=107280427804502451722&rtpof=true&sd=true

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
# clone the repository
git clone https://github.com/PowerBarcoder/PowerBarcoder.git

# build the docker image (amd64)
docker build -t powerbarcoder .
# build the docker image (arm64)
docker build -t powerbarcoder --platform linux/arm64 .

# run the docker container
docker run -d -p 15000:15000 -v ${PWD}:/PowerBarcoder --name powerbarcoder powerbarcoder

# open the GUI in browser
open 127.0.0.1:15000 in browser

# (optional) enter the container for CLI
docker exec -it powerbarcoder bash
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

## Debugging

1. if WSL ext4.vhdx too large, run this command to shrink it
   ```
     docker builder prune
     wsl --shutdown
     diskpart
     select vdisk file="C:\Users\kwz50\AppData\Local\Docker\wsl\data\ext4.vhdx"
     attach vdisk readonly
     compact vdisk
     detach vdisk
     exit
     wsl
   ```
2. different docker image for different platform
   2.1. build the docker image for amd64
   ```
     docker build -t powerbarcoder .
     docker run -d -p 5000:5000 -v ${PWD}:/PowerBarcoder --name powerbarcoder powerbarcoder
     docker exec -it powerbarcoder bash
   ```
   2.2. build the docker image for arm64
   ```
     docker build -t powerbarcoder --platform linux/arm64 .
     docker inspect powerbarcoder | grep Architecture
     docker run -d -p 15000:15000 -v ${PWD}:/PowerBarcoder --name powerbarcoder --platform linux/arm64/v8 powerbarcoder
   ```