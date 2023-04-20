FROM bioconductor/bioconductor_docker:RELEASE_3_16

# install R dependencies
RUN R -e 'BiocManager::install("dada2", version="3.16", update=TRUE, ask=FALSE)'

ENV PATH="/venv/cutadapt-venv/bin:$PATH"

# Install basic tool and cutadapt
RUN apt-get update && \
    apt-get install -y build-essential curl python3-dev python3-pip python3-venv && \
    python3 -m venv /venv/cutadapt-venv && \
    /venv/cutadapt-venv/bin/pip install cutadapt && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /usr/local/bin
# install blast and mafft
RUN curl -O ftp://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/ncbi-blast-2.13.0+-x64-linux.tar.gz && \
    tar -zxvf ncbi-blast-2.13.0+-x64-linux.tar.gz && \
    rm ncbi-blast-2.13.0+-x64-linux.tar.gz && \
    ln -s /usr/local/bin/ncbi-blast-2.13.0+/bin/* /usr/local/bin/ && \
    apt-get update && \
    apt-get install -y rpm && \
    curl -O https://mafft.cbrc.jp/alignment/software/mafft-7.520-gcc_fc6.x86_64.rpm && \
    rpm -Uvh mafft-7.520-gcc_fc6.x86_64.rpm

# install Python dependencies
WORKDIR /PowerBarcoder
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

## install parallel for multi-threading in bash (deprecated temporarily)
#RUN apt-get install -y parallel

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]

#sudo apt-get -y install util-linux