FROM bioconductor/bioconductor_docker:RELEASE_3_16

# install R dependencies
RUN R -e 'BiocManager::install("dada2", version="3.16", update=TRUE, ask=FALSE)'
RUN R -e "install.packages('foreach', dependencies = TRUE)"
RUN R -e "install.packages('doParallel', dependencies = TRUE)"

ENV PATH="/venv/cutadapt-venv/bin:$PATH"

# Install basic tool and cutadapt
RUN apt-get update && \
    apt-get install -y build-essential curl python3-dev python3-pip python3-venv && \
    python3 -m venv /venv/cutadapt-venv && \
    /venv/cutadapt-venv/bin/pip install cutadapt && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /usr/local/bin
# install blast
RUN curl -O https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/2.13.0/ncbi-blast-2.13.0+-x64-linux.tar.gz
RUN tar -zxvf ncbi-blast-2.13.0+-x64-linux.tar.gz && \
    rm ncbi-blast-2.13.0+-x64-linux.tar.gz && \
    ln -s /usr/local/bin/ncbi-blast-2.13.0+/bin/* /usr/local/bin/

# install fastp
RUN wget http://opengene.org/fastp/fastp.0.23.1 && \
    mv fastp.0.23.1 fastp && \
    chmod a+x ./fastp

# install mafft
RUN apt-get update && \
    apt-get install -y rpm && \
    curl -O https://mafft.cbrc.jp/alignment/software/mafft-7.520-gcc_fc6.x86_64.rpm && \
    rpm -Uvh mafft-7.520-gcc_fc6.x86_64.rpm

# install seqkit and seqtk
RUN apt-get update && \
    apt-get install -y seqkit && \
    apt-get install -y seqtk

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

#  docker build -t powerbarcoder .
#  docker run -d -p 5000:5000 -v ${PWD}:/PowerBarcoder --name powerbarcoder powerbarcoder
#  docker exec -it powerbarcoder bash

#  if WSL ext4.vhdx too large, run this command to shrink it
    #  docker builder prune
    #  wsl --shutdown
    #  diskpart
    #  select vdisk file="C:\Users\kwz50\AppData\Local\Docker\wsl\data\ext4.vhdx"
    #  attach vdisk readonly
    #  compact vdisk
    #  detach vdisk
    #  exit
    #  wsl
